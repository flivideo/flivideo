# FliVideo architecture review — 2026-10-29

**Purpose**: The current architecture of the FliVideo family across four layers, and the design for FliStudio's extension core, written so extension #2 does not copy Overlay Pilot's coupling.

**For Agents**:
- This supersedes `docs/flivideo-standard-architecture-v1.0.md` and `docs/architecture-alignment-report.md` (Feb 2026, stale).
- §5 is the extension-core design. The build happens tomorrow with David, not overnight.
- Code was read on 2026-10-29. The B669 ChatGPT dossier is treated as a set of hypotheses; the code is the truth.
- Written by session `flivideo-arch-rsch` (M4). Extension architecture is owned by `flivideo-orch`, not by builders.

---


> **Status 2026-10-30 (flivideo-arch-rsch):** §5 is BUILT and live.
> - `@flivideo/extension-core` is merged into FliStudio `1e89742`, with Overlay Pilot migrated (64 tests, conformance included).
> - `system.status` busy is now real (C5 closed). `scripts/busy.sh` plus apps.json `busy` make `my-app restart flistudio` refuse while busy (FliStudio `f0dc19a`).
> - Still open: C6 (the server resolves the extension through dist, the client through source); C7 (Overlay Pilot's private FliTools client); `ExtensionHost` still carries Overlay Pilot's own settings; a YouTube upload is not in `system.status` busy.
> - Extension #2 is StoryPilot: brief `docs/briefs/storypilot-launch-2026-10-30.md`, session `storypilot-dev`, managed by flivideo-orch.
> - Cross-umbrella follow-on: `/Users/davidcruwys/dev/ad/brains/brand-dave/studio-pattern-synthesis-2026-10-30.md`.

## 0 · Recommendations first

1. **Build `@flivideo/extension-core` as a workspace package inside FliStudio**, modelled on how fli-core was made: a contract-first contents table, zod schemas with inferred types, a browser-safe entry, and zero host imports pinned by a test. Move `HostKit`, `OverlayHost`, `OverlayRefusal` and the menu descriptor into it (§5).
2. **Use the npm workspace properly now; do not create separate repos or publish anything.** Overlay Pilot is already `@flivideo/overlay-pilot`; finish the job with a `./client` export and imports by package name. That is what makes a later move a copy-and-paste (§6).
3. **Derive every host registry from the extension's descriptor.** Today, adding an extension means hand-editing seven places in FliStudio. Kybernesis's worst recurring failure was exactly this (§4).
4. **Pipeline stage, ruled:** a descriptor may declare `stage`. The extension shows in that stage's box as a link with no running dot, and never holds the current stage. With no `stage`, it goes in a plain "Extensions" group.
5. **Server verbs, ruled:** they stay on FliStudio's one capability door (`callCapability`), bound by one generic loop over the descriptor's capabilities. Names must start with the extension's namespace. Read-only status comes from each capability's `kind`, never from a hand-copied list.
6. **Wire extension busy state into FliStudio's restart safety.** `busyRuns` is exported by Overlay Pilot and used nowhere in FliStudio's server.
7. **Version drift in fli-core is cheap; one break needs a ruling.** FliCast and FliEdit still write `-final`, which v0.25 removed.
   - **Ruled:** they write `-cast` and `-edit`.
   - One `wholeVideoOwner` rule goes into fli-core, so FliStudio and FliEdit stop crediting different owners.
   - Overnight spec W3–W5.
8. **The zod split is the biggest real hazard in the family.** FliCast, FliEdit, FliCut and Teletubby each install zod 3 (via `@appydave/core`) **and** zod 4 (via fli-core). Teletubby already broke on it. Move `@appydave/core` to zod 4 as 0.2.0, as daytime work (§1.2).
9. **Neither template upgrade tool is safe to run on the apps.**
   - AppyStack's: FliStudio's `scaffoldCommit` is wrong, so it overwrites silently.
   - AppyTron's: it has no baseline at all.
   - Fix both tools before anyone runs them; FliStudio's catch-up tonight is a hand merge (§1.4).
10. **Duplicates:**
    - FliTools clients → fli-core only (four private copies to retire).
    - Logger, SerialQueue and config → `@appydave/core` only.
    - `atomicWrite` → acceptable to duplicate (§1.2).

---

## 1 · The four layers

| Layer | What it is | Where | Template / version |
|---|---|---|---|
| `@appydave/core` | Product-neutral process plumbing: Lifecycle, ConfigLoader, Logger, atomicWrite, SerialQueue, Store, a `z` re-export | `/Users/davidcruwys/dev/ad/apps/appydave-foundation/packages/core` | 0.1.0. Beneath both boilerplates; not the focus here |
| **AppyStack** | The RVETS boilerplate (React, Vite, Express, TypeScript, Socket.IO; npm workspaces client/server/shared) | `/Users/davidcruwys/dev/ad/apps/appystack` | create-appystack 0.4.18, appystack-upgrade 0.4.2 |
| **AppyTron** | The Electron boilerplate | `/Users/davidcruwys/dev/ad/apps/appytron` | create-appytron 0.1.0 |
| **FliVideo** | The umbrella: the apps plus fli-core | `/Users/davidcruwys/dev/ad/flivideo/` | — |
| **fli-core** | `@flivideo/core`: video-domain rules shared by the apps (brands, identity, layout, naming, lab paths, renders, publish, the capability contract, the open contract) | `/Users/davidcruwys/dev/ad/flivideo/fli-core`, GitHub `flivideo/fli-core`, consumed by git tag | v0.25.0 |
| **FliStudio** | The hub: brands, projects, the pipeline, launch/publish, and the only extension host | `/Users/davidcruwys/dev/ad/flivideo/flistudio` | AppyStack 0.4.18, `lastUpgrade: null` (never upgraded) |

**Apps by template** (from the marker file at each repo root):

| Template | Apps |
|---|---|
| AppyStack | FliStudio |
| AppyTron | FliCast, FliCut, FliEdit, Teletubby |
| None established | FliHub, FliTools, FliDeck, FliGen, FliVoice, Storyline, fli-brief, flilaunch |

**How the layers depend on each other:**

```
            @appydave/core  (process plumbing)
             ▲            ▲
   AppyStack template   AppyTron template          fli-core  (video domain; zod only,
             ▲            ▲                           ▲        deliberately NOT on @appydave/core)
         FliStudio    FliCast FliCut FliEdit Teletubby ─┘   + FliHub, FliTools
             ▲
   @flivideo/extension-core   (proposed, §5 — FliStudio only)
             ▲
   modules/overlay-pilot, modules/<extension #2>
```

**Settled boundaries:**

- fli-core is for what **several apps** must agree on: file names, folder layout, schemas on disk, the capability and lifecycle contracts.
- Extension contracts are **FliStudio-only**, so they do not belong in fli-core. David's correction in B669 §7.3 is confirmed by the code: no other app hosts extensions.
- The W1 brief that created fli-core (`fli-core/docs/briefs/overnight-W1-fli-core.md`) says: "runtime dependency: `zod` only (no `@appydave/core` …)".

### 1.1 Who depends on fli-core

| Consumer | Pin | Verdict on the drift (checked by reading code) |
|---|---|---|
| FliStudio (server, shared, client, overlay-pilot) | v0.25.0 | current |
| FliCast, FliEdit | v0.23.0 | **bump needs work:** they call `videoFileName({kind:'final'})`, which v0.25 removed |
| FliCut | v0.18.0 | bump is trivial |
| FliHub (server, shared) | v0.15.0 | bump is trivial |
| FliTools | v0.11.0 | safe to leave |
| Teletubby | v0.7.3 | safe to leave |

**Measured 2026-10-29** (each app in a worktree, pin forced to v0.25.0):

- **FliCast and FliEdit break, on `final` only** (one TS2322 each).
  - FliCast's cast-export path silently becomes `null` (7 test failures).
  - FliEdit's `exportPath` would throw at runtime, and no test covers it.
- **FliCut, FliHub, FliTools and Teletubby:** 0 new type errors, and no real new test failures (only load flakes).
- **Trap:** a plain `npm install` after changing the pin keeps the old commit from the lockfile. Install the tag explicitly.

**Cross-app agreement on disk:**

- **Holds** for control files, window state, `fli.words.json`, `fli.studio.json`, the brand and machine registries, and the project layout. Those modules have not changed in any breaking way since the oldest pin.
- **Real divergences:**
  - the `-final` file name (above);
  - FliStudio and FliEdit credit different owners for the same whole-video file;
  - `fli.brand.json` has two writers with no lock (§1.3).

### 1.2 Duplicated code across apps

**Who uses `@appydave/core` (12 consumers):**

- **Apps:** FliCast, FliEdit, FliCut, Teletubby, ImageDrip, Samantha.
- **Templates:** the AppyTron template (and its factory copy), the AppyStack template (logger only), AppySentinel core and template.
- **Not consumers:** AngelEye, Captain's Log, AppyRadar, FliHub, FliStudio, FliTools.
- **Content:** the vendored tgz, git `791e1c9`, the working tree and npm 0.1.0 are byte-for-byte the same content today. But npm has only ever had 0.1.0, so the `^0.1.0` and `file:` consumers will drift silently on the next change.

**⚠ zod skew is live, not theoretical:**

- `@appydave/core` brings zod 3.25; fli-core brings zod 4.6.
- FliCast, FliEdit, FliCut and Teletubby each install **both majors**.
- FliCast mixes them in its own source.
- Teletubby was already bitten: `src/core/fli-zod.ts` documents a TS2719 error.
- **Fix (daytime, breaking):** `@appydave/core` 0.2.0 on zod 4, or zod as a peer dependency. Not overnight.

**Where each duplicated utility belongs:**

| Utility | Belongs in | Reason |
|---|---|---|
| `atomicWrite` | **Acceptable to duplicate**: fli-core keeps its own, apps use `@appydave/core`'s | About 15 lines. fli-core's `wx` + pid temp is the safer one; port that into `@appydave/core`. Adding a fli-core → `@appydave/core` dependency would cost 7 tag bumps and reopen the zod split. Fix fli-core's `window-state.ts`, which hand-rolls a weaker copy (non-hidden temp, ms-collision, no cleanup), to call its own `atomicWrite` |
| `takeLock` (lock file) | **fli-core only** | Every user is a domain read-modify-write (words, series, youtube) |
| SerialQueue | **`@appydave/core` only** | Neutral; nobody imports it yet, and five apps hand-roll queues |
| Logger, config loading | **`@appydave/core` only** | Neutral. FliStudio and FliHub use raw pino |
| zod `z` re-export | **Both, but contracts take `z` from fli-core** | Collapses to one when `@appydave/core` moves to zod 4 |
| FliTools client | **fli-core only** | Domain; shipped since v0.8. Four private copies: FliCast, FliCut, FliHub and Overlay Pilot. FliCut's 45-minute polling and Overlay Pilot's `wordsOf`/`cleanAudio` may need fli-core's client extended first |
| Open-context resolution | **fli-core only** | Domain contract. FliCast/FliCut wiring on fli-core primitives is fine; Teletubby's documented departure stays until its projects have identity files |


### 1.3 `fli.brand.json` lost update

FliHub writes it by plain read-modify-write (`managedBrandConfig.ts`: no lock, not atomic); FliStudio writes it through fli-core. **CONFIRMED (reproduced with the real write functions on temp copies):**

- **The confirmed sequence:**
  1. FliHub's Brand Config panel is loaded;
  2. a publish change is applied in FliStudio;
  3. Save is clicked in FliHub;
  4. FliStudio's change is lost.
- No simultaneous clicks are needed: FliHub posts its whole cached `publish` block.
- Two millisecond-window races also exist: FliStudio's `brand.publish.set` and `brand.playlists.set` (which agents can call).
- **Fix:** overnight W8 adds a lock-and-re-read `updateBrandSettings` in fli-core, and FliHub gets a version check (409 when the file changed since the panel loaded).
- **Noted, not fixed:** fli-core's brand schemas strip unknown keys on write.

### 1.4 Templates

**AppyStack** (`/Users/davidcruwys/dev/ad/apps/appystack`):

- **main is clean.** `spaghetti/step3-wip` is unmerged lint tooling and is red; main does not depend on it.
- `create-appystack/template` is a **stale synced copy** of `template/`, and the upgrade tool reads the stale copy by default.
- Patch/minor upgrades are safe. Majors are excluded: vite 8, vitest 5, TypeScript 7, zod 4 for the template, eslint 10.

**⚠ `appystack-upgrade` must not run on FliStudio as is:**

- FliStudio's `appystack.json` `scaffoldCommit` (`28d3805b…`) exists nowhere. The real scaffold is `522079a`.
- The tool's `git diff` error is swallowed as "unchanged", so it would **silently overwrite** FliStudio's middleware, ci.yml and eslint config (even with `--yes`).
- It would also re-add `useSocket.ts`, which FliStudio deleted on purpose.
- The tool has no dry-run.
- Bringing FliStudio up to date is therefore a **hand merge**: one template fix (`server/src/config/logger.ts`), with everything else app-owned.

**AppyTron** (`/Users/davidcruwys/dev/ad/apps/appytron`, canonical; `appytron-factory` is a merged leftover worktree):

- The upgrade engine has **no scaffold baseline**. It overwrites every differing template-owned file, including each app's preload IPC bridge (FliCast alone: about 360 lines).
- All four apps are on create-appytron 0.1.0 against 0.2.0 and have never been upgraded.
- FliCut and Teletubby are on **Electron 34** against the template's 44.
- **No AppyTron app upgrades overnight.** The tool needs a baseline (like AppyStack's `scaffoldCommit`) first.


---

## 2 · FliStudio as an extension host: what exists today

**Overlay Pilot** (`flistudio/modules/overlay-pilot`, `@flivideo/overlay-pilot`, private, npm workspace) is better built than B669 assumed:

| Good: keep it | Evidence |
|---|---|
| Fenced by dependency-cruiser: a module never imports FliStudio, and FliStudio meets it only at its entry files | `flistudio/.dependency-cruiser.cjs:18-50` |
| Host capabilities are **handed in**, not imported: `HostKit` for the screen, `OverlayHost` for the server | `modules/overlay-pilot/client/kit.ts`, `server/host.ts` |
| Server verbs are fli-core `defineCapability` contracts and ride FliStudio's one door (`callCapability`: validation, ★ fence, output check), so HTTP, JSON-RPC and CLI cannot drift | `shared/contracts.ts` spreads `OVERLAY_PILOT_CAPABILITIES`; `registry.ts:289` |
| The screen calls the same door as an agent (`kit.call` → `POST /api/call` as `human:ui`) | `client/src/components/ModuleKit.tsx` |
| Split client/server/shared, with its own tests and coverage | `modules/overlay-pilot/package.json` |

**The coupling that extension #2 would copy:**

| # | Problem | Where | Why it matters |
|---|---|---|---|
| C1 | **The contract lives in the extension.** `HostKit`, `Answer`, `PlayerItem`, `OverlayHost`, `CallAnswer`, `OverlayRefusal` and `must()` are defined in Overlay Pilot; FliStudio imports their types from it | `client/kit.ts`, `server/host.ts`; host: `ModuleKit.tsx:2`, `registry.ts:127-131` | Extension #2 would either import from Overlay Pilot (cross-extension coupling) or redefine them (twins that drift) |
| C2 | **Folder-path reach-in on the client.** `../../../modules/overlay-pilot/client` | `ProjectHome.tsx:35`, `ModuleKit.tsx:2` | The package declares no `./client` export, so the path is the only way in; depcruise allows it as a special case (`.dependency-cruiser.cjs:29`) |
| C3 | **Seven hand-edited host sites per extension**: `shared/contracts.ts` (import + spread), `registry.ts` (import, 14 per-verb lines, a bespoke `overlayHost()` and `overlay()` wrapper), `client/src/api.ts` (read-only list copied by hand, kept equal by a mirror test), `ProjectHome.tsx` (import, `EXTENSIONS` array, a `view === 'ext:overlay-pilot'` branch, a dedicated `OverlayPilotScreen`), `ModuleKit.tsx`, root `package.json` workspaces, `CapabilityContext.overlay` | as listed | This is Kybernesis's KYB-245 class of failure: a hand-kept map per extension |
| C4 | **The stage is hard-coded.** PipelineStrip puts every extension under the Overlay box | `ProjectHome.tsx` `PipelineStrip` / `stagesOf` | The open contract decision |
| C5 | **Busy state is not wired.** `busyRuns` is exported, but FliStudio's server never imports it | `server/index.ts` exports it; `command grep -rn busyRuns flistudio/server/src` → no hits (positive control: the same search finds `@flivideo/overlay-pilot`) | FliStudio's restart safety cannot see an overlay run in progress |
| C6 | **Server via dist, client via source.** The server imports built `dist/`, so the module must be built before the server runs; the client imports TS source | `package.json` exports; `.dependency-cruiser.cjs:30` | Two resolution rules for one package; a stale `dist/` is a silent hazard |
| C7 | **A private FliTools client** | `modules/overlay-pilot/server/flitools.ts` | Fifth copy of a client fli-core already ships (§1.2) |

**Not wrong, but say it in the contract:**

- "FliStudio reads an extension's results from disk and never calls the module" is true **of the project page**: it counts `-overlay-` exports in `videos/`.
- The extension's own screen and agents **do** call its verbs, through the door.
- The contract must state both, so neither gets "fixed" later.

---

## 3 · B669 dossier: hypotheses vs code

| B669 claim | Code says | Status |
|---|---|---|
| The first extension is unaudited; boundary compliance unknown | Fenced by depcruise, host-injected, own tests (§2) | **Mostly compliant.** The gaps are contract ownership and host wiring, not leakage |
| Extensions must not depend on FliStudio; FliStudio consumes them | Already enforced (`a-module-never-imports-flistudio`) | **True today** |
| A shared contract package is needed | It exists by accident, inside the first extension (C1) | **Confirmed, and needed** |
| Extension contracts do not belong in fli-core | No other app hosts extensions | **Confirmed** |
| One package per extension holding client, server and shared | Already the shape of `modules/overlay-pilot` | **True today** |
| DI per tier (different client and server capabilities) | `HostKit` (client) and `OverlayHost` (server) already differ | **True today**; generalise it |
| Express routes / Socket.IO events per extension | Neither exists. Verbs go through `callCapability`; live updates come via `kit.onChange` (the estate feed) | **Rule: extensions get no routes and no sockets of their own** (§5.4) |
| Lint/test enforcement | depcruise rules exist and are generic over `modules/[^/]+` | **True today**; add a conformance suite |

---

## 4 · Kybernesis prior art: KBDE "the seam"

**What it is:**

- The extension system in **KBDE**, Kybernesis's KyberAgent Desktop/Enterprise (Electron plus a daemon), is called "the seam". The repo is `/Users/davidcruwys/dev/kybernesis/KBDE-KyberAgent-Enterprise`.
- It has two packages: contracts in `packages/extension-contracts`, and the SDK in `packages/extension-sdk` (`define*` builders, seam ports, an in-memory host, conformance checks C1–C16).
- The extensions David built on it, `captains-log` and `muster`, live in `/Users/davidcruwys/dev/ad/apps/kyberagent-extensions`.
- "FDE" in its docs means Forward-Deployed Engineer: the third-party author path.

**Why it was hard:**

- Extensions ran **out of process**: sandboxed iframes over a custom `kyber-ext://` protocol, daemon-supervised backend children, signed tarballs, CSP and an origins allowlist.
- On top of that, the rules were enforced only at the host and never told to the author. The first end-to-end install hit five silent hops, and four of them reported success while broken (KYB-451/452).

| Pattern | For FliStudio (in-process) |
|---|---|
| One typed descriptor per extension, written with builders | **Carry over** → `defineExtension()` (§5.1) |
| Derive registries from the descriptor, never a hand-kept map (KYB-245, docs/93 §6) | **Carry over** → fixes C3 |
| Namespaced ids, with host namespaces reserved | **Carry over** → verb names must start with `<namespace>.` |
| Capabilities injected as ports, no globals | **Carry over** → already the case (`HostKit`/`OverlayHost`); move them to the core |
| In-memory host plus a conformance suite every extension runs | **Carry over** → `@flivideo/extension-core/testing` (§5.5) |
| Fail loudly to the author at registration/test time | **Carry over** → conformance runs in the extension's own `npm test` |
| `contractVersion` on the contract | **Carry over** (cheap) |
| Declared permissions must match real calls ("18 declared, 7 wired") | **Lighter form**: fli-core's ★ fence and principals already gate every verb. No separate permission list |
| Single activation authority, default-deny install | **Drop.** In-process extensions are compiled in; they are on if listed |
| Iframe sandbox, postMessage seam, custom protocol, CSP, origins allowlist | **Out-of-process only. Drop** |
| Daemon-supervised backends, health checks, ports | **Out-of-process only. Drop** (no extension ports; KYB-469 was three copies of port 7301) |
| Signing, TOFU ledger, self-contained bundles | **Out-of-process only. Drop** |
| Serialized wire format plus decode checks | **Drop.** The capability door's zod validation already does this |
| A separate foundry repo with independent publishing | **Drop for now** (§6) |
| **Anti-patterns to avoid:** building every surface twice; per-id hand-registered handlers; two names for one SDK package; spec ahead of the first real consumer; no logging for extensions; status labels that misreport | Each is a rule in §5. One name (`@flivideo/extension-core`); `host.log`; the core is built from Overlay Pilot's real needs only, not a speculative taxonomy |

**The lesson in one line:** almost everything that made KBDE hard came from the process boundary. The parts worth keeping are the cheap ones: a typed descriptor, registries derived from it, injected ports, and a conformance suite.

---

## 5 · Extension-core design

### 5.0 How fli-core was made, and what this copies

fli-core (W1, 2026-09-15) was built:

- **contract first**: a contents table in the FliStudio spec §4;
- **from existing behaviour**: "copy the *rules*, not the file";
- with **zod schemas and inferred types**;
- with a **browser-safe `./contracts` entry**;
- with **zero app imports, pinned by an architecture test**.

The extension core copies all five. The one difference: it lives **inside the FliStudio repo**. fli-core needed its own repo and git tags because seven repos consume it. The extension core has exactly one consumer repo.

### 5.1 Package

```
flistudio/
  extension-core/                 @flivideo/extension-core   (private, workspace)
    src/descriptor.ts             ExtensionDescriptor, StageKey, defineExtension()
    src/client.ts                 HostKit, Answer, PlayerItem, ExtensionScreen   ← browser-safe entry
    src/server.ts                 ExtensionHost, CallAnswer, ExtensionRefusal, must(), ExtensionServer
    src/testing.ts                fakeHost(), fakeKit(), conformance(ext)
    test/architecture.test.ts     imports only: relative, zod, react (types), @flivideo/core/contracts
  modules/overlay-pilot/          depends on @flivideo/extension-core + @flivideo/core
```

**Exports:** `.` (descriptor, browser-safe), `./client` (browser-safe), `./server` (node), `./testing`.

**Dependencies:** `@flivideo/core` (for `defineCapability`, `CapabilityContract` and failure codes), zod, and `react` as a type-only peer dependency.

### 5.2 The descriptor: one object, every host registry derived from it

```ts
// modules/<name>/shared/descriptor.ts  (browser-safe: no node imports)
export const OVERLAY_PILOT = defineExtension({
  key: 'overlay-pilot',              // url: ext:overlay-pilot, test ids, folder name
  label: 'Overlay Pilot',
  namespace: 'overlay',              // every verb must be named overlay.*
  stage: 'overlay',                  // optional: script|record|edit|overlay|launch|publish; absent → "Extensions"
  contractVersion: 1,
  capabilities: OVERLAY_PILOT_CAPABILITIES,   // fli-core defineCapability contracts
});
// read-only verbs = capabilities whose kind is 'query'; no hand list
```

```ts
// modules/<name>/client/index.ts
export default defineExtensionClient(OVERLAY_PILOT, OverlayPilot);   // Screen: ({kit, brand, project}) => JSX

// modules/<name>/server/index.ts
export default defineExtensionServer(OVERLAY_PILOT, {
  handlers: (host) => ({ 'overlay.sources': …, … }),   // typed: must cover every capability, nothing else
  busy: () => busyRuns(),                              // optional; joins FliStudio's restart safety
});
```

### 5.3 The host side: one list per tier, everything else generic

```ts
// flistudio/shared/src/extensions.ts
export const EXTENSIONS = [OVERLAY_PILOT] as const;           // descriptors only (browser-safe)
// shared/src/contracts.ts: ...capabilitiesOf(EXTENSIONS)

// flistudio/server/src/extensions.ts
export const EXTENSION_SERVERS = [overlayPilotServer] as const;
// registry.ts: ...bindExtensions(EXTENSION_SERVERS, hostFor)  ← replaces the 14 lines + overlay()/overlayHost()
// system status: busy = [...appBusy, ...EXTENSION_SERVERS.flatMap(e => e.busy?.() ?? [])]

// flistudio/client/src/extensions.ts
export const EXTENSION_CLIENTS = [overlayPilotClient] as const;
// api.ts READ_ONLY: ...readOnlyOf(EXTENSIONS)    ProjectHome: generic ext:<key> route + PipelineStrip by stage
```

**Adding extension #2 touches exactly:**

- its own folder;
- one line in each of the three lists;
- the root `workspaces` entry.

Everything else is derived.

**Registration is static (build time).** There is no discovery, no activation and no dynamic loading. In-process, compiled-in extensions do not need them, and KBDE shows what they cost.

### 5.4 Contract rules (to go in the core's README; tested where marked ✔)

1. ✔ An extension imports only `@flivideo/extension-core`, `@flivideo/core`, its own files and npm libraries. It never imports FliStudio or another extension (depcruise, existing, generalised).
2. ✔ FliStudio imports an extension only by package name and only through its declared exports (`./client`, `./server`, `./contracts`). No relative paths (C2).
3. ✔ Every verb name starts with `<namespace>.`. Namespaces are unique, and the host namespaces (`project`, `export`, `publish`, `system` …) are reserved.
4. ✔ The handler set equals the capability set, no more and no less (types plus conformance).
5. **Server verbs, ruled:** bound by `bindExtensions`. Each handler runs under `callCapability` (validation, ★ fence, principal, output check) exactly like a core verb. An `ExtensionRefusal` maps to FliStudio's `Refusal` in one place.
6. **No routes, no sockets.** An extension gets no Express router and no Socket.IO access. Requests go through the door. Live updates come through `kit.onChange` (the estate feed), plus a future `kit.onEvent(name)` if a real need appears. This removes B669's §9.4–9.5 questions by design.
7. **Stage, ruled:**
   - `stage` is optional.
   - The extension appears in that stage's box as a link (no running dot) to `ext:<key>`.
   - Extensions are optional work, so they never hold the current stage.
   - No `stage` → the "Extensions" group.
   - Results are read from disk by the page, never by calling the extension.
8. Host capabilities are injected only through `HostKit` (client) and `ExtensionHost` (server). `ExtensionHost` gains `log(line)`: KBDE's missing logging capability.
9. An extension that runs long work exposes `busy()`. FliStudio adds it to `system.status` busy, so restarts are refused while an extension works (C5).
10. Shared FliVideo-domain code (a FliTools client, open context, naming) comes from fli-core, never a private copy (C7).

### 5.5 Conformance suite (`@flivideo/extension-core/testing`)

Every extension's own `npm test` runs `conformance(descriptor, server, client)`, which checks:

- the descriptor is valid;
- the namespace is respected;
- the handlers match the capabilities;
- each query verb has `kind: 'query'`;
- the screen renders with `fakeKit()` and makes no calls on mount that are not queries;
- `fakeHost()` handlers refuse with typed codes;
- `busy()`, if declared, returns an array.

This is KBDE's C1–C16 idea at in-process size. It **fails at the author's desk**, not in the host.

### 5.6 Migration of Overlay Pilot (tomorrow, before extension #2)

1. Create `extension-core` with the types moved verbatim from `kit.ts` and `host.ts`. Rename `OverlayHost` → `ExtensionHost`, `OverlayRefusal` → `ExtensionRefusal`, and keep the old names as re-exports for one release.
2. Overlay Pilot: add a `descriptor.ts` and the `./client` export, and call `defineExtensionServer`/`defineExtensionClient`.
3. FliStudio: add the three lists plus `bindExtensions`, `readOnlyOf` and a generic `ext:` route. Delete the 14 lines, the `overlay()`/`overlayHost()` pair, the copied read-only list and `OverlayPilotScreen`. Group PipelineStrip by `stage`. Wire `busy`.
4. Gates:
   - typecheck, unit, e2e and depcruise all green;
   - `command grep -rn "modules/overlay-pilot" flistudio/client/src flistudio/server/src flistudio/shared/src` returns nothing;
   - Overlay Pilot runs conformance;
   - the project page looks unchanged (David looks).

---

## 6 · Packages: the call

**Use the workspace properly now; leave separate repos and publishing for later, probably never.** David's instinct ("too early; get the architecture right so the later move is copy-and-paste") is right about *repos and publishing*, and wrong about the *workspace*:

- Overlay Pilot is already an npm workspace package.
- The thing that blocks a copy-and-paste move is not the package boundary. It is the relative-path import, the hand-wired host lists and the contract living in the wrong package.
- Declaring exports, importing by package name and putting the contract in its own workspace package cost an afternoon and change nothing at runtime.
- They are also exactly what makes a later move to its own repo mechanical: change `"workspace"` to `"github:…#tag"` and nothing else.
- Plain folders would remove the one mechanical guard (package `exports`) that turns a boundary breach into a build error rather than a review comment.

---

## 7 · Not verified

- I did not run FliStudio or the extension. The design is from reading code.
- **Checked after commit:** all nine `HostKit` members are used by Overlay Pilot:
  - `call`, `mediaUrl`, `toast` and `onChange` in its code;
  - `Here`, `CopyImage`, `Button`, `Info` and `Player`, destructured in `OverlayPilot.tsx:181` and `PlanBoard.tsx:35`.
  Move all of them; there is nothing to drop.
- **Checked after commit:** FliStudio's `system.status` hard-codes `busy: []` (`server/src/capabilities/control.ts:72`). So C5 is confirmed: a FliStudio restart cannot see an Overlay Pilot run in progress. §5.4 rule 9 is where this gets fixed.
- KBDE findings come from its docs and KDD files; nobody re-ran KBDE.
