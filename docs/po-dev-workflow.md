# PO ↔ Dev Workflow

Shared workflow pattern for FliVideo projects (FliHub, FliDeck, etc.).

---

## The Pattern

```
backlog.md        = INDEX ONLY (table with links, status tracking)
docs/prd/*.md     = REQUIREMENT SPECS (these ARE the handoffs)
changelog.md      = HISTORY (what shipped and when)
```

---

## Flow Diagram

```
  PRODUCT OWNER                                    DEVELOPER
  ─────────────                                    ─────────
       │                                                │
       │  1. Create PRD file                            │
       │     docs/prd/fr-XX-name.md                     │
       │     • User Story                               │
       │     • Problem / Solution                       │
       │     • Acceptance Criteria                      │
       │     • Technical Notes                          │
       │     • Completion Notes: (empty)                │
       │                                                │
       │  2. Add to backlog.md index                    │
       │     Status: Pending                            │
       │                                                │
       │              ─────────────────►                │
       │               HANDOFF TO DEV                   │
       │              (PRD file IS the handoff)         │
       │                                                │
       │                                   3. Implement │
       │                                                │
       │                                   4. Fill in   │
       │                                      Completion│
       │                                      Notes     │
       │                                                │
       │                                   5. Update    │
       │                                      backlog   │
       │                                      Status:   │
       │                                      Implemented
       │                                                │
       │              ◄─────────────────                │
       │               HANDOFF TO PO                    │
       │              (same PRD file, now complete)     │
       │                                                │
       │  6. Review & verify                            │
       │  7. Update changelog.md                        │
       │  8. Archive if needed                          │
       │                                                │
       ▼                                                ▼
```

---

## Key Principles

1. **Single source of truth** - The PRD file contains everything (spec + completion notes)
2. **Backlog stays slim** - Just an index table linking to PRD files
3. **No duplication** - Don't copy specs into a separate handover document
4. **Status in one place** - backlog.md tracks status, PRD has details

---

## PRD File Template

```markdown
# FR-XX: [Title]

**Status:** [Pending/Implemented]
**Added:** YYYY-MM-DD
**Implemented:** [Date or -]

---

## User Story
As a [user], I want [goal] so that [benefit].

## Problem
[What pain exists]

## Solution
[How we're solving it]

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2

## Technical Notes
[Implementation guidance]

## Completion Notes
_To be filled by developer upon completion._
```

---

## Backlog Index Template

```markdown
# Backlog

Requirements index for [Project Name].

## Requirements

| ID | Requirement | Added | Status |
|----|-------------|-------|--------|
| FR-1 | [Title](prd/fr-01-name.md) | 2025-12-18 | Pending |

## Status Legend

| Status | Meaning |
|--------|---------|
| `Pending` | Ready for development |
| `With Developer` | Currently being implemented |
| `Implemented` | Complete |
| `Needs Rework` | Issues found |
```

---

## Slash Commands

| Command | Role | Action |
|---------|------|--------|
| `/po` | Product Owner | Creates PRD files, manages backlog |
| `/dev` | Developer | Implements from PRD, fills completion notes |
| `/uat` | Tester | Verifies implementations |
| `/progress` | Status | Quick status check |

---

## Related

- Commands: `/flivideo/.claude/commands/`
- FliHub docs: `/flivideo/flihub/docs/`
- FliDeck docs: `/flivideo/flideck/docs/`
