// W8 rerun of docs/runbooks/brand-race/race.mts against the BRANCH code (FliHub + FliStudio overnight/2026-10-29-fli-core-026,
// fli-core v0.26.0-rc.1). TEMP COPIES only: REAL is read, never written.
import { promises as nfs } from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { readManagedPublish, writeManagedPublish, managedPublishVersion } from '/Users/davidcruwys/dev/ad/flivideo/flihub-worktrees/fli-core-026/server/src/utils/managedBrandConfig.ts';
import { applyPublish } from '/Users/davidcruwys/dev/ad/flivideo/flistudio-worktrees/fli-core-026/server/src/capabilities/brand-publish.ts';
import { updateBrandSettings } from '/Users/davidcruwys/dev/ad/flivideo/flistudio-worktrees/fli-core-026/node_modules/@flivideo/core/dist/index.js';

const REAL = '/Users/davidcruwys/dev/video-projects/v-appydave/fli.brand.json';
const config = { now: () => new Date() };
const PRINCIPAL = 'agent:race-test';
let failures = 0;

async function fresh(name: string) {
  const dir = await nfs.mkdtemp(path.join(os.tmpdir(), `brand-race-w8-${name}-`));
  await nfs.copyFile(REAL, path.join(dir, 'fli.brand.json'));
  return { root: dir, file: path.join(dir, 'fli.brand.json') };
}
const load = async (f: string) => JSON.parse(await nfs.readFile(f, 'utf8'));
const report = (name: string, checks: Record<string, boolean>) => {
  const lost = Object.entries(checks).filter(([, ok]) => !ok).map(([k]) => k);
  if (lost.length) failures++;
  console.log(`${name}: ${lost.length ? 'LOST UPDATE -> ' + lost.join(', ') : 'nothing lost'}`);
};
const flihubPayload = (cached: any, ctaLabel: string) => ({
  ...cached,
  ctas: { ...cached.ctas, primaryCta: { ...cached.ctas.primaryCta, label: ctaLabel } },
});
const studioPatch = { descriptionTemplate: { endNote: 'STUDIO-ENDNOTE' } };
// FliHub's GET /api/poem-wui/brand-config: the publish block and the version it was read at.
const hubGet = async (file: string) => {
  const version = await managedPublishVersion(file);
  return { version, cached: await readManagedPublish(file) };
};
// FliHub's POST: refused 409 changed-elsewhere when the file moved since the GET.
const hubSave = async (file: string, cached: any, version: string | null, label: string) => {
  try {
    await writeManagedPublish(file, flihubPayload(cached, label), version ?? undefined);
    return 'saved';
  } catch (error: any) {
    if (error?.code === 'changed-elsewhere') return 'changed-elsewhere';
    throw error;
  }
};
// FliStudio's brand.playlists.set (youtube.ts setBrandPlaylists, branch): one updateBrandSettings.
const studioPlaylists = (root: string) =>
  updateBrandSettings(root, (s: any) => ({ ...s, youtube: { activePlaylists: ['PL-STUDIO'], defaultPlaylists: ['PL-STUDIO'] } }));

// S0 control: sequential, FliHub GETs after FliStudio wrote.
{
  const { root, file } = await fresh('s0');
  await applyPublish(config, root, studioPatch, PRINCIPAL, 'race test');
  const g = await hubGet(file);
  const saved = await hubSave(file, g.cached, g.version, 'HUB-CTA');
  const j = await load(file);
  report(`S0 control (sequential, fresh GET) [hub ${saved}]`, {
    hubSaved: saved === 'saved',
    studioEndNote: j.publish.descriptionTemplate.endNote === 'STUDIO-ENDNOTE',
    studioHistory: j.publish._meta.history.at(-1)?.by === PRINCIPAL,
    hubCta: j.publish.ctas.primaryCta.label === 'HUB-CTA',
  });
}

