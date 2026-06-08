# HexToColor Whitespace Parsing Baseline Plan

status: completed

## Context

`toColor(hex:)` trims surrounding whitespace and newlines before parsing a
six-character RGB value. That behavior is useful for callers that pass values
from text fields or copied CSS snippets, but the existing baseline did not
cover it directly.

## Objectives

- Preserve whitespace/newline trimming before hex parsing.
- Keep invalid-input fallback behavior unchanged.
- Extend the static baseline so the trimming test remains present.
- Document the parser behavior.

## Work Items

1. Added `testTrimsWhitespaceAndNewlines`.
2. Extended `scripts/check-baseline.py` to require the trimming coverage.
3. Updated README, VISION, CHANGES, and this plan.

## Verification

- `make check`
- `git diff --check`
