# FliVideo open questions

Questions that are still undecided. They aren't backlog items: nothing here is meant to be built. They're kept so a future
decision can start from them. When one is decided, write the decision and its date under it, and leave the question
in place.

## From the FliVideo architecture talk (3 Nov 2026)

**Sources:**
- Capture B686 (3 Nov, 34 min): the six core apps, extensions and pilots, and an 80/20 guardrail for extensions.
- Capture B687: its ChatGPT dossier, which widens the talk to the whole AppyDave ecosystem.

Recorded on David's ruling of 13 Nov: "not really backlog items … just open questions for the future that might be
useful. They can be recorded against the FliVideo project."

### Q1. What replaces FliEdit?
Keep its engine, move it onto another engine, or replace the app? The dossier's wording is "Should it retain its
engine, adopt another engine or be replaced?" (B686, B687)

### Q2. Should there be a B-roll library, and what shape?
Should B-roll Pilot own the asset-management side itself, or hand it to an outside asset manager (a DAM or MAM)?
(B686, B687)

### Q3. How is the 80/20 extension guardrail enforced?
The guardrail is about what belongs in an extension and what belongs in a standalone app. The dossier lists ways to
investigate: interface contracts, dependency direction, package separation, runtime boundaries and tests. No method
was approved. FliStudio's extension architecture (self-contained modules, shared contracts, no cross-module bleed) is
where to start. (B686, B687)

### Further questions listed in the B687 dossier (section 12)
Recorded as written there. The dossier says they "should remain open until the relevant evidence is available".

| Area | Open question |
|---|---|
| Umbrellas | What are the final boundaries and responsibilities of the four domains? |
| Applications | Which capabilities belong in standalone applications rather than extensions? |
| Shared libraries | Which contracts belong in fli-core, an extension-specific core or other shared packages? |
| Motion Pilot | Should it be an extension, a standalone application or an orchestration layer over external engines? |
| HyperFrames | Can it deliver the required visual quality, automation and reproducibility? |
| OpenMontage | Which architectural patterns are reusable, and what licensing constraints apply? |
| Story Pilot | How should structured story and production data drive asset selection and motion generation? |
| Tool interfaces | What common contracts should agents use to invoke capabilities? |
| Security | How can external engines and agent-driven operations be isolated appropriately? |
| Infrastructure | How should the team's machines coordinate research and keep artefacts in sync? |
| Approval | Which recommendations should go on to proof-of-concept work, and who authorises them? |
