---
created: 2026-11-05
timestamp: 2026-11-05T16:20+07:00
---
# Brief: hosted voice inference as a cost alternative to ElevenLabs (M2 worker, research only)

**Owner**: flivideo-orch (M4). **David's ask**: 2026-11-05. **Machine**: M2. **Folder**: `~/dev/labs/voice-hosted-research/`, new, own `git init`, no remote.

## The question
Can VoxCPM2 or comparable voice-cloning models run through SaaS or API inference providers, and is that cheaper than ElevenLabs?

## Cover, for each provider and model you find
Who hosts VoxCPM2; who hosts comparable cloning-capable models; price per 1,000 words and for a D13-length script (1,049 words, 5,598 characters by `wc -c`; state your conversion when a provider prices by seconds or by compute time); speed; whether voice cloning is supported and how; word timings; limits on text length; licence of the model and the provider's commercial terms; what happens to an uploaded voice sample (retention, training use, deletion), quoted from their terms.

## Compare with
- **ElevenLabs** at its current published prices, including how plans and credits turn into a cost for 1,049 words.
- **Local M2 run** (measured 2026-11-05, 202-word script, VoxCPM2 8-bit via mlx-audio, Apache-2.0 + MIT): 0.87x to 0.99x real time, about 6 GB peak line by line, 11.9 GB in one piece; 3.5 GB disk; no per-use fee. D13 is untested.

## Evidence rules
- Current primary sources only: pricing pages, model cards, licence files, provider terms. Put a check date on every figure.
- Mark anything unverified. If a price needs a login to see, say so. A blog or comparison site is a lead, not a source.
- Don't extrapolate quality from provider marketing. No listening has happened, so quality stays "not established".
- Say what you looked for and didn't find. "No provider found" means none in the places you searched, listed.

## Rules
No paid calls, no accounts, no API keys, no signups. Upload no audio. Use no voice sample of David's and read none. Don't touch `~/dev/labs/voice-poc/`, any FliVideo app or the ElevenLabs integration. Nothing global, no `sudo`. Use `command grep`.

Keep the report about models and providers. Don't mention which voices or tools any of our channels have used.

## Deliverables, in the folder
- `REPORT.md`: comparison table, sources with dates, not established, and **one recommendation**.
- `page/index.html`: light-only AppyDave page (cream `#faf5ec`, white cards, `#342d2d` text, Oswald + Roboto, `color-scheme: light`, no `prefers-color-scheme`, no dark theme). Verdict first, then one table David can read at a glance, then sources. Orch publishes it.

Commit locally. End with exactly one line: `APPYNET: done — <one line>`, `APPYNET: blocked — <why>` or `APPYNET: question — <a real decision>`. Never for status.
