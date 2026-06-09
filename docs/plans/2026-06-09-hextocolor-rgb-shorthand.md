# HexToColor RGB Shorthand Parsing

status: completed

## Context

`toColor(hex:)` accepted trimmed six-character RGB strings with optional `#` or
`0x` prefixes. Callers often copy CSS-style three-character RGB shorthand such
as `#F0A`, which should expand deterministically instead of falling back to
gray.

## Objectives

- Expand three-character RGB strings before the existing six-character scanner
  validation.
- Preserve the gray fallback for malformed lengths such as four characters.
- Add focused XCTest coverage for shorthand expansion.
- Extend `scripts/check-baseline.py` so shorthand support stays visible without
  requiring Xcode locally.

## Verification

- `make check`
- `git diff --check`
