# Changes

## 2026-06-08

- Added `make check` for static Xcode, podspec, plist, and parser guardrails.
- Kept the package API consumable by exposing the public `toColor(hex:)` function.
- Rejected partial `NSScanner.scanHexInt` parses so invalid hex strings return gray.
- Replaced the placeholder performance test with focused valid and invalid hex parser tests.
- Made `build.sh` POSIX-safe and configurable through Xcode destination environment variables.
