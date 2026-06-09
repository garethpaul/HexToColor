# HexToColor RGBA Alpha Parsing

status: completed

## Context

`toColor(hex:)` supported RGB strings with optional `#` or `0x` prefixes and
three-character RGB shorthand. Callers also commonly use RGBA forms where the
last channel is alpha, such as `#F0A8` or `#33669980`.

## Objectives

- Expand four-character RGBA shorthand before scanner validation.
- Accept eight-character RGBA strings and map the final byte to alpha.
- Keep six-character RGB values opaque by default.
- Preserve gray fallback behavior for malformed lengths and invalid
  characters.
- Extend the static baseline so alpha parser coverage remains visible without
  requiring Xcode locally.

## Verification

- `make check`
- `git diff --check`
