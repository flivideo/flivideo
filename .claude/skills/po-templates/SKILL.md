---
name: po-templates
description: Scaffold product documentation files for FliVideo projects. Use when (1) starting a new project that needs docs structure, (2) PO needs to create backlog.md, changelog.md, or brainstorming-notes.md, (3) docs/README.md index is needed. Creates files in docs/ relative to current project.
---

# PO Templates

Scaffold product documentation for FliVideo projects.

## File Location

All files created in `docs/` relative to project root.

## Commands

### Scaffold All Docs

When asked to "scaffold docs" or "set up documentation":

1. Create `docs/` directory if needed
2. Create `docs/prd/` directory
3. Create `docs/uat/` directory
4. Create each file from templates below

### Individual Files

Create specific files when requested:
- "create backlog" → `docs/backlog.md`
- "create changelog" → `docs/changelog.md`
- "create brainstorming" → `docs/brainstorming-notes.md`
- "create docs readme" → `docs/README.md`

## Templates

### docs/README.md

See `templates/readme.md`

### docs/backlog.md

See `templates/backlog.md`

### docs/changelog.md

See `templates/changelog.md`

### docs/brainstorming-notes.md

See `templates/brainstorming-notes.md`

## Usage

After creating files, inform the user what was created and suggest next steps:
- Use `/po` to start capturing requirements
- Use `/brainstorming-agent` to capture ideas
