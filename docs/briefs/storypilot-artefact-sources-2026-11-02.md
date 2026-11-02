---
created: 2026-11-02
timestamp: 2026-11-02T17:45+07:00
---
# Brief: claude.ai artefacts as Story Pilot sources, then register the rig-series artefacts on D19 (2026-11-02)

**From:** `flivideo-orch` (Swagger). **To:** `storypilot-dev`. Report to `flivideo-orch` by name.
**Go:** David, relayed from `roamy-home-orch` 17:35 (his words, 17:38 +07: "all the artefacts that we've been collecting
from Spaghetti Rig, AppyStack, and AppyTron … need to be available for that video"). He does not want to watch: run to done.

## Video
D19 = `/Users/davidcruwys/dev/video-projects/v-appydave/d19-spaghetti-rig` (rig series Spaghetti → AppyStack → AppyTron).
It already has `fli.resources.json` and 16 Story Pilot sources.

## Step 1 — find out (no code yet)
Can a FliStudio project already hold a claude.ai artefact link (`https://claude.ai/artifact/<id>`) as a **resource**
(`fli.resources.json`, `flivideo:flistudio` resource verbs) and/or a **Story Pilot source**, in a way that Story Pilot,
B-roll and Remotion graphics can read? Name the verbs/fields that exist. Write the answer in your report.

## Step 2 — only if the answer is no or partial
Smallest change that makes an artefact link a first-class source: kind `artefact` (url, title, origin repo path if known,
addedAt), shown as a card in Story Pilot that opens the URL. Reuse the existing resource contract; flag before touching
`fli-core` or any shared contract. Fresh branch from FliStudio main `d053b9c` (or later) in your worktree — never the live
checkout `/Users/davidcruwys/dev/ad/flivideo/flistudio`. Gates: typecheck, `npm test`, targeted storypilot e2e only (never the
full suite), schema mirror `mirror:check` if capabilities change. Report branch + commit; orch gates, merges, restarts.

## Step 3 — register on D19 (after orch merges, or now if no code was needed)
Register each as an artefact source/resource on D19 with a readable title:

| Title | URL |
|---|---|
| Spaghetti gate ladder | https://claude.ai/artifact/TaGLV3SmZwmJWPPCv9nNfp |
| AppyRig runsheet | https://claude.ai/artifact/2kYavV6EKgex7xQd1ynCST |
| Spaghetti validation pack | https://claude.ai/artifact/NeMVpSiv9iPenMNVqduYRp |
| AppyStack pack | https://claude.ai/artifact/ATv9e8swbb8VzA1AsW4MRm |
| AppyTron progress | https://claude.ai/artifact/67msrV1MQngU13ma3fgJXX |
| AppyTron validation pack | https://claude.ai/artifact/EFwNgMDFfzMLXydmhp9Ygk |

Plus every other artefact URL under `/Users/davidcruwys/dev/appyrigs/runs/` (spaghetti/*, ladder/appystack, ladder/appytron).
Orch's grep found six more: `B1VHG7nEABNEmR4GvpcJ5r`, `QiEZJ82dHpZzq7wnpAZAbm`, `NUsbtXJtsM3vfCwpqpt9HD`,
`LUraADXBeyWxmxDN2DvKdr`, `GMbxJcd1rZE5khkXsdgP4S`, `6ayzC4SfovoC8MdhLPTXEK` — title each from the file that cites it
(or the artifacts MCP `get_artifact`). Also register as file sources: each run's `WEIGH-UP.md` and `decisions-*.md`
(`runs/ladder/appystack/`, `runs/ladder/appytron/`, `runs/spaghetti/*`). A 13th artefact (the three-way comparison) arrives
from orch later: register it when sent.

No duplicates; idempotent re-runs. Do not touch D19's angle (David-only) or remove any existing source.

## Done means
- All of the above appear on D19 in Story Pilot in live FliStudio `http://localhost:7150`, in a real browser.
- Screenshot(s) saved to `/Users/davidcruwys/dev/ad/flivideo/docs/reports/proof-2026-11-02/d19-artefacts-*.png`.
- Report to `flivideo-orch`: step-1 answer, branch/commit (if any), count registered, screenshot paths, anything skipped.

## Limits
Story Pilot / resources only. Do not merge, do not restart FliStudio. Questions to `flivideo-orch` with a recommendation.
