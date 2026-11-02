---
created: 2026-11-02
timestamp: 2026-11-02T13:15+07:00
---
# Brief: how to build a macOS app in Swift — reusable research for Snappy and future Swift rigs (2026-11-02)

**From:** `flivideo-orch` (Swagger). **To:** `swift-rsch`. Report to `flivideo-orch` by name.

**Why:** David approved Snappy in **Swift** (spec: `/Users/davidcruwys/dev/ad/flivideo/docs/specs/snappy-spec-2026-11-02.md`,
§9 approvals). It will be built by an OpenRig developer/tester rig, and this research is the rig's starting knowledge and
the first entry in a reusable Swift knowledge base for future Swift apps.

## Cover (current, primary sources: developer.apple.com docs, swift.org, Apple sample code; context7 where useful)
1. Toolchain on this fleet: which Xcode / Swift versions are installed on the M4 (`xcodebuild -version`, `swift --version`),
   SwiftPM vs Xcode project, building a signed `.app` from the command line, code signing identity, notarisation need for
   local-only use, stable bundle identity so permission grants survive rebuilds.
2. Menu-bar agent apps: `NSStatusItem`, `LSUIElement`, SwiftUI `MenuBarExtra` vs AppKit, launch at login (`SMAppService`).
3. ScreenCaptureKit for stills: `SCScreenshotManager` (macOS 14 / 15.2 / 26 variants), content filters excluding own windows,
   permission preflight/request, the Sequoia/26 re-prompt behaviour.
4. Global hotkeys: Carbon `RegisterEventHotKey` vs `NSEvent` monitors vs third-party packages (e.g. KeyboardShortcuts);
   which need Accessibility / Input Monitoring.
5. Overlay windows: borderless click-through `NSWindow` above all spaces/full-screen apps.
6. CLI packaging: a CLI target in the same package, talking to the agent over a Unix socket; installing it on PATH.
7. Testing: XCTest / Swift Testing from the command line, what can be tested headless, what needs a real display.
8. Agent-friendliness: what an LLM coding agent gets wrong in Swift/macOS most often, and guardrails for a rig.

## Where it goes (reusable, not buried in this project)
Create a brain: `/Users/davidcruwys/dev/ad/brains/swift-macos/` following
`/Users/davidcruwys/dev/ad/brains/brain-documentation-pattern.md` (INDEX.md with frontmatter, kebab-case files, sources/).
Include a `snappy-build-notes.md` that maps each item above to Snappy's spec sections, and a `rig-learnings.md` stub
(where the first build's learnings will be banked). Commit and push the brains repo (only your folder).

## Limits
- Research and documentation only. **Do not create a Snappy repo, do not write app code, do not run the four spikes
  (§8 of the spec) — David has not released them.** Small throwaway `swift` one-liners to confirm a toolchain fact are fine.
- Do not install Xcode or packages. Report what is missing instead.
- STOP after the brain is written and report the path + gaps to `flivideo-orch`.
