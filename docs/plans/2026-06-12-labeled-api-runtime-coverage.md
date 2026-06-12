# Labeled API Runtime Coverage

status: completed

## Context

The Swift 5 modernization preserves the historical `toColor(hex:)` call shape
as a deprecated wrapper around `toColor(_:)`. The static baseline verifies that
the wrapper source exists, but the XCTest suite never invokes it. A wrapper
that is removed, recursively delegates to itself, or diverges from the primary
RGBA path could therefore break existing clients without an executed
regression.

## Priority

Source compatibility is an explicit public contract for this small library.
The hosted workflow now runs real XCTest, so the compatibility entry point
should be exercised there instead of relying only on source-string checks.

## Prioritized Engineering Backlog

1. Execute the deprecated labeled API through the current RGBA parser now.
2. Add Swift Package Manager support only in a dedicated packaging change.
3. Align published CocoaPods release metadata when a new version is tagged.

## Requirements

- R1. XCTest must compile and invoke `toColor(hex:)` using the labeled call
  shape expected by historical clients.
- R2. The labeled API must return the same RGBA component values as
  `toColor(_:)` for a representative alpha-bearing input.
- R3. The wrapper must remain deprecated and delegate to the primary parser.
- R4. Parser acceptance, fallback behavior, deployment targets, and package
  version metadata must remain unchanged.
- R5. The static baseline must require the executed compatibility test and its
  labeled invocation.

## Implementation Units

### U1. Add compatibility XCTest

- **Files:** `HexToColorTests/HexToColorTests.swift`
- Call `toColor(hex:)` with an RGBA value and verify all four normalized color
  components.

### U2. Extend the baseline contract

- **Files:** `scripts/check-baseline.py`
- Require the new test and labeled call so hosted XCTest coverage cannot be
  silently removed.

### U3. Update maintenance documentation

- **Files:** `README.md`, `VISION.md`, `CHANGES.md`
- Record that the deprecated labeled compatibility API is covered by real
  XCTest.

## Scope Boundaries

- Do not change parser implementation or add new accepted formats.
- Do not remove the deprecation annotation.
- Do not change CocoaPods versioning, deployment targets, or Xcode settings.

## Verification

- `make check`
- `make test` on hosted macOS/Xcode
- `git diff --check`
- A mutation removing the labeled invocation must fail the static baseline.

Completed on 2026-06-12 with the local static baseline and mutation check
passing; the hosted macOS XCTest workflow is required before merge to compile
and execute the labeled compatibility call.
