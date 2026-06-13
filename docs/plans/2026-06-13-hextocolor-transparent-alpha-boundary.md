# Cover Transparent Alpha Boundaries

status: completed

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

- Added one hosted XCTest covering both `#0000` shorthand and `#00000000`
  full-width RGBA through the failable parser.
- Required each input to produce a non-`nil` color with zero red, green, blue,
  and alpha components.
- Verified the compatibility wrapper returns the same transparent color rather
  than its gray fallback.
- Extended static test, documentation, and completed-plan contracts without
  changing parser source, project settings, workflow, or release metadata.

## Verification Completed

- All four Make gates passed; XCTest was skipped because `xcodebuild` is not
  installed locally.
- `sh -n build.sh`, `ruby -c HexToColor.podspec`, workflow YAML parsing,
  `python3 -m py_compile scripts/check-baseline.py`, and `git diff --check`
  passed.
- Exact-base comparisons confirmed `Hex.swift`, the podspec, Xcode project, and
  hosted workflow remained unchanged.
- Three isolated hostile mutations were rejected: test removal, non-`nil`
  assertion removal, and a changed zero-alpha expectation.
- Intended-file generated-artifact and secret-pattern scans passed.
- Hosted macOS XCTest and CodeQL evidence is recorded separately after push;
  this plan claims only the completed local static verification above.
