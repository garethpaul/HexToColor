# HexToColor Prefixed Alpha Coverage

status: completed

## Context

`toColor(hex:)` strips a leading hash and then a leading `0x`/`0X` prefix before
shorthand expansion and RGBA alpha parsing. That means prefixed shorthand and
eight-character RGBA values are supported, but the behavior was not covered
directly.

## Completed Scope

- Added focused XCTest source coverage for `0xRGBA` shorthand alpha input.
- Added focused XCTest source coverage for `#0xRRGGBBAA` alpha input.
- Extended the static baseline and docs so prefix normalization remains covered
  before shorthand expansion and alpha parsing.

## Verification

- `python3 scripts/check-baseline.py`
- `make check`
- `git diff --check`
