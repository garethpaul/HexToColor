# Cover Transparent Alpha Boundaries

status: planned

## Context

The parser supports four-digit RGBA shorthand and eight-digit RGBA values, but
existing tests use only nonzero alpha bytes. Fully transparent black encodes to
an all-zero numeric value, so it is the boundary most likely to expose a parser
that mistakes zero for scan failure or lets the compatibility wrapper return
gray instead of a valid transparent color.

## Priority

The new failable API makes success versus failure explicit. Hosted XCTest should
prove that zero-valued RGBA input remains a successful parse across both
supported alpha widths before further parser refactoring or release work.

## Scope

1. Add XCTest coverage for `#0000` and `#00000000` through
   `parseHexColor(_:)`, requiring non-`nil` colors with all channels zero.
2. Confirm `toColor(_:)` preserves the valid transparent result rather than
   taking the gray fallback path.
3. Extend the static baseline and maintenance documentation with exact boundary
   contracts.
4. Preserve parser source, supported syntax, podspec version, deployment target,
   and stacked prerequisite branches unchanged.

## Verification Plan

- Run checker compilation, all four Make gates, shell and podspec syntax, YAML
  parsing, diff checks, and intended-file artifact and secret scans locally.
- Remove the transparent-alpha test, remove the failable assertion, and change
  the expected alpha from zero; every hostile mutation must fail.
- Require hosted macOS XCTest on both push and pull-request events before the
  tracker evidence is completed.

## Risk And Rollback

This change adds characterization only and does not alter production parsing.
Rollback removes the transparent-alpha regression, leaving future parser
changes without explicit protection for valid all-zero RGBA values.

## Work Completed

Pending implementation.

## Verification Completed

Pending implementation and verification.
