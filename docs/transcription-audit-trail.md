---
created: 2026-10-05
status: design for David's review (robustness phase 2, write-up 8). Nothing is built from this yet.
owner: flitools
brief: /Users/davidcruwys/dev/ad/flivideo/docs/briefs/transcription-robustness-2026-10-05.md
related: /Users/davidcruwys/dev/ad/flivideo/docs/post-transcription-rules.md
---

# One audit trail for every transcription decision

**The problem.** David: *"there's no unified decision on how we got to that final output… a transient audit log for
this tied to the transcriptions allows us to learn."* Today a take's history is spread over eight places in three
formats, and some decisions leave no record at all:

| Decision | Where it is recorded today | Gap |
|---|---|---|
| Each engine run (engine, model, seconds) | `engine` on each `engines/<base>.<slug>.json` | `engine.worker {name, commit}` only since step 1; d02–d06 copies have none |
| Word list sent | `engine.vocabulary` | — |
| Best-engine choice | the queue job's `note` (`~/Library/Application Support/flitools/queue/edit/<id>.json`) | **not in the transcript**; the queue file is machine-local and pruned |
| Retry on the other engine | `health.attempts`, `health.retried` | — |
| Silence drop | `health.droppedInSilence` | — |
| Ends cut back to speech energy | `health.clampedWords` | — |
| Folded word spliced from pass 1 | `health.spliced` | — |
| Filler replaced by Whisper's word | `health.wordsFromWhisper` | — |
| Levelling (name, gap, loop) | `health.levelled` | — |
| Project codes (D06) | **nothing**: `codes.ts` rewrites the words silently | gap |
| Rules (16:9, Skool) | `health.rules` (phase 2) | — |
| Word-store spelling on SRT/TXT | **nothing**: applied at render time | gap |
| Caption cues (which words make which cue) | **nothing** | gap |
| Project-level effect | `scorecard.json` history | per project, not per decision |

So "why does the SRT say X at 01:23?" means reading the transcript JSON, both engine copies, the queue folder, the word
store and the code. That is the scratchiness David means.

## The design: two layers

```
 engines/<base>.<slug>.json  ──┐   (durable: what each engine heard; never rewritten)
 word store (3 levels)       ──┼──▶ replay the stages ──▶  decisions[] on the transcript   (durable, small: changes only)
 FliTools code @ commit      ──┘                     └──▶  <base>.why.json                 (TRANSIENT: everything,
                                                                                            delete any time)
```

### Layer 1: `decisions[]` on the transcript (durable, changes only)
One array, one record shape, in pipeline order. It replaces the six health arrays that record changes, and adds the
three stages that record nothing today.

```jsonc
{ "seq": 7, "stage": "levelling", "kind": "name",          // stage ∈ engine | choose | retry | silence | clamp |
  "at": 29.04, "to": 29.68,                                  //   splice | whisper-words | levelling | codes | rules
  "before": ["Kybernetics."], "after": ["Kybernesis."],
  "why": "mlx-flihub heard the word-list name at the same place",
  "evidence": { "engines": { "crisper": "Kybernetics.", "mlx-flihub": "Kybernesis" } },
  "by": { "provider": "deterministic", "code": "levelling.ts@c3c0811" },
  "state": "auto" }                                          // auto | review | confirmed | rejected
```

- **Folds in:** `health.droppedInSilence`, `clampedWords`, `spliced`, `wordsFromWhisper`, `levelled`, `rules`. They stay
  readable for one version while readers move over. FliHub's `readTranscriptHealth` reads only `suspect` and `reasons`,
  which do not move.
- **Added:** the best-engine choice (`stage: "choose"`, with the reason now in the queue note), each engine run
  (`stage: "engine"`: worker, commit, vocabulary, seconds), and the codes rule.
- **Size:** d01–d06 record 0–4 changes per take (most: d02 06-1), about 200 bytes each, so under 2 KB on a 40–56 KB transcript.
- **The scorecard reads this layer.** `restored`, `levelled` and `rulesApplied` become counts over `decisions[]` by
  stage, so the scorecard and the trail cannot disagree.

### Layer 2: `<base>.why.json` (transient, everything)
The full replay of one take. Built on demand by a new verb, `transcribe.explain { recording, at? }`, which re-runs the
deterministic stages from the engine copies (no transcription, no model) and writes down every step:

