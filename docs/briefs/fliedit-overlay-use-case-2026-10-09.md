---
created: 2026-10-09
timestamp: 2026-10-09
---

# FliEdit: overlay images / B-roll on a FliCut export (research, 2026-10-09)

**Purpose**: David's use case (2026-10-09): FliHub → FliCut cut → export → open in FliEdit → lay images and/or short videos over the main video with transitions → export. Can it, and can an agent drive it?

**For Agents**: Read before ticketing FliEdit overlay work. Source: read-only code research by flivideo-orch's research agent; nothing was run live (FliEdit was not running).

## Verdict
FliEdit can do it from code, and it's agent-drivable by design (control door `~/Library/Application Support/fliedit/control.json`, `POST /v1/call`, 62 verbs in `fliedit/api/openrpc.json`, CLI `node bin/fliedit.mjs`). NOT verified live.

- Base track: the FliCut render `videos/<name>/<name>-cut.mp4` (never FliCut's document). Golden test `test/golden/parity.test.ts:43-52` = cut on V1 + overlay on O1 + export.
- Image overlay: yes (png/jpg/webp/gif/bmp/tiff; default 125 frames, any duration). Video overlay: yes (`clip.place` on O1, `withAudio:false`).
- Position/scale/crop/opacity/fit: `clip.setProps` (`src/core/render/geometry.ts:15-33`).
- Transitions: fade in/out of an overlay yes; dissolve only between touching clips on one track; NO wipes/slides/keyframed moves.
- Export: `export.start` → `task.status`, ffmpeg, h264/AAC mp4 at `videos/<edit>/<edit>-final.mp4`. Captions as a sidecar track + .srt (no burn-in: no libass).
- Trap found: d06's edit has the raw recordings on audio track A1 → would export a black picture (`fli.edit.d06-…-edit/history.jsonl` lines 2,4; `src/core/ops/edit-ops.ts:149,154`).

## Gaps — needed for the use case (dependency order)
1. **Image overlay proven end to end** — an image on O1 with fade in/out exports and matches the preview frame (images only tested in core, `test/core/ops.test.ts:21`).
2. **`assets.list` scans `resources/`** — d06 returns `resources/project/*.png` (today: audio, music, images, assets only, `src/main/media/resolver.ts:93`). Workaround: `source.add` with absolute path.
3. **No accidental video-on-audio-track** — dropping a video file on A1 warns or lands on V1 with linked audio.
4. **`flivideo:fliedit` skill** — start/stop, token, and the recipe edit.create → source.add (cut) → track.add (overlay) → clip.place → clip.setProps → transition.set fade → export.start → task.status. None exists (deferred in `docs/gap-ledger.md:75`).
5. **Cutaway plan input** — one JSON list `{asset, start, duration, fit, fade}` applied in one dry-runnable step, so an agent can map transcript moments (cut .srt) to B-roll.

## Nice to have
Wipe/slide transitions (ffmpeg xfade) · Ken Burns pan/zoom keyframes · burned-in captions (libass, G5) · MCP server · waveforms/filmstrips · FliCut output manifest (G2).

## Not verified
Any live call; d06 cut fps vs 25 fps canvas; image render quality; full-length render time; d07 (no cut yet).

## Live verification (2026-10-09, later the same morning)
Started with `scripts/app.sh start`, stopped with `scripts/app.sh stop` (was not running before). Throwaway project in a scratchpad, test media made with ffmpeg.
- **RPC: yes.** `POST /v1/rpc` (JSON-RPC 2.0) + `POST /v1/call`, Bearer token from control.json, door on 127.0.0.1:7171 (7170 is dev-server only). 62 verbs, matches api/openrpc.json. `/v1/openrpc.json` needs the token (FliCast's is open).
- **Docs page: yes, reference only.** `GET /v1/docs`, no login, generated from OpenRPC (`referencePage()` in `src/main/control/openrpc.ts`): filter, families, params, principal, idempotent, confirm, refusals. Gaps vs FliCast (ADR-0005/0008): page served `mode:"reference"`, `rpcPath:null` so the Fire form is off; no dry-run; no capability-console window (`agent:console`, dry-run default, undo per result); only reachable via Help menu; no "which copy" banner; no published snapshot.
- **Driveable: yes for every edit, not the viewer.** No verb for play/pause, J/K/L, step, prev/next edit, Home/End, seek/playhead, zoom/zoom-to-fit, snapping, select/select-all, inspector tabs, go-to-marker/chapter/caption. Human-only: `edit.pickPath`, `edit.reveal`, `export.start` overwrite, `system.quit/restart` force.
- **Live run: all pass.** context.select → edit.create → source.add (mp4 + png) → clip.place V1 (linked audio created) → track.add overlay O1 → clip.place png on O1 → transition.set fade → preview.frame (real PNGs, 86 ms; overlay visible) → history.undo → dry-runs via RPC, CLI and /v1/call (patch + inverse, version unchanged). edit.reveal as agent refused (-32001).
- **Oddities:** `context.get` returned null after edit.create with an edit open; CLI dry-run went out as `cli` without `--as`.
- **Not verified:** UI repaint after agent edits; export.start; preview.chunk; events stream; pages side by side in a browser.
