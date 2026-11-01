---
created: 2026-11-01
timestamp: 2026-11-01T14:00+07:00
---
# Story Pilot "Listen" — hear the script, one paragraph at a time (design, 2026-11-01)

Design only. No code changed. Builds on `docs/specs/resources-model-2026-11-01.md` (where the audio is *not* a resource).
Visual page: `docs/specs/storypilot-listen-2026-11-01.html` · https://claude.ai/artifact/R4GPEs2XUkfjUpdkXweGno (private).

## Verdict

Orch's take is **right on the big three** (per-piece audio keyed by a text hash; it's cache, not a resource or recording; auto
on first write, "out of date" after). I **disagree on four details** (section 9). The one real design risk is not the
player: it is **who runs Kokoro**, and **that nothing today cleans a cache automatically**.

## 1. The unit: paragraph, not chapter

Story Pilot has no chapters today. D13's `script.md` is 17+ plain paragraphs separated by blank lines (`grep -c '^## '` = 0), and
`story.json` already indexes things by paragraph (`script.triggers.items[].paragraph`). So the natural unit is the **paragraph**.
A "chapter" grouping can be layered later (a run of paragraphs) without changing the cache: audio files stay per paragraph,
a chapter is just a play-range. FliHub's chapters are recorded takes (each chapter = several segment files), a different thing.

## 2. Where the files live and how they are named

Home: **`<project>/-renders/storypilot/<slot>/audio/`**, built with fli-core's existing `rendersPath({projectDir, tool:'storypilot', subject:<slot>})` (`fli-core/src/renders.ts:34-44`). Slot is `project` for D13.

```
-renders/storypilot/project/audio/
  manifest.json                    # what the player reads
  p01-3fa9c21b7d04.mp3             # paragraph 1, hash of its spoken text + voice + speed + engine
  p02-81c0d5e2a9b7.mp3
  …
```

- Name = `p<NN>-<hash12>.mp3`. Content-addressed: change the words → new hash → new file; the old one is now an orphan.
- `manifest.json`: `{ schema, voice, speed, engine: 'kokoro-82m@<version>', paragraphs: [{ n, hash, file, ms, bytes, madeAt }] }`.
- mp3 (Kokoro skill supports `.mp3`/`.wav` via ffmpeg; mp3 ≈ 1 MB/min, wav ≈ 2.9 MB/min at 24 kHz mono). mp3 for caching.
- Why not elsewhere: `resources/` = a curated thing Launch/Publish read; `voice/` = FliCast source recordings (`classify.ts:16-17`); `recordings/` = FliHub takes; `script/` = tier *authored*, never cleaned (`classify.ts:243-247`).
- Already git-ignored (`gitignore-rules.ts:79` ignores `-renders/`). Already counted in the project's renders size (`rendersOf`).

## 3. Cache key and staleness rule

```
spoken  = normalise(paragraphText)      # strip markdown, collapse whitespace, the same text the TTS is given
hash    = sha256(spoken + '\0' + voice + '\0' + speed + '\0' + engineVersion)[0:12]
```
- **Fresh** = `manifest.paragraphs[n].hash === hash(current text)` and the file exists.
- **Stale** = the paragraph's current hash differs (words, voice, speed or engine changed). Computed live in the client from `script.md`; no timestamps.
- **Missing** = no manifest row / file deleted (cache cleared). Treated like stale for the UI, but copy says "not generated".
- **Paragraph shift:** if a paragraph is inserted, indices move but hashes don't — match by hash first, by index second, so inserting paragraph 4 doesn't regenerate 5–17. (Implementation note for the builder; this is why the key is the *text*, not the position.)
- Cosmetic edit (trailing space, markdown only) normalises to the same hash → still fresh.

## 4. Generation triggers

