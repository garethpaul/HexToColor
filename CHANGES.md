# Changes

## 2026-06-26 01:22 UTC - P2 - unambiguous simulator discovery

### Summary

Automatic Xcode test discovery now selects an available iPhone by UDID instead
of a model name that can be duplicated across installed iOS runtimes.

### Work completed

- Added a portable AWK selector for the first available iPhone UDID.
- Preserved explicit `IOS_DESTINATION` and `IOS_SIMULATOR_NAME` overrides.
- Added a duplicate-name fixture contract and updated build documentation.

### Threads

- None; the focused build-script change was completed directly.

### Files changed

- `build.sh` and `scripts/select-ios-simulator-id.awk` - select the automatic destination by ID.
- `scripts/check-baseline.py` - execute the selector against duplicate model names.
- `README.md`, `VISION.md`, and `docs/plans/2026-06-25-simulator-id-selection*.md` - record the behavior and design.

### Validation

- `make check` and `sh -n build.sh` passed locally.
- Hosted SwiftPM and Xcode tests are required before merge.

### Bugs / findings

- P2: name-only automatic destinations can be ambiguous when multiple installed runtimes contain the same iPhone model.

### Blockers

- Xcode and Apple simulators are unavailable on the local Linux host.

### Next action

- Run hosted macOS validation and merge only if the exact PR head is green.

## 2026-06-19

- Replaced Foundation scanner and Unicode-wide trimming with an exact UTF-8
  grammar that trims only ASCII space, tab, carriage return, and line feed and
  rejects Unicode whitespace, controls, homoglyphs, partial parses, and overflow.
- Added AppKit support through the shared `HexColor` type alias while preserving
  the existing UIKit function call shapes and gray compatibility fallback.
- Upgraded hosted verification from manifest parsing to executable Swift package tests,
  removed unhandled plist warnings, and retained simulator XCTest.
- Added byte-range property coverage plus focused alpha-order, malformed-prefix,
  Unicode, control-character, and whitespace mutation cases.

## 2026-06-17

- Added Swift Package Manager metadata for the existing iOS 12, Swift 5 source
  and XCTest layout, with hosted manifest parsing through `make test`.

## 2026-06-13

- Made every Make verification target derive the checkout root so parser and
  XCTest gates work from external directories.
- Validated ASCII hex source characters before uppercasing so Unicode case
  expansion cannot turn malformed input into accepted color data.
- Added hosted XCTest coverage proving fully transparent RGBA is a valid
  failable parse and does not take the gray compatibility fallback.
- Added public `parseHexColor(_:) -> UIColor?` so callers can distinguish
  malformed input from a valid gray color while both existing `toColor` call
  shapes retain their gray compatibility fallback.

## 2026-06-12

- Added hosted XCTest coverage for the deprecated `toColor(hex:)` call shape
  and verified that it delegates through full RGBA component parsing.
- Migrated the parser and XCTest target from Swift 2-era syntax to Swift 5 while
  preserving unlabeled calls and a deprecated labeled compatibility wrapper.
- Raised the Xcode project deployment floor to iOS 12 and made `build.sh`
  discover an available simulator when no destination override is provided.
- Aligned CocoaPods compatibility metadata with Swift 5 and iOS 12 while
  leaving release versioning unchanged.
- Changed hosted macOS validation from project listing only to the real XCTest
  suite through `make test`, with checkout credential persistence disabled.
- Removed the obsolete Xcode 7 Travis job so the current GitHub Actions XCTest
  workflow is the sole hosted validation contract.

## 2026-06-10

- Completed the alpha parsing test matrix for `0x` and `#0x` prefixes at both
  shorthand and full RGBA widths.
- Added pinned macOS GitHub Actions validation for parser/source guardrails and
  current-Xcode project parsing.

## 2026-06-09

- Added coverage for prefixed shorthand and RGBA alpha forms such as `0xRGBA`
  and `#0xRRGGBBAA`.
- Added `make lint`, `make test`, and `make build` aliases so local verification
  has the expected pre-push gate targets in addition to `make check`.
- Added parser support and focused coverage for three-character RGB shorthand
  strings such as `#F0A`, while preserving gray fallback for malformed lengths.
- Added parser support and focused coverage for RGBA alpha strings such as
  `#F0A8` and `#33669980`.
- Rejected signed-looking and other non-hex characters before scanner
  conversion so malformed values stay on the gray fallback path.
- Added explicit coverage and docs for `#0x`-prefixed RGB strings, which
  normalize through the same parser path as `0xRRGGBB`.
- Updated invalid-length coverage to use unsupported lengths now that
  four-character RGBA shorthand is valid.

## 2026-06-08

- Added `make check` for static Xcode, podspec, plist, and parser guardrails.
- Kept the package API consumable by exposing the public `toColor(hex:)` function.
- Rejected partial `NSScanner.scanHexInt` parses so invalid hex strings return gray.
- Replaced the placeholder performance test with focused valid and invalid hex parser tests.
- Added parser coverage for whitespace and newline trimming.
- Added parser support and coverage for `0x`-prefixed RGB strings.
- Made `build.sh` POSIX-safe and configurable through Xcode destination environment variables.
