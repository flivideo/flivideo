# StoryPilot — launch brief (FliStudio extension #2)

**Purpose**: Start StoryPilot, FliStudio's second extension. This session writes its spec and then, on David's go, builds it on `@flivideo/extension-core`.

**For Agents**:
- Read this in full before anything else. It is self-contained; you have no access to the session that wrote it.
- Work happens in a FliStudio git worktree. Never edit the live checkout `/Users/davidcruwys/dev/ad/flivideo/flistudio`.
- Written 2026-10-30 by `flivideo-arch-rsch`. Extension architecture is owned by `flivideo-orch`, which coordinates merges and restarts.

## 1 · What StoryPilot is (David's own words are the authority)

Read both sources in full before writing anything:

- **B670**: the ChatGPT dossier "Working Dossier — My Videos Suck / Story Pilot" (51 sections). It is David's thinking, reconstructed from the conversation.
- **B667**: the raw voice log of the same session (Plaud, 2026-10-29 07:04). Where it differs from B670, B667 wins: it is what he said.

Fetch both through Captain's Log, with the `captains-log:find` skill or the `captains-log` MCP `capture_get` (code `B670`, `B667`). The B670 brief is on the M2 at `~/dev/raw-intake/chatgpt/briefs/2026-10-29-story-pilot-my-videos-suck.md`.

The short version, so you know what you are looking for (do not build from this summary):

- StoryPilot turns a video's source material into a **script David can narrate in his own voice**. The material is Claude Code sessions and his spoken notes, ordered and labelled. The script has a real story spine, with tension and resolution, and no invented drama.
- **It is not a chatbot.** FliStudio holds the state:
  - creator, brand and video settings, with defaults and overrides;
  - the ordered source references;
  - the current script.

  Claude Code does the thinking over JSON-RPC ("we're working on D13") and writes the script back.
- What the viewer should feel and do is set per video or series, never baked in.
- **V1 leaves out** revision history, state management between drafts, an in-app chat and B-roll capture.
- **First real test:** the script for the Overlay Pilot video.

## 2 · Rulings already made (don't re-open them)

- **It is an extension, built on `@flivideo/extension-core`** (merged in FliStudio `1e89742`). The contract and rules are in FliStudio `docs/AGENT-NOTES.md` § "Modules" and `extension-core/README.md`. The design is in `/Users/davidcruwys/dev/ad/flivideo/docs/architecture-review-2026-10-29.md` §5.
  - Registering it touches only its own `modules/storypilot/` folder, the root `workspaces` entry, and one line in each of `shared/src/extensions.ts`, `server/src/extensions.ts` and `client/src/extensions.ts`. Then the counted capability lists, the spec table and `npm run api:openrpc`, as for any new verb.
  - **If you need any other host edit, stop and report it.** That means the contract has a gap, and the gap is not yours to patch.
- **Getting the script to Teletubby:**
  - StoryPilot never writes `fli.tubby.json`. That file is Teletubby's, and the rule is that only the app that owns a file writes it.
  - V1 hands the script over through **Teletubby's own agent API**, its control surface on :7111, which already reads and writes scripts.
  - fli-core names where shared files live. The app that owns a file decides its contents.
  - If Teletubby's API can't accept what StoryPilot produces, record that as a gap. Don't work around it.
- **The JSON-RPC door is the product surface.** Every StoryPilot state change is a capability that an agent can call. The screen is a view over the same capabilities.
- **Namespace:** `story.*` is suggested. Check it isn't reserved.
- **Stage:** `script`. The link appears in the Script box of the pipeline strip.

## 2a · How it fits FliStudio (addendum, 2026-10-30 10:45; settle each one in the spec)

- **Name on screen.** David's working name is "StoryPilot". Propose the `label` (it appears in the rail's Extensions group, as the "StoryPilot ›" link in the Script box, and as the screen title) and confirm it with David. Key `storypilot`, view `ext:storypilot`.
- **Sources already exist as video resources. Reuse them; don't invent a second list.**
  - FliStudio's `fli.resources.json` already has a `session` resource kind (audience `internal`).
  - Claude Code conversations attach to a video with the `flivideo:flistudio` skill's "attach this conversation to the video" recipe (`attach_session.py`).
  - ChatGPT conversations attach the same way, with `meta.tool: "chatgpt"` and `conversation_id`.
  - Read `~/dev/ad/appydave-plugins/flivideo/skills/flistudio/SKILL.md` § "Video resources" and `/Users/davidcruwys/dev/ad/flivideo/docs/briefs/video-resources-model.md`.
  - StoryPilot's job is the **order and labels** over those resources, plus spoken notes. If notes need a new resource kind, propose it as data (`resources.kinds`), not code.
- **Unit:** a **video** inside a project, as for Launch and resources. Say what happens for a project with several videos.
- **Script stage.** The Script box already shows Teletubby. Decide how StoryPilot's link and Teletubby's dot sit together, and what the box's fact line says once a script exists (e.g. "script · 1,240 words"). The page reads that from disk; it never calls the extension.
- **Agent entry.** "We're working on D13" must work. Name the first verb an agent calls (a `query` returning everything needed to write the script), and say whether the `flivideo:flistudio` skill or a new skill documents the flow.

## 3 · Order of work

1. Read B667 and B670 in full. Read FliStudio's extension contract (§2), and Overlay Pilot at `modules/overlay-pilot/` as the worked example.
2. Read how Teletubby takes scripts: its CLAUDE.md, `src/core/agent-layer.ts`, and its `api/openrpc.json` if present, at `/Users/davidcruwys/dev/ad/flivideo/teletubby`. Confirm the handover verb exists, and note its input shape.
3. **Create the worktree** `/Users/davidcruwys/dev/ad/flivideo/flistudio-worktrees/storypilot` (branch `storypilot`, off FliStudio main), and **write the spec** there at `docs/planning/storypilot/spec.md`. Commit and push the spec on the branch. It is the only file you commit before David's go. It covers:
   - the settings layers and their fields;
   - the source-reference model (sessions, notes, order, labels);
   - the verbs, with kind (query or command) and fence;
   - where state lives on disk (inside FliStudio's lane);
   - the Teletubby handover;
   - the screen, at a sketch level;
   - the conformance and test plan;
   - the Overlay Pilot video as the acceptance test;
   - open questions.

   Mark each claim as either David's (with a B667/B670 citation) or your proposal.
4. **STOP. Report the spec to David and wait for his go.**
5. On his go, build in the same worktree and branch. The gates are FliStudio's full set:
   - build, typecheck, lint (includes depcruise), format:check and api:check;
   - all tests, plus StoryPilot's conformance;
   - `npm run test:e2e`.

   Push the branch, then report to David and to `flivideo-orch`.

## 4 · Constraints

- **Never merge to FliStudio main. Never start, stop or restart FliStudio, Teletubby or any app.** `flivideo-orch` merges and restarts on David's go, and only after `my-app` reports FliStudio isn't busy.
- **Don't change `@flivideo/extension-core` or `fli-core`.** If you need a change there, it's a finding: report it.
- **Tests use fixture estates**, never the live estate, `~/.config/appydave` or `~/.fli`.
- **Never invent David's intent.** Anything not in B667/B670 is a proposal and is labelled as one.
- **Report in plain language,** leading with the verdict. David doesn't read jargon-dense walls.
