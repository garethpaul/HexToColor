## HexToColor Vision

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

Next priorities:

- Document supported hex formats and failure behavior
- Modernize Swift/project settings in a dedicated pass
- Add tests for shorthand, alpha, case, and malformed strings if supported
- Clarify package-manager support if revived

Contribution rules:

- One PR = one focused API, test, package, or documentation change.
- Keep the library dependency-free.
- Run the build script or Xcode tests before pushing behavior changes.
- Treat API compatibility as important for consumers.

## Security

This utility has low security risk, but parsing should be deterministic and
should not crash callers on malformed input.

## What We Will Not Merge For Now

- Broad UI frameworks or unrelated color tooling
- API-breaking changes without migration notes
- Package metadata changes without verification
- Parser behavior changes without tests