- every engine's words at each place where they differ (not only where something changed);
- every rule or vote that was **considered but did not fire**, and why (e.g. "skill: no context word within 3");
- word-store spelling hits at render time (find → write, with which level: global, brand or project);
- the caption cue map: cue number, time, and the word ids in it, so an SRT line leads straight back to its words.

**Where it lives:** `~/Library/Application Support/flitools/why/<project-code>/<base>.json`, on the machine that runs
FliTools. It is never committed and never synced. **Size:** estimated at 10–30 KB per take (the cue map plus the
differences), so about 1 MB for a 40-take project. **Transient by design:** delete the folder at any time;
`transcribe.explain` rebuilds a take in under a second, because every input is durable (engine copies, the word store,
the code at a commit). If the code has moved on since the transcript was made, the replay says so
(`replayedAt: <commit>` vs `madeAt: <commit>`) and shows both answers.

**Why not keep it in the brand repo:** it changes on every replay and would churn git for nothing. Layer 1 is the part
worth keeping, and it is already committed with the transcript.

## Worked example: d02 06-1-outro (real data, 2026-10-05)

**Question:** "Why does the SRT say *Kybernesis This is a company…* at 00:28, run together?" (This was true until
c3c0811.)

**One read of `06-1-outro.why.json`, the decision part:**
```text
seq stage          at      before              after          why / evidence                                   by
1   engine         –       –                   –              crisperwhisper on mac-mini-m2, 24.5 s, no vocab;  crisper.ts (worker commit
                                                              worker commit NOT RECORDED (ran before step 1)    missing → shows the gap)
2   engine         –       –                   –              mlx-flihub: FliHub's own whisper, kept as a copy  —
3   choose         –       –                   crisperwhisper "the only transcript" (FliHub's plain file was    queue 10b12a86,
                                                              replaced), 2026-10-05T01:44Z                      backfill
4   whisper-words  26.96   [UH]                AI             mlx-flihub heard "AI" over crisper's filler      whisperWords.ts
5   levelling      29.04   Kybernetics.        Kybernesis     mlx-flihub heard the word-list name here;         levelling.ts@6bfebcb
                                                              ⚠ the spine's "." was dropped
6   rules          33.68   school              Skool          context: "community" within 3; Skool in the list  rules.ts@b35b21d (review)
7   rules          36.6    school              Skool          context: "community" within 3                     rules.ts@b35b21d (review)
render  cue 8 00:28.00–00:31.75 = words 54–66: "then come and check out Kybernesis This / is a company…"
```

**Answer in one read:** seq 5. Levelling took mlx's "Kybernesis" (no full stop) in place of CrisperWhisper's
"Kybernetics.", so the cue builder saw no sentence end and ran on. **Where to fix:** `levelling.ts`, the name branch.
That is the fix made in c3c0811 (keep the spine's punctuation); d02 03-1 "cutting," → "Cutty" had the same defect.
The trail turned "the SRT looks wrong" into a file and a line. Without it, the same answer took reading three files.

**d01 03-1-flistudio:** "Why does it say 16:9 at 00:19?" → `rules, format:16:9, before ["69"], trigger "format",
state review` (David can confirm or reject it).

## What the trail must record so a classifier can be compared later (link to write-up 9)
- **Every candidate, not only changes:** each place a rule or provider looked at, with its inputs (the words around it,
  each engine's word there, times, confidences) and its answer, including "no change". Without the negatives,
  precision can't be measured.
- **Provider and version** on every record (`deterministic@<commit>`, later `classifier:<model>@<version>`), plus a
  `confidence` (1.0 for deterministic rules).
- **David's verdict** (`confirmed` / `rejected`) joined to the record it judged. That is the labelled set a classifier
  is scored against.
- The transient layer holds the candidates; only the verdicts need to be durable (Layer 1 `state`, or a review log
  beside the word store).

## Not decided (David)
1. Whether `transcribe.explain` also renders a short human page (FliStudio) or stays JSON for Claude.
2. Whether the old health arrays are dropped after one version, or kept for good beside `decisions[]`.

**Recommendation:** build Layer 1 first. It is a refactor of fields that already exist, plus three missing stages
(choose, codes, engine runs). `transcribe.explain` (Layer 2) follows, and the scorecard moves to read `decisions[]`.
