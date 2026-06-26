# Cross-Platform Description Alignment

status: completed

## Problem

The maintained source and Swift package support both UIKit and AppKit through
`HexColor`, but source comments and top-level project descriptions still called
the repository a UIColor convenience sample.

## Decision

Describe the public result as a platform color and the repository as a UIKit and
AppKit library. Preserve API names, parser behavior, platform floors, and the
legacy CocoaPods release boundary.

## Verification

- The portable baseline failed first on the stale UIKit-only descriptions.
- Source and project guidance now name the shared platform surface.
- Agent guidance distinguishes the cross-platform Swift package from the
  iOS-only legacy Xcode and CocoaPods release surfaces.
- `make check`, `make lint`, `make test`, and `make build` passed locally; Swift
  package and Xcode execution skipped because those toolchains are unavailable.
- Exact-head Check runs `28246877617` and `28246879410` passed in 2m39s and
  4m50s, executing the maintained AppKit SwiftPM and UIKit XCTest surfaces.
- CodeQL run `28246876636` passed Actions, Python, and Swift analysis; Swift
  completed in 17m52s.
- Codex review was attempted on both branch heads and blocked by repeated OpenAI
  API HTTP 401 failures; immutable exact-head manual review found no actionable
  findings.
