# Coverage — script-style library, text lane (2026-11-05)

Source rule (David, via orch): **AITLDR and AppyDave text comes from FliVideo's own stores/projects, not YouTube.** YouTube captions directly for Maitis and Mike (OpenRig). The 13 rows FliVideo's store lacked (4 aitldr-old, 9 aitldr-new) were later filled into the FliVideo store from YouTube captions (sources.json note "filled from YouTube captions"); nothing is missing for aitldr now.

| Style | Wanted | Found in FliVideo | YouTube captions used | Used for guides | Missing |
|---|---|---|---|---|---|
| aitldr-old (Series A, long) | 25 | 21 (store `transcript.txt`; none have scripts) | 4 filled into the FliVideo store from YouTube captions (`d_YPcRVnAQM`, `sBJo4h1q_0E`, `XJdxVmNyxmg`, `BA435LYtYho`) | 25 | none |
| aitldr-new (Series B, long) | 27 | 27 (19 project incl. `a2EGJnOCpoA` b01 matched by title; 7 script-only incl. `8uypPWDhDs8` b04 and `P4c-XkAeJxI` b26 matched by title) | 1 filled from captions (`q724ELdSywE`, newest long, 2026-11-04) | 27 (22 scripts for section maps; 17 final transcripts for spoken measures; 5 script-only use spoken script lines; 1 caption) | none |
| aitldr-new (Series B, short) | 18 | 12 (10 project with short final transcript incl. `5r8dGfwSbjI` b05 matched by title, 2 script-only) | 6 filled from captions (`UJXxVigGahk`, `iWGZOYoGU-w`, `fm1WrkZ9Bvk`, `6zAtQHHg6Io`, `aZjw4FzKZrM`, `Pi2Ggb2hWM4`) - these are standalone showcase shorts, not the companion template | 18 (12 companion, 6 standalone) | none |
| appydave (newest 25) | 25 | 25 (17 store transcripts, 8 videos from 5 projects as per-segment transcripts; no `script.md`) | 0 | 22 distinct recordings (3 d12 videos share one project, 2 more share another) | none |
| mike (OpenRig) | 3 (+3 short explainers measured) | 0 | 3 (+3 on disk from earlier batches) | 3 (6 for the verbal measures) | none |
| maitis (@maitis-ai) | 15 (channel has 16 long-form) | 0 | 15 fetched | 15 | 1 long-form not sampled; 31 Shorts not sampled |

## Notes
- The first fetch (before the ruling) pulled 22 aitldr-old YouTube auto-captions into `~/dev/upstream/tubescripts/aitldr/` (not deleted). The 4 that FliVideo lacked are now in its store; the other 18 were not used (FliVideo's copies were).
- Series B scripts (`script.md`, `short-script.md`) are planned text; final transcripts (`<name>-final.txt`) are spoken. Guides say which is which; spoken-rate numbers use finals only.
- `sources.json` first marked 11 aitldr-new and 4 aitldr-old rows `kind=none` (15). Orch then matched 4 aitldr-new rows by title (`matched: by title (orch), not linked in the project`): 8uypPWDhDs8, a2EGJnOCpoA, 5r8dGfwSbjI, P4c-XkAeJxI, and filled the remaining 11 aitldr-new and 4 aitldr-old rows from YouTube captions (the 4 old rows include the two I had fetched). The guides were updated for these: aitldr-old now n=25; aitldr-new notes the newest long video ends with the Series A sign-off and that 6 shorts are standalone showcases.
- 429s: the YouTube fetch was rate limited from the start (anonymous), `--cookies chrome` failed on this machine (keychain unreadable); the Maitis fetch succeeded at `--pace 45` after a cool-off.
- Not verified: wpm for Series B shorts that are script-only (excluded); AppyDave project wpm (segment files can't be split per video, excluded).
