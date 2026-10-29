// Reproduces the fli.brand.json lost-update between FliHub and FliStudio against TEMP COPIES only.
// Real functions: FliHub readManagedPublish/writeManagedPublish (live flihub source, imported read-only),
// FliStudio applyPublish (live flistudio source) + fli-core v0.25 readBrandSettings/writeBrandSettings.
import { promises as nfs } from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import fsx from '/Users/davidcruwys/dev/ad/flivideo/flihub/node_modules/fs-extra/lib/index.js';
import { readManagedPublish, writeManagedPublish } from '/Users/davidcruwys/dev/ad/flivideo/flihub/server/src/utils/managedBrandConfig.ts';
import { applyPublish } from '/Users/davidcruwys/dev/ad/flivideo/flistudio/server/src/capabilities/brand-publish.ts';
import { readBrandSettings, writeBrandSettings } from '/Users/davidcruwys/dev/ad/flivideo/flistudio/node_modules/@flivideo/core/dist/index.js';

const REAL = '/Users/davidcruwys/dev/video-projects/v-appydave/fli.brand.json';
const config = { now: () => new Date() };
const PRINCIPAL = 'agent:race-test';

async function fresh(name: string) {
  const dir = await nfs.mkdtemp(path.join(os.tmpdir(), `brand-race-${name}-`));
  await nfs.copyFile(REAL, path.join(dir, 'fli.brand.json'));
  return { root: dir, file: path.join(dir, 'fli.brand.json') };
}
const load = async (f: string) => JSON.parse(await nfs.readFile(f, 'utf8'));
const report = (name: string, checks: Record<string, boolean>) => {
  const lost = Object.entries(checks).filter(([, ok]) => !ok).map(([k]) => k);
  console.log(`${name}: ${lost.length ? 'LOST UPDATE -> ' + lost.join(', ') : 'both writes survived'}`);
};

// FliHub's Save button payload (ConfigPanel.tsx:1197): {...cachedPublish, brand, socialLinks, ctas, affiliates, descriptionTemplate}
const flihubPayload = (cached: any, ctaLabel: string) => ({
  ...cached,
  brand: cached.brand,
  socialLinks: cached.socialLinks,
  ctas: { ...cached.ctas, primaryCta: { ...cached.ctas.primaryCta, label: ctaLabel } },
  affiliates: cached.affiliates,
  descriptionTemplate: cached.descriptionTemplate,
});
const studioPatch = { descriptionTemplate: { endNote: 'STUDIO-ENDNOTE' } };

// S0 control: sequential, FliHub GETs after FliStudio wrote.
{
  const { root, file } = await fresh('s0');
  const r = await readBrandSettings(root);
  await applyPublish(config, root, r.value, studioPatch, PRINCIPAL, 'race test');
  const cached = await readManagedPublish(file);
  await writeManagedPublish(file, flihubPayload(cached, 'HUB-CTA'));
  const j = await load(file);
  report('S0 control (sequential, fresh GET)', {
    studioEndNote: j.publish.descriptionTemplate.endNote === 'STUDIO-ENDNOTE',
    studioHistory: j.publish._meta.history.at(-1)?.by === PRINCIPAL,
    hubCta: j.publish.ctas.primaryCta.label === 'HUB-CTA',
  });
}

// S1 UI stale snapshot: FliHub Config panel loaded (GET) -> person applies a publish change in FliStudio ->
// person clicks Save Brand Config in FliHub. No simultaneity needed.
{
  const { root, file } = await fresh('s1');
  const cached = await readManagedPublish(file); // FliHub GET /api/poem-wui/brand-config
  const r = await readBrandSettings(root); // FliStudio brand.publish.set
  await applyPublish(config, root, r.value, studioPatch, PRINCIPAL, 'race test');
  await writeManagedPublish(file, flihubPayload(cached, 'HUB-CTA')); // FliHub POST
  const j = await load(file);
  report('S1 FliHub stale UI snapshot overwrites FliStudio publish.set', {
    studioEndNote: j.publish.descriptionTemplate.endNote === 'STUDIO-ENDNOTE',
    studioHistory: j.publish._meta.history.at(-1)?.by === PRINCIPAL,
    hubCta: j.publish.ctas.primaryCta.label === 'HUB-CTA',
  });
}

// S2 server interleave, FliStudio stale: FliStudio has read settings; FliHub's whole POST lands; FliStudio writes.
{
  const { root, file } = await fresh('s2');
  const r = await readBrandSettings(root);
  await writeManagedPublish(file, flihubPayload(await readManagedPublish(file), 'HUB-CTA'));
  await applyPublish(config, root, r.value, studioPatch, PRINCIPAL, 'race test');
  const j = await load(file);
  report('S2 FliStudio read -> FliHub write -> FliStudio write', {
    studioEndNote: j.publish.descriptionTemplate.endNote === 'STUDIO-ENDNOTE',
    hubCta: j.publish.ctas.primaryCta.label === 'HUB-CTA',
  });
}

// S3 server interleave, FliHub stale: inside writeManagedPublish, after its readFile resolves, FliStudio's
// brand.playlists.set (faithful copy of youtube.ts:218-238) writes youtube; then FliHub writes.
{
  const { root, file } = await fresh('s3');
  const cached = await readManagedPublish(file);
  const orig = fsx.readFile;
  let injected = false;
  (fsx as any).readFile = async (...a: any[]) => {
    const out = await (orig as any).apply(fsx, a);
    if (!injected && a[0] === file) {
      injected = true;
      const s = await readBrandSettings(root);
      const youtube = { activePlaylists: ['PL-STUDIO'], defaultPlaylists: ['PL-STUDIO'] };
      const w = await writeBrandSettings(root, { ...s.value, youtube });
      if (w.kind !== 'written') throw new Error(JSON.stringify(w));
    }
    return out;
  };
  await writeManagedPublish(file, flihubPayload(cached, 'HUB-CTA'));
  (fsx as any).readFile = orig;
  const j = await load(file);
  report('S3 FliHub read -> FliStudio playlists.set write -> FliHub write', {
    injected,
    studioYoutube: j.youtube?.activePlaylists?.[0] === 'PL-STUDIO',
    hubCta: j.publish.ctas.primaryCta.label === 'HUB-CTA',
  });
}

// S4 truly concurrent, no forced interleave: fire both at once, 200 trials, count losses.
{
  let lost = 0; let tornRead = 0;
  const N = 200;
  for (let i = 0; i < N; i++) {
    const { root, file } = await fresh('s4');
    const cached = await readManagedPublish(file);
    await Promise.all([
      (async () => {
        const r = await readBrandSettings(root);
        if (r?.kind !== 'valid') { tornRead++; return; } // real setPublish refuses here ('unusable-file')
        await applyPublish(config, root, r.value, studioPatch, PRINCIPAL, 'race');
      })(),
      writeManagedPublish(file, { ...cached, ctas: { ...cached.ctas, primaryCta: { ...cached.ctas.primaryCta, label: 'HUB-CTA' } } }),
    ]);
    const j = await load(file);
    if (j.publish.ctas.primaryCta.label !== 'HUB-CTA' || j.publish.descriptionTemplate.endNote !== 'STUDIO-ENDNOTE') lost++;
    await nfs.rm(root, { recursive: true, force: true });
  }
  console.log(`S4 unforced concurrency in one process (fresh GET each time): ${lost}/${N} trials lost an update; ${tornRead}/${N} FliStudio reads saw a missing/partial file mid FliHub write`);
}
