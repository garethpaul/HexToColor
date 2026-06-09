# HexToColor 0x Prefix Parsing

status: completed

## Context

`toColor(hex:)` already accepts hash-prefixed and bare six-character RGB
strings after trimming surrounding whitespace. Callers may also pass copied
numeric-style color values such as `0x112233`; those should parse the same
six RGB digits instead of falling back to gray.

## Objectives

- Strip a leading `0x` or `0X` prefix after whitespace trimming.
- Keep the six-character RGB length check and gray invalid-input fallback.
- Add focused XCTest coverage for the prefixed form.
- Extend `scripts/check-baseline.py` so the parser and test guard remain
  visible without requiring Xcode locally.

## Verification

- `make check`
- `python3 scripts/check-baseline.py`
- `git diff --check`