| When | What | Why |
|---|---|---|
| Script **first written** (first `story.script.set` for a slot with no manifest) | generate all paragraphs in the background | David: "when you first create a script you really do want audio" |
| After that, a paragraph edit | mark that paragraph **stale**; show "audio out of date", one click regenerates just it | David: "if you're refactoring you don't necessarily want it" |
| `Listen ▸ Regenerate all stale` | button, batches the stale ones | after a big rewrite |
| Voice or speed changed | all become stale (hash covers them) | no silent mass-regeneration |
| Never | on every save | avoids Kokoro churn during refactors |

Background means: the Script screen is usable immediately, paragraphs light up as they finish (a per-paragraph progress dot).

## 5. Who runs Kokoro (the real risk)

Kokoro today is a **skill + a Python venv at `~/.kokoro-tts/`, Apple Silicon only**, played via `afplay` (`appydave-plugins/appydave/skills/kokoro-tts/SKILL.md`). A FliStudio server shelling out to that venv is a hidden, per-machine dependency.

Recommendation: put it behind **FliTools** (the suite's local-model service on `:7161`; per memory it already owns transcription). Story Pilot asks FliTools "speak this text with voice V → file path under `-renders/…`" and FliTools owns the venv, the model, and the "not installed on this machine" error. If FliTools isn't ready, the fallback is a thin server helper calling the skill's `speak` shim, written to be swapped. I did **not** find any TTS code in FliTools (grep of its README/CLAUDE.md and `fli-core/src/flitools.ts` for tts/speech/kokoro: no hits), so this is a new verb there.

## 6. Cleanup policy — and does cleanup actually run today?

**What exists:** `-renders/` is declared a cache, shown with its size (amber over 500 MB, hidden under 1 MB; `renders.ts:46-50`), and `clearRenders` removes it **only when a person runs it with `confirm: true`** (`server/src/capabilities/renders.ts`; UI in `client/src/components/Renders.tsx`, whose own copy says "keep it until the video is published, then clear it **from the project**"). `-trash/` is the same: shown, emptied on request (`empty-trash.ts`).

**What I found for automatic cleanup: nothing.** No timers, cron, launchd job, retention/TTL, or publish-triggered clear in `flistudio/server/src` (searched for `setInterval`, `cron`, `prune`, `sweep`, `retention`; the only `setInterval` hit is a comment in `requestLogger.ts`). So **the existing cleanup is manual, and "cleared once the video is published" is a policy sentence, not a running job.** Absence caveat: I searched the source with text patterns; a job in another repo (FliTools `launchd/`, FliHub) was not checked.

**Proposed policy for audio (two layers):**
1. **In-tool orphan GC (new, small, owned by Story Pilot):** after each (re)generation, delete any `p*-<hash>.mp3` in `audio/` that no manifest row references. A one-paragraph edit leaves exactly one file behind for a moment, never a pile. This is the part that makes "files get cleaned up over time" true without waiting for a human.
2. **Project-level (existing, manual):** the whole `-renders/storypilot/` is a normal `-renders` tool folder; `clear-renders` removes it. Missing audio just shows as "not generated" with a Generate button. Nothing breaks.
3. **Optional later, FliStudio lane:** clear `-renders/` automatically when the video's resource is marked `published`. This would fix *all* render caches, not just audio; it is a behaviour change to an existing contract, so it needs David's call and is **out of scope** for Listen.

Size reality: ~6 min of script ≈ 6 MB as mp3, under the 1 MB display threshold only when tiny. It will show; it won't hurt.

## 7. Player UX (mock)

Closed (script, no playback; each paragraph has a small speaker glyph):
```
┌ Script ─────────────────────────────────────  ▶ Listen  [auto-next ●] ┐
│ 01 ◔ My girlfriend Joy is not a content creator. She's a nail artist…  │
│ 02 ◔ And it turns out she's bloody good at it. …                       │
│ 03 ◔ But her videos don't get published. …                             │
└──── 17 paragraphs · audio 17/17 ready · 5:48 · voice af_heart ─────────┘
```
Playing (paragraph 02; the focus/contrast treatment storypilot-dev is restoring; others dimmed):
```
│ 01 ✓ (dim) My girlfriend Joy is not a content creator…                 │
│ 02 ▶ AND IT TURNS OUT SHE'S BLOODY GOOD AT IT. She'll do a video in    │  ← full contrast, highlighted
│      one take, forty-five seconds…                       0:14 / 0:31   │
│ 03 ◔ (dim) But her videos don't get published…                         │
├ ⏮  ⏯  ⏭   ━━━━━━●━━━━━━━━━━  0:44 / 5:48   speed 1.0×  auto-next ● ┤
```
Stale paragraph (words edited after audio was made):
```
│ 07 ⚠ one day, autopilot … (edited)   audio out of date  [Regenerate] │
│      – plays the OLD audio, greyed, until regenerated –              │
```
Behaviour (copied from FliHub): single `<audio>`; on `ended`, if auto-next is on, load the next paragraph and play (`flihub/client/src/components/WatchPage.tsx:588-591` → `playNextSegment` at L393-410; the toggle persists in `localStorage` key `flihub:watch:autonext`, L62/L223/L354-358). Story Pilot uses a `storypilot:listen:autonext` key. Click a paragraph = play from there. Preload the next file to avoid a gap. Stale paragraphs are **skipped or played** per a setting; default: play, because David wants to hear the draft even when slightly behind.

## 8. Which repo / lane owns each piece

| Piece | Repo | Lane |
|---|---|---|
| Player bar, per-paragraph states, auto-next, stale/regenerate buttons | `flistudio/modules/storypilot/client/` | storypilot-dev (already restoring the focus/contrast treatment) |
| Manifest, hashing, staleness, orphan GC, `story.audio.status/generate` RPCs | `flistudio/modules/storypilot/server/` + `shared/` | storypilot-dev |
| Speech synthesis (Kokoro, voices, "not installed here") | `flivideo/flitools` | FliTools lane — **new verb** |
| Serving an `-renders/…mp3` file to the browser | `flistudio/server` | FliStudio core — **unverified** how project files are served to the client today; check before building |
| `rendersPath`, `-renders` zone, clear verb | `fli-core` + `flistudio/server` | already exist; **no fli-core change needed** |
| Clear-on-publish (optional) | `flistudio/server` | FliStudio core, needs David's call |

**Touches the shared `fli-core` contract: no.** Everything lives in the module's own state plus the existing renders convention.

## 9. Where I disagree with orch's take

1. **Unit.** Orch/David said chapters; Story Pilot has none. Use **paragraph**; chapter = optional play-range later.
2. **"Generated automatically when first written"** — agree, but as a *background* job with visible progress, never blocking the write RPC; and **only if FliTools reports TTS available**. Otherwise show "Generate audio" with the reason, not a silent failure.
3. **Who runs it.** Orch's note points at the `kokoro-tts` skill. A skill is an agent convenience (Apple-Silicon venv on whichever machine); the app needs a service. → FliTools verb. Story Pilot must not shell out to Python.
4. **"Cleaned up like -renders / trash."** That cleanup is **manual today** (section 6). If the design says "it's a cache, it gets cleaned", it's misleading unless we add the orphan GC (cheap, ours) and decide separately on clear-on-publish.
5. Minor: keying by hash alone isn't enough if the hash is positional; match by hash, then index (section 3).

## 10. Not verified

- Kokoro speed on the machine that would run it (I did not run it); "real-time-factor" claims are none.
- How FliStudio serves project files (audio streaming, range requests) to the client.
- That FliTools has no TTS: only a grep of three files, not its `src/` tree or `launchd/`.
- That no cleanup job exists anywhere in the fleet (FliTools `launchd/`, FliHub, brain scripts not searched).
- Whether `story.script.set` is the one place a script is "first written" (other paths: `door-log.ts`, direct file edits by agents); needs a read of `modules/storypilot/server/story.ts`.
- The focus/contrast treatment: taken from orch's message, not seen.
- Exact FliHub segment-end behaviour beyond the lines cited (`WatchPage.tsx` is 968 lines; read only the grep hits).
