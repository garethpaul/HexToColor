# HexToColor Signed Character Guard

status: completed

## Context

`toColor(hex:)` already constrained normalized input to six or eight
characters and rejected partial scanner parses. The parser still benefits from
an explicit hexadecimal character allowlist before invoking `NSScanner`, so
signed-looking strings and other non-hex input cannot depend on scanner edge
cases.

## Objectives

- Preserve valid RGB, RGBA, shorthand, whitespace, and `0x` parsing behavior.
- Reject signed-looking values such as `+FFFFF` and `-FFFFF`.
- Keep malformed values returning `UIColor.grayColor()`.
- Extend the static baseline and XCTest source coverage without requiring
  local Xcode.

## Verification

- `python3 scripts/check-baseline.py`
- `make check`
- `git diff --check`
