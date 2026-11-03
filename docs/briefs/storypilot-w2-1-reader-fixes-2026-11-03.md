---
created: 2026-11-03
timestamp: 2026-11-03T22:10+07:00
---
# Brief: W2.1 — three Reader defects found on the live d13 screenshots (2026-11-03)

**From:** `flivideo-orch`. **To:** `storypilot-w1-dev` (**M2**, code). Branch `storypilot-w2-1` off origin/main (`c827c92`+).
Evidence: `/Users/davidcruwys/dev/ad/flivideo/docs/reports/proof-2026-11-03/w2-reader-3-spec.png` and `w2-reader-4-send.png`.

1. **Spec card "File" row is empty** (label + `>_` only). The source card on the left shows `file overlay-pilot/spec.md`, so the
   Reader has the path but doesn't render it. Note: on the M4 `d13-overlay-pilot/overlay-pilot/spec.md` does not exist at that
   relative path — show the stored path anyway, and mark it "not on this machine" when it can't be found (don't hide the row).
2. **Bullets cut mid-sentence**: "…Overlay Studio, which will" / next bullet "be later" ; "…the name of whatever we show in the" ;
   "…visual interface and". Looks like hard-wrapped markdown continuation lines being split into separate bullets (or an
   excerpt cut per line). Render a wrapped list item as one item. Also a raw `~~…~~` strikethrough shows as literal tildes —
   render it as strikethrough.
3. **The open Send-to-session popover covers the Reader header** (tabs, M/L/×). It must not cover the panel chrome: open it
   below its trigger inside the content area, or push content, per the brand rule (panels push, never overlay).

Tests: a unit test per defect (a wrapped bullet stays one item; `~~x~~` renders as `<s>`/`<del>`; the File row shows a stored path
and the "not on this machine" state), and an e2e assertion that the Send popover's box doesn't intersect the Reader's tab bar.
Gate: typecheck + full unit + every storypilot spec (CL stub enforced). Push the branch, write a short report into
`/Users/davidcruwys/dev/ad/flivideo/docs/reports/storypilot-w2-1-report-2026-11-03.md`, STOP. Orch re-gates on the M4.
