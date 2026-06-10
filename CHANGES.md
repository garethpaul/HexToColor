# Changes

## 2026-06-10

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
