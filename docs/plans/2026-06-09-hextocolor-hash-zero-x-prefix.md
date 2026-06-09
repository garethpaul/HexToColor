# HexToColor Hash 0x Prefix Parsing

status: completed

## Context

`toColor(hex:)` trims input, strips a leading `#`, and then strips a leading
`0x`/`0X` prefix before validating RGB length and characters. That order means
`#0xRRGGBB` already parses correctly, but the behavior was implicit and not
covered by the baseline.

## Objectives

- Preserve the existing parser order that handles hash prefixes before `0x`
  prefixes.
- Add focused XCTest source coverage for `#0xRRGGBB`.
- Keep malformed signed or non-hex inputs on the gray fallback path.
- Extend `scripts/check-baseline.py`, README, VISION, and CHANGES so the
  normalization contract stays visible without requiring local Xcode.

## Verification

- `make check`
- `git diff --check`
