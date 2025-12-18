---
name: handover-queue
description: Manage handover communication between PO and Dev agents via a central queue file. Use when (1) PO needs to hand work to Dev with full context, (2) Dev needs to read assigned work from queue, (3) Dev needs to mark work complete with notes, (4) PO needs to process completed items into changelog. Works with docs/handover-queue.md relative to current project.
---

# Handover Queue

Central file-based communication between PO and Dev agents.

## File Location

Queue file: `docs/handover-queue.md` (relative to project root)

**If file doesn't exist**: Ask user if they want to create it. If yes, create with template from references/queue-format.md.

## Commands

### PO: Create Handover

When PO says "hand over FR-XX" or similar:

1. Read `docs/handover-queue.md`
2. Add new entry to `## Pending` section:

```markdown
### FR-XX: Title
**Created:** YYYY-MM-DD
**Status:** Pending

**Problem:** [One sentence]

**Implementation:**
[Full implementation details - files, code snippets, acceptance criteria]
[Must be COMPLETE and SELF-CONTAINED - Dev works from this alone]

---
```

3. Confirm handover added

### Dev: Read Queue

When Dev says "what's in my queue" or starts work:

1. Read `docs/handover-queue.md`
2. Show items in `## Pending` section
3. If starting specific FR-XX, update status to `In Progress`

### Dev: Complete Work

When Dev says "mark FR-XX complete" or provides handover:

1. Read `docs/handover-queue.md`
2. Move FR-XX entry from `## Pending` to `## Completed`
3. Update the entry:

```markdown
### FR-XX: Title
**Created:** YYYY-MM-DD
**Completed:** YYYY-MM-DD
**Status:** Complete

**Problem:** [original]

**Implementation:** [original]

**Completion Notes:**
[What was implemented]
[Files changed]
[Testing notes]

---
```

### PO: Process Completed

When PO says "process completed items" or similar:

1. Read `docs/handover-queue.md`
2. For each item in `## Completed`:
   - Show summary to PO
   - Help update `docs/changelog.md`
   - Help update `docs/backlog.md` status
3. After processing, remove items from `## Completed` section
4. Optionally move to `## Archived` if keeping history

## Queue File Format

See references/queue-format.md for full template and examples.

## Key Principles

- **Self-contained handovers**: Dev works from queue alone, no hunting through files
- **Single source of truth**: All active handovers in one place
- **Clean transitions**: Items flow Pending → Completed → Archived/Removed
