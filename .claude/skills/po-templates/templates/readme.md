# [Project Name] Documentation

Documentation for [Project Name] - [brief description].

---

## Quick Links

| Document | Purpose |
|----------|---------|
| [backlog.md](backlog.md) | Active requirements (FRs/NFRs) |
| [changelog.md](changelog.md) | Implementation history |
| [brainstorming-notes.md](brainstorming-notes.md) | Ideas and exploration |
| [handover-queue.md](handover-queue.md) | PO ↔ Dev communication |

---

## Documentation Structure

```
docs/
├── prd/                  # Feature specs (complex requirements)
├── planning/             # Architecture, initial requirements
├── uat/                  # User Acceptance Testing
├── backlog.md            # Active requirements
├── changelog.md          # Version history
├── brainstorming-notes.md
├── handover-queue.md     # PO ↔ Dev handovers
└── README.md             # This file
```

---

## Workflow

```
Stakeholder (David)
       │
       ▼
┌─────────────────┐
│  /po Agent      │  ← Requirements gathering
│  backlog.md     │  ← Document FRs/NFRs
│  prd/*.md       │  ← Detailed specs
└────────┬────────┘
         │ handover (via handover-queue.md)
         ▼
┌─────────────────┐
│  /dev Agent     │  ← Implementation
│  [project]/     │  ← Code changes
└────────┬────────┘
         │ completion
         ▼
┌─────────────────┐
│  /uat Agent     │  ← Testing
│  uat/*.md       │  ← Test results
└────────┬────────┘
         │ verified
         ▼
┌─────────────────┐
│  changelog.md   │  ← History updated
└─────────────────┘
```

---

## Related

- **Application code**: `../`
- **Slash commands**: `../.claude/commands/` (inherited from FliVideo)
- **Skills**: `../.claude/skills/` (inherited from FliVideo)
