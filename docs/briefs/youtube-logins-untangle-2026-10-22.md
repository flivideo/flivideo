# YouTube logins — untangle brief (pick up 2026-10-22)

**Purpose**: David finds the brand ↔ Google account ↔ YouTube channel mapping in FliStudio "incredibly confusing" (2026-10-21) and wants every mismatch fixed. This is the state at end of 2026-10-21 and the work list for the next session.

**Written by**: session `aitldr-growth-rsch` (M4 Mini), 2026-10-21. Facts marked **checked** were reached live (read-only FliStudio calls); **inferred** ones were not.

## State at 2026-10-21 end of day

Tokens live in `/Users/davidcruwys/.config/flivideo/youtube-tokens/<brand>.json` (one per brand, mode 600; agents never read them). Sign-in command (David runs it himself, in iTerm2):

```bash
cd /Users/davidcruwys/dev/ad/flivideo/flistudio && npm run research:auth -- --brand <brand>
```

| FliStudio brand | Mirror channel id (checked) | Token saved | Token actually reaches | Reach jobs |
|---|---|---|---|---|
| `aitldr` | `UC8vD5DvNTh03eID8iOl07XQ` (AiTLDR) | 2026-10-07 11:45 | Analytics pull with `ids=channel==UC8vD5…` works (2026-10-19 pull). Reporting guard refuses it; the token's own channel looks like **@davidcruwys** (inferred from top video `tUe5QakWLnc`) | 2 jobs on the **personal channel**: `d1790797-5290-40bb-a930-566a34c883ef` (basic), `943c9887-64bc-4a1a-98f2-84cbcdd6d041` (combined), created 2026-10-21 11:36Z — left alone pending David |
| `appydave` | `UC3fDZp6BryiFmBzVChBTlNg` (AppyDave) | 2026-10-21 20:15 (local) | **Checked:** Analytics refuses `ids=channel==UC3fDZ…` (403, `wrong-channel`). Guard guesses AppyDave Labs (inferred) | none |
| `appydavelabs` | `UCLyscJVSp1l_V6gZg5F5wZg` (AppyDave Labs) | 2026-10-07 11:34 | **Checked:** passes the guard | `56c4cb60-ba98-4500-b395-194252b54e8f` (basic, 13:21:24Z), `d5f55d1e-2623-44a5-86ad-3c191ead3e48` (combined, 13:21:29Z). First reports ~2026-10-23 13:21Z |

Other facts:
- **AITLDR decision (David, 2026-10-21):** no API reach jobs for AITLDR. The AiTLDR channel is under his friend Daniel's Google account, so David can't pick it at sign-in. Impressions/CTR come from manual Studio exports. Keep the aitldr token, because the analytics pull needs it. Recorded in `/Users/davidcruwys/dev/aitldr/aitldr-brain/research/channel-growth-2026-10/findings/09-impressions-ctr.md`.
- **David's Brand Accounts** (screenshot, myaccount.google.com/brandaccounts) include **two named "AppyDave"**: one with a purple "A" avatar and one with David's photo. There is no "AppyDave Labs" entry. David picked the **photo** one on 2026-10-21 and is sure of it. **Inferred:** the photo "AppyDave" Brand Account owns the AppyDave Labs channel, and the purple "A" one owns the main AppyDave channel. Not yet confirmed.
- The others listed include 555Manifesto, AppyCast, FliVideo, IdeasMen and more. FliStudio only has the three brands above.
- The channel guard is FliStudio `f8cb003`, and it applies to `youtube.reporting.*` only. The Reporting API itself is enabled in Cloud project "FliVideo" (believed to be 229911379755).

## Work list for tomorrow

1. **Map the accounts (David, ~5 min):** click each "AppyDave" Brand Account on myaccount.google.com/brandaccounts and note which YouTube channel it holds. Optionally rename the Labs one to "AppyDave Labs" so the chooser stops lying. That's a Google account change, so David's call.
2. **Re-sign `appydave`** picking the right entry. Then run the read-only check `node bin/flistudio youtube.reporting.jobs --brand appydave --json`: it should list jobs or `[]`, not `wrong-channel`. Then flivideo-orch creates both reach jobs.
3. **Make sign-in say what it got (FliStudio fix, proposed):** after `research:auth`, immediately run the same channel check and print "this login reaches <channel title> (<id>)", or refuse to save the token on a mismatch. Today the mismatch only shows up later, inside a report call.
4. **Decide the stray personal-channel jobs** (`d1790797…`, `943c9887…`): delete them or keep them as @davidcruwys data.
5. **Optional:** a one-page "which login is which" table in FliStudio's README, so this never has to be rediscovered.

**Deadlines:** pull the AppyDave Labs backfill (and, once they exist, the AppyDave reports) within 30 days of their first availability, which for Labs means before about 2026-11-22. Every day `appydave` stays unsigned loses a day of its 30-day backfill.
