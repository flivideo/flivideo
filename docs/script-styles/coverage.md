# Coverage — script-style library, text lane (2026-11-05)

Source rule (David, via orch): **AITLDR and AppyDave text comes from FliVideo's own stores/projects, not YouTube.** YouTube captions only for Maitis, Mike (OpenRig) and the two aitldr-old gap-fills.

| Style | Wanted | Found in FliVideo | YouTube captions used | Used for guides | Missing |
|---|---|---|---|---|---|
| aitldr-old (Series A, long) | 25 | 21 (store `transcript.txt`; none have scripts) | 2 (`d_YPcRVnAQM`, `sBJo4h1q_0E`; FliVideo kind=none) | 23 | 2 - gap, orch filling: `XJdxVmNyxmg`, `BA435LYtYho` |
| aitldr-new (Series B, long) | 27 | 26 (19 project incl. `a2EGJnOCpoA` b01 matched by title; 7 script-only incl. `8uypPWDhDs8` b04 and `P4c-XkAeJxI` b26 matched by title) | 0 | 22 scripts for section maps; 17 final transcripts for spoken measures; 5 script-only use spoken script lines | 1 - gap, orch filling: `q724ELdSywE` |
| aitldr-new (Series B, short) | 18 | 12 (10 project with short final transcript incl. `5r8dGfwSbjI` b05 matched by title, 2 script-only) | 0 | 11 measured in the guide + 1 checked after (`5r8dGfwSbjI`) | 6 - gap, orch filling: `UJXxVigGahk`, `iWGZOYoGU-w`, `fm1WrkZ9Bvk`, `6zAtQHHg6Io`, `aZjw4FzKZrM`, `Pi2Ggb2hWM4` |
| appydave (newest 25) | 25 | 25 (17 store transcripts, 8 videos from 5 projects as per-segment transcripts; no `script.md`) | 0 | 22 distinct recordings (3 d12 videos share one project, 2 more share another) | none |
| mike (OpenRig) | 3 (+3 short explainers measured) | 0 | 3 (+3 on disk from earlier batches) | 3 (6 for the verbal measures) | none |
| maitis (@maitis-ai) | 15 (channel has 16 long-form) | 0 | 15 fetched | 15 | 1 long-form not sampled; 31 Shorts not sampled |

## Notes
- The first fetch (before the ruling) pulled 22 aitldr-old YouTube auto-captions into `~/dev/upstream/tubescripts/aitldr/` (not deleted). They were **not** used as the source except for the two gap-fills above.
- Series B scripts (`script.md`, `short-script.md`) are planned text; final transcripts (`<name>-final.txt`) are spoken. Guides say which is which; spoken-rate numbers use finals only.
- `sources.json` first marked 11 aitldr-new and 4 aitldr-old rows `kind=none` (15). Orch then matched 4 aitldr-new rows by title (`matched: by title (orch), not linked in the project`): 8uypPWDhDs8, a2EGJnOCpoA, 5r8dGfwSbjI, P4c-XkAeJxI; 7 aitldr-new gaps remain (and 2 aitldr-old).
- 429s: the YouTube fetch was rate limited from the start (anonymous), `--cookies chrome` failed on this machine (keychain unreadable); the Maitis fetch succeeded at `--pace 45` after a cool-off.
- Not verified: wpm for Series B shorts that are script-only (excluded); AppyDave project wpm (segment files can't be split per video, excluded).
