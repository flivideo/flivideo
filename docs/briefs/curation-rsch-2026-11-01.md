---
created: 2026-11-01
---
# Brief: `curation-rsch` — what already curates sessions, captures and dossiers

**From:** `flivideo-orch`. **To:** `curation-rsch` (tmux `curation-rsch`). Read `/Users/davidcruwys/dev/ad/flivideo/docs/briefs/_curation-quotes.md` first: David's words, context and rules.

## Do

1. **First**, run the full skill inventory (mandatory before claiming any skill is missing):
   `find ~/.claude ~/.agents ~/dev/ad ~/dev/agents ~/dev/clients -name "SKILL.md" -not -path "*/node_modules/*" 2>/dev/null`
   That counts files, not skills (many are cached/build copies); dedupe to the live `~/dev/ad/appydave-plugins/<plugin>/skills/*/SKILL.md` where both exist.
2. Find every skill and pattern that **reviews, synthesises or curates** sessions, captures, dossiers, conversations or sources: e.g. `captains-log:dossier`, `captains-log:keeper`, `sesh:session-archaeology`, `appydave:lisa`, `steno:*`, `writers-room:*`, `flivideo:storypilot`, `abridge`, anything Story Pilot already calls. Also non-skill patterns in Story Pilot / FliStudio code (how a source becomes SYNTH vs RAW today; `storypilot.story`).
3. For each: what it does (one line), its input and output, **whether it handles staleness** (does it record what source state it was built from? can it tell its output is out of date?), whether it **places or orders** material, and **whether Story Pilot could call it** (agent-only skill vs something an app can trigger).

## Deliver

`/Users/davidcruwys/dev/ad/flivideo/docs/specs/curation-inventory-2026-11-01.md`: a table (skill · plugin · does · staleness? · places/orders? · callable from Story Pilot?), then gaps, then your recommendation on which existing pieces a single Story Pilot curation skill should reuse vs replace. Note the placement rule: new skills go in a domain plugin (flivideo), never the legacy `appydave` plugin. Commit + push, report to `flivideo-orch`, stop.
