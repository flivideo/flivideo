# Runbook — a transcript looks wrong: how to tell, how to redo it

**Purpose**: anyone can spot a bad transcript and get a good one without David.

**For agents**:
- FliHub shows `T⚠` on a recording, or FliCut shows `⚠ transcript health` on a recording header
- the words in FliCut or the transcript don't match what was said, words appear twice, or a take plays backwards
- you need to know when to stop and ask

---

## 1 · How to tell

Look at the **T** badge on the recording's row in FliHub (Recordings view, next to the filename).

| You see | Means | Do |
|---|---|---|
| green **T** | FliTools checked it and found nothing wrong | nothing |
| amber **T** (pulsing) | transcribing now | wait |
| amber **HQ…** next to the T | the fast transcript is in; the high-quality pass (CrisperWhisper on the M2) is still running | wait. A toast says "high-quality transcript has landed" when it's done |
| **amber T⚠** | OK, but FliTools repaired something itself. Hover to see what, e.g. "repaired automatically: transcriber duplicated 41.7–49.5s; the 29 repeated words were dropped" | check the cut around those seconds in FliCut (step 4) |
| **red T⚠** | suspect: still bad after FliTools' one automatic retry. Hover for the reason | redo it (step 2) |

Hover text you may see on a red T⚠:

- **text repeated: transcriber duplicated 40–50s (N words go back in time)**: the same stretch of audio has two sets
  of words. This is the CrisperWhisper chunk-overlap bug (D10, 2026-10-12). FliTools now drops the duplicate
  automatically, so a red one means the transcript was made before that fix, or by some other route.
- **longest repeated run / repetition share / compression ratio**: Whisper looped (the same line over and over).
- **segment(s) start past the media's end / end past the media's end**: invented text after the audio ends.
- **folded-word / unexplained-speech** (high-quality pass only): a word swallowed a phrase, or speech has no words on it.
- **prompt-echo**: the word list was written back as if it had been spoken.

The tooltip also says which pass is on disk: "fast transcript (pass 1)" or "high-quality transcript (pass 2,
crisperwhisper)". Edit with pass 2.

## 2 · Redo it (one recording)

1. In FliHub's Recordings view, click **↻** right of the recording's **T**.
2. Confirm. The old transcript is kept: it goes to `hub/transcripts/engines/` and `-trash/`.
3. The T pulses amber (fast pass, about a minute), then shows **HQ…** (high-quality pass on the M2, a few minutes).
4. When the toast says **"high-quality transcript has landed"**, hover the T. It should be green, or amber with a
   repair note, and say pass 2.

**No button? (an agent, or FliHub's UI is not to hand.)** Use the API:

```
curl -s -X POST localhost:5101/api/transcriptions/queue -H 'content-type: application/json' \
  -d '{"videoPath":"/Users/davidcruwys/dev/video-projects/<brand>/<project>/hub/recordings/<name>.mov","force":true}'
curl -s localhost:5101/api/transcriptions/status/<name>.mov   # pass, pass2Pending, health
```

⚠️ Manage → Regen Transcripts does **not** redo a transcript that is already fresh, because it never sends `force`.
Use ↻ instead.

## 3 · Check it yourself (optional)

Count the words that go back in time (0 = clean):

```
python3 -c "import json,sys;ws=json.load(open(sys.argv[1]))['words'];h=-1e9;n=0
for w in ws: n+=w['start']<h-0.05; h=max(h,w['end'])
print(n)" /Users/davidcruwys/dev/video-projects/<brand>/<project>/hub/transcripts/<name>.json
```

## 4 · FliCut: the edit still has the old words

FliCut copies the words into the edit when a recording is first transcribed, so a FliHub redo does **not** change an
existing cut. FliCut shows **⚠ transcript health: text repeated…** on the recording header when its own words go back
in time.

**FliCut cannot reload one recording yet.** It has no button, verb or command for it, and reopening the project does
not do it either. Ticket with done-condition: `/Users/davidcruwys/dev/ad/flivideo/docs/briefs/flicut-reload-one-recording.md`.
Until it is built:

- **The cut has not started** (no decisions worth keeping): make a new cut. It picks up the redone transcripts.
- **The cut has decisions:** do not hand-edit `fli.cut.*.json`. Escalate (step 5).
- Never touch `fli.edit.*` files.

## 5 · When to escalate (ask David, through the orchestrator)

- It is still red after one redo.
- The redo stays on **HQ…** for more than 20 minutes. The M2 worker may be down or on old code: run
  `/Users/davidcruwys/dev/ad/flivideo/flitools/scripts/deploy-worker.sh` from the M4. It refuses if busy and prints
  both commits.
- A recording with cut decisions needs its FliCut words replaced (step 4).
- Many recordings in one project go red at once. That points to a FliTools regression, not a recording: check
  `~/Library/Logs/flitools/stdout.log` for "suspect … retrying once".

## Where things live

- **FliTools** owns the health check: `/Users/davidcruwys/dev/ad/flivideo/flitools/src/transcribe/transcript.ts`
  (`transcriptHealth`, `wordsBackInTime`, `withTimeOrder`). The duplicate drop is in `src/transcribe/crisper.ts`
  (`dropRewoundWords`).
- **FliHub** handles the badge and redo: `client/src/utils/transcriptHealth.ts` and `client/src/components/RecordingsView.tsx`
  (`TranscriptionBadge`).
- **FliCut** shows the warning: `src/shared/transcript-warning.ts` and `src/renderer/src/Script.tsx`.
