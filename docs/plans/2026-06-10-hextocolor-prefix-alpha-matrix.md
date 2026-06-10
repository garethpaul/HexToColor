# HexToColor Prefix Alpha Matrix

status: completed

## Context

The parser accepts both `0x` and `#0x` prefixes for four-digit RGBA shorthand
and eight-digit RGBA values. Existing tests covered only one width for each
prefix, leaving two valid combinations uncharacterized even though all four
pass through the same normalization code.

## Completed Scope

- Added `0xRRGGBBAA` XCTest coverage.
- Added `#0xRGBA` XCTest coverage.
- Extended the static baseline to require all four prefix/alpha-width cases.
- Documented the complete accepted prefix matrix without changing parser API or
  behavior.

## Verification

- `make lint`
- `make test`
- `make build`
- `make check`
- `git diff --check`
