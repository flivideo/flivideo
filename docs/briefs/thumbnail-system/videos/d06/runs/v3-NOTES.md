# d06 v3 runs (2026-09-27)

- B4 106 of me / B5 casting call / B6 face filing cabinet: v3 briefs, **style reference board attached**, refs from David's favourites. The light show is gone and they read like the board.
- B5 compact: the same idea as ONE ~2.3k-char JSON (`scenes/d06-b5-casting-call.prompt.json`) pasted directly. Result as good as or better than the long brief. **This is the method now.**
- Compositor now auto-picks the calmest zone and fits the text. Gap: no 2-line wrap yet, so B6's headline came out small (62px, under the 64 minimum).
- Chats: b4 6ab8b589-fb6c-83ec-8b37-80af447c9939 · b5 6ab8b58d-b7cc-83ec-8c8c-2ce8b05dfd18 · b6 6ab8b591-112c-83ec-8345-f5f27c0ed51f · b5-compact 6ab8b719-8088-83ec-ab63-89d247153612

## Ideas 1 + 3 re-made with the compact pipeline (13:4x)
- a1 6ab8b888-e8a0-83ec-acac-4e5985c230a2, a3 6ab8b88c-1148-83ec-a8ee-9d44920dad8c. Scene files `scenes/d06-a1-ai-picked-this.json`, `scenes/d06-a3-thumbnail-machine.json`.
- Board style held with no light show. In a3, ChatGPT added a thumbnail-within-a-thumbnail (a YouTube card), which is a nice touch.
- Compositor: added 2-line wrap and `--pill` (brown AppyDave panel). Auto zone fails on plain surfaces (a shirt reads as "calm"), so named zone + pill is the reliable mode.
- `d06-selection-board-all6.png` = all six ideas.
