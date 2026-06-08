# HexToColor Parser Baseline Plan

status: completed

## Context

`HexToColor` is a small Swift 2-era iOS framework that converts six-character
hex strings into `UIColor` values. Local `xcodebuild` is unavailable here, so
the practical baseline is static project validation plus parser guardrails.

## Objectives

- Add a reproducible `make check` command that does not require Xcode.
- Keep the legacy Xcode build script configurable for simulator differences.
- Reject invalid six-character hex strings instead of accepting partial scans.
- Cover valid, lowercase, short, and malformed hex inputs with tests.
- Document the static baseline and remaining Xcode requirement.

## Work Items

1. Added `Makefile` and `scripts/check-baseline.py`.
2. Made `build.sh` POSIX-safe and configurable with `IOS_SIMULATOR_NAME` and `IOS_DESTINATION`.
3. Rejected partial `NSScanner.scanHexInt` parses in `toColor`.
4. Added focused parser tests and removed the placeholder performance test.
5. Added Xcode artifact ignore rules.
6. Updated README, VISION, CHANGES, and podspec URL metadata.

## Verification

- `make check`
- `git diff --check`
