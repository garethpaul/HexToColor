## HexToColor Vision

This document explains the current state and direction of the project.
Project overview and developer docs: [`README.md`](README.md)

HexToColor is a small iOS utility library that provides convenience methods for
creating `UIColor` values from hex strings.

The repository is useful as a compact Swift/Objective-C library sample with a
podspec, tests, and Xcode project setup. Project context lives in
[`README.md`](README.md).

The goal is to keep the color utility tiny, predictable, and easy to consume.

The current focus is:

Priority:

- Preserve the hex-to-UIColor conversion API
- Keep podspec and Xcode project metadata aligned
- Maintain test coverage for valid and invalid color inputs
- Avoid adding broader color-system behavior without a clear need
- Keep `make check` passing for static parser, podspec, plist, and build-script guardrails

Current baseline:

- Invalid hex strings, including partial `scanHexInt` parses, return gray.
- The package exposes the conversion entry point as public `toColor(hex:)`.
- Valid hash-prefixed and lowercase six-character values have focused tests.
- `build.sh` supports simulator destination overrides for legacy Xcode tests.
- Static checks validate plists, podspec HTTPS metadata, and generated Xcode artifact ignores.

Next priorities:

- Modernize Swift/project settings in a dedicated pass
- Add tests for shorthand, alpha, case, and malformed strings if supported
- Clarify package-manager support if revived

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
