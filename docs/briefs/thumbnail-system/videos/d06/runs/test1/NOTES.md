# d06 fresh-chat test 1 (2026-09-27)

**Verdict: PASS on the core question.** A brand-new ChatGPT chat with no history, given only the brief file (`../../fresh-chat-test-1-prompt.md`) and 7 cutouts, produced a board-quality, on-brand thumbnail that follows the spec's layout.

- Chat: https://chatgpt.com/c/6ab895fb-3c70-83ec-8a46-e4612c6ebeb9 (Chat mode, no project). Caveat: ChatGPT's account-level memory may still be on. It was not checked, so "no history" means no chat history, not proven zero memory.
- The brief went in as an attached `.md`, not pasted text. The prompt was one line pointing at it.
- Faces: every face is a faithful copy of its cutout. c58's green eye look is in the original photo, not model drift (I briefly misread it as drift).
- The model didn't render the headline, as instructed. `tools/composite_headline.py` added "WHICH ME?" afterwards.
- Misses: no QC report from ChatGPT, and the hero slightly overlaps the CONFIDENT card.
- Files: `d06-a1-test1.png` (raw), `d06-a1-test1-final.png` (+ `-320` mobile check), `generation-record.json`, `d06-a1-test1-transcript.md` (includes ChatGPT's own caption of the image).
