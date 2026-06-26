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
- Hosted verification remains required before merge.
