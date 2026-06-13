# Changes

## 2026-06-13

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
