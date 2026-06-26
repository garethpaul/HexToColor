## HexToColor Vision

This document explains the current state and direction of the project.
Project overview and developer docs: [`README.md`](README.md)

HexToColor is a small Apple-platform utility library that provides convenience
methods for creating UIKit or AppKit color values from hex strings.

The repository is useful as a compact Swift/Objective-C library sample with a
podspec, tests, and Xcode project setup. Project context lives in
[`README.md`](README.md).

The goal is to keep the color utility tiny, predictable, and easy to consume.

The current focus is:

Priority:

- Preserve the hex-to-UIColor conversion API while sharing parser behavior with AppKit
- Keep podspec and Xcode project metadata aligned
- Maintain test coverage for valid and invalid color inputs
- Avoid adding broader color-system behavior without a clear need
- Keep `make lint`, `make test`, `make build`, and `make check` passing for
  static parser, podspec, plist, and build-script guardrails

Current baseline:

- GitHub Actions runs the parser/source baseline and real XCTest suite on macOS
  through `make test`; simulator selection remains configurable through
  `build.sh`.
- Automatic XCTest destination discovery uses a simulator UDID so duplicate
  device names across installed iOS runtimes remain unambiguous.
- Framework and test targets use Swift 5 with an iOS 12 deployment floor.
- CocoaPods compatibility metadata matches Swift 5 and iOS 12 while release
  versioning remains unchanged until a future tag.
- Swift Package Manager exposes the existing source and XCTest layout as an
  iOS 12/macOS 10.13 Swift 5 library without replacing CocoaPods or the Xcode
  project; Swift package tests execute the AppKit path on macOS.
- Invalid hex strings, including partial `scanHexInt` parses, return gray.
- Public `parseHexColor(_:)` returns `nil` when callers need explicit failure,
  while both existing `toColor` call shapes preserve the gray fallback.
- Parse only ASCII hex source bytes without Unicode case normalization.
- Alpha parsing remains characterized for both accepted prefixes at shorthand
  and full RGBA widths.
- The package exposes public `toColor(_:)` and retains deprecated
  `toColor(hex:)` compatibility for labeled callers, with the compatibility
  path executed by hosted XCTest.
- Surrounding ASCII space, tab, carriage return, and line feed are trimmed;
  Unicode whitespace and other controls are rejected.
- Valid hash-prefixed and lowercase six-character values have focused tests.
- `0x`-prefixed six-character RGB values are supported without changing the
  invalid-input fallback.
- `#0x`-prefixed six-character RGB values normalize through the same parsing
  path after the hash prefix is stripped.
- Three-character RGB shorthand values are expanded before the existing
  six-character validation path.
- Four-character RGBA shorthand and eight-character RGBA values preserve alpha
  while RGB values remain opaque by default.
- Fully transparent RGBA remains valid input rather than gray fallback.
- 0x-prefixed shorthand and RGBA values normalize before shorthand expansion
  and alpha parsing.
- Unsupported lengths still return gray now that four-character RGBA shorthand
  is valid.
- Non-hex characters, including signed-looking strings, are rejected before
  scanner conversion.
- Mixed-case payloads across every accepted prefix and width are covered by the
  executable XCTest matrix.
- Malformed prefixes, partial parses, overflow, Unicode lookalikes, and controls
  are rejected and locked into the static baseline contract.
- `build.sh` discovers an available iPhone simulator and supports explicit
  destination overrides for current Xcode tests.
- Static checks validate plists, podspec HTTPS metadata, and generated Xcode artifact ignores.
- Local verification targets stay available while full Xcode execution needs a
  macOS toolchain.

Next priorities:

- Align CocoaPods release metadata with the modernized source in a future tag
- Publish a future tag that includes the Swift package manifest

Contribution rules:

- One PR = one focused API, test, package, or documentation change.
- Keep the library dependency-free.
- Run the build script or Xcode tests before pushing behavior changes.
- Treat API compatibility as important for consumers.

## Security

Canonical security policy and reporting:

- [`SECURITY.md`](SECURITY.md)

This utility has low security risk, but parsing should be deterministic and
should not crash callers on malformed input.

## What We Will Not Merge (For Now)

- Broad UI frameworks or unrelated color tooling
- API-breaking changes without migration notes
- Package metadata changes without verification
- Parser behavior changes without tests

This list is a roadmap guardrail, not a permanent rule.
Strong user demand and strong technical rationale can change it.