// S1 UI stale snapshot: FliHub panel loaded -> FliStudio applies -> FliHub Save. Expect 409, then reload + Save keeps both.
{
  const { root, file } = await fresh('s1');
  const g = await hubGet(file);
  await applyPublish(config, root, studioPatch, PRINCIPAL, 'race test');
  const before = await nfs.readFile(file, 'utf8');
  const stale = await hubSave(file, g.cached, g.version, 'HUB-CTA');
  const untouched = (await nfs.readFile(file, 'utf8')) === before;
  const again = await hubGet(file); // "Changed in another app — reload"
  const saved = await hubSave(file, again.cached, again.version, 'HUB-CTA');
  const j = await load(file);
  report(`S1 FliHub stale snapshot [stale save ${stale}; after reload ${saved}]`, {
    staleRefused: stale === 'changed-elsewhere',
    fileUntouchedBy409: untouched,
    studioEndNote: j.publish.descriptionTemplate.endNote === 'STUDIO-ENDNOTE',
    studioHistory: j.publish._meta.history.at(-1)?.by === PRINCIPAL,
    hubCtaAfterReload: j.publish.ctas.primaryCta.label === 'HUB-CTA',
  });
}

// S2 FliStudio stale: was "FliStudio read -> FliHub write -> FliStudio write". applyPublish no longer takes a settings it
// read earlier; it merges under the lock into what is on disk, so FliHub's write in between survives.
{
  const { root, file } = await fresh('s2');
  const g = await hubGet(file);
  const hub = await hubSave(file, g.cached, g.version, 'HUB-CTA');
  await applyPublish(config, root, studioPatch, PRINCIPAL, 'race test');
  const j = await load(file);
  report(`S2 FliHub write lands before FliStudio's apply [hub ${hub}]`, {
    studioEndNote: j.publish.descriptionTemplate.endNote === 'STUDIO-ENDNOTE',
    hubCta: j.publish.ctas.primaryCta.label === 'HUB-CTA',
  });
}

// S3 FliHub read -> FliStudio playlists.set -> FliHub write. Sequential: 409. Concurrent (both after the GET): the lock
// serialises them; whichever lands second sees its own outcome — nothing written is lost.
{
  const { root, file } = await fresh('s3');
  const g = await hubGet(file);
  const w = await studioPlaylists(root);
  const hub = await hubSave(file, g.cached, g.version, 'HUB-CTA');
  const j = await load(file);
  report(`S3a FliHub read -> FliStudio playlists write -> FliHub write [studio ${w.kind}; hub ${hub}]`, {
    studioYoutube: j.youtube?.activePlaylists?.[0] === 'PL-STUDIO',
    hubRefusedNotLost: hub === 'changed-elsewhere' || j.publish.ctas.primaryCta.label === 'HUB-CTA',
  });
}
{
  let lost = 0; let refused = 0;
  const N = 200;
  for (let i = 0; i < N; i++) {
    const { root, file } = await fresh('s3b');
    const g = await hubGet(file);
    const [hub, w] = await Promise.all([hubSave(file, g.cached, g.version, 'HUB-CTA'), studioPlaylists(root)]);
    const j = await load(file);
    if (w.kind !== 'written' || j.youtube?.activePlaylists?.[0] !== 'PL-STUDIO') lost++;
    if (hub === 'saved' && j.publish.ctas.primaryCta.label !== 'HUB-CTA') lost++;
    if (hub === 'changed-elsewhere') refused++;
    await nfs.rm(root, { recursive: true, force: true });
  }
  if (lost) failures++;
  console.log(`S3b concurrent FliHub save + FliStudio playlists.set, ${N} trials: ${lost} lost a written update; ${refused} FliHub saves refused 409 (told to reload)`);
}

// S4 truly concurrent publish writes, 200 trials (as the original S4).
{
  let lost = 0; let refused = 0;
  const N = 200;
  for (let i = 0; i < N; i++) {
    const { root, file } = await fresh('s4');
    const g = await hubGet(file);
    const [, hub] = await Promise.all([
      applyPublish(config, root, studioPatch, PRINCIPAL, 'race'),
      hubSave(file, g.cached, g.version, 'HUB-CTA'),
    ]);
    const j = await load(file);
    if (j.publish.descriptionTemplate.endNote !== 'STUDIO-ENDNOTE') lost++;
    if (hub === 'saved' && j.publish.ctas.primaryCta.label !== 'HUB-CTA') lost++;
    if (hub === 'changed-elsewhere') refused++;
    await nfs.rm(root, { recursive: true, force: true });
  }
  if (lost) failures++;
  console.log(`S4 unforced concurrency, ${N} trials: ${lost} lost a written update; ${refused} FliHub saves refused 409`);
}
console.log(failures ? `FAIL: ${failures} scenario(s) lost an update` : 'PASS: no scenario lost an update');
process.exit(failures ? 1 : 0);
