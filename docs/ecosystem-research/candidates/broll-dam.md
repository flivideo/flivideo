---
type: reference
tags: [flivideo, ecosystem-research, candidate, B686, broll-dam]
description: "Has anyone built the B-roll store + per-media-type tagging + human-override system David described? Immich, ResourceSpace, versus the Dam'It design."
created: 2026-11-03
timestamp: 2026-11-03T12:30+07:00
---

# B-roll hosting, tagging and delivery (DAM)

**Purpose**: Has anyone built the B-roll store + per-media-type tagging + human-override system David described? Immich, ResourceSpace, versus the Dam'It design.

**For Agents**: Research only (B686 B2, 2026-11-03). *Observed* = read in repo or via `gh api`; *Inference* and *Lean* are B2's and **not approved**. Anything unread is **UNVERIFIED**. Index: [../03b-capability-landscape.md](../03b-capability-landscape.md).

## Requirement (B686 verbatim intent)
Store all B-roll; tag it appropriately per media type; tags human-overridable; editors can pick assets. B-roll Pilot differs from a DAM in being *per video project*, not B-roll in general. Prior art: `brains/damit/` (design brain), `brains/video-as-code/broll-knowledge-2026-10-15.md` §5 (what exists in David's own estate; FliHub `b-roll/` deprecated, AITLDR brand library unused).

## 1. Immich
- **Repo**: https://github.com/immich-app/immich (clone `2c87a17`, `/Users/davidcruwys/dev/upstream/repos/immich`).
- **Licence**: AGPL-3.0 (GitHub API). Self-hosting for our own use is fine; modifying and offering as a network service triggers source-sharing.
- **Stars / last commit**: 118,039★, pushed 2026-11-03, 716 open issues, not archived.
- **Agent surface** *(Observed)*: OpenAPI spec with 338 operations (`open-api/immich-openapi-specs.json`), including `/tags`, `/tags/{id}/assets`, `/tags/assets`; API-key controller (`server/src/controllers/api-key.controller.ts`); smart search via ML vectors (`search.controller.ts`, `POST smart`); a CLI (`cli/`). Clean REST + generated SDKs, the best agent surface of any DAM candidate. **UNVERIFIED**: custom per-media-type metadata schemas (Immich is a photo/video library; tags exist, arbitrary typed fields were not found).
- **Security**: scoped scan CLEAN; 7 `AGENTS.md` files read (build/test conventions only). Large codebase and ML containers; internet-facing instances are a known target in general. Not run.
- **Two questions**:
  1. *Elegant?* Excellent for storing, tagging, searching photos/videos at scale; designed for personal libraries, not "projects with levels" (project/brand/central/global).
  2. *Agent-drivable safely?* Yes: scoped API keys, OpenAPI. Safe if kept on the tailnet.
- **Outcome lean (not approved)**: *absorb/add* as a possible storage + search backend behind a B-roll capability; *replace Dam'It* only if per-media-type tag schemas and the project-level view fit (they may not).

## 2. ResourceSpace
- **Repo**: https://github.com/resourcespace/resourcespace (clone `4151e4d`).
- **Licence**: GitHub reports NOASSERTION; `documentation/licenses/resourcespace.txt` reads as a BSD-style licence (redistribution with notice, no endorsement, plus a clause forbidding derived products from using the "ResourceSpace" trademark). Observed text, not legal advice; permissive for self-hosting.
- **Stars / last commit**: 88★ (the GitHub repo is a mirror; the project is long-established with its own site), pushed 2026-11-03, 5 open issues. Stars understate adoption; adoption not measured by B2.
- **Agent surface** *(Observed)*: PHP app with an `api/` directory, `include/api_functions.php`, user API sessions (`documentation/user_api_session_code.md`), plugins, strong metadata/field model, collections. Full API endpoint list not enumerated (**UNVERIFIED**). A 19 KB `AGENTS.md` (read, coding standards: prepared statements, CSRF tokens).
- **Security**: scoped scan CLEAN. PHP + MySQL stack: needs hardening and patching; historically a typical DAM attack surface. Not run.
- **Two questions**:
  1. *Elegant?* Closest to "metadata per resource type, human-editable, collections"; heavier admin UX.
  2. *Agent-drivable safely?* API exists; maturity for agents unproven.
- **Outcome lean (not approved)**: *none* now; keep as the comparison point for per-type metadata fields.

## 3. Dam'It (David's own design, brain only)
- **Repo**: not a repo here; design brain `/Users/davidcruwys/dev/ad/brains/damit/` (requirements-v2, domain-model, storage-economics). **Licence**: n/a (own). **Stars / last commit**: n/a.
- **Agent surface**: design stage; cheap fetch-on-demand cloud storage (R2) is the core bet (`storage-economics.md`). **Security**: n/a.
- **Two questions**: not applicable until built.
- **Outcome lean (not approved)**: stays the owner of the *storage economics* and *project/brand/central/global levels*; Immich could be an implementation detail, not a replacement of the design.

## Comparison
| | Immich | ResourceSpace | Dam'It (design) |
|---|---|---|---|
| Licence | AGPL-3.0 | BSD-style + trademark clause | own |
| Stars | 118k | 88 (mirror) | n/a |
| API for agents | OpenAPI, 338 ops, API keys | PHP API, sessions | planned |
| Per-media-type tags | tags only (UNVERIFIED typed fields) | rich resource-type fields | designed |
| Project-level view | albums, not projects | collections | designed levels |
| Ops burden | Docker + ML | PHP + MySQL | n/a |
