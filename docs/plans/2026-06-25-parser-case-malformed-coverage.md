# Parser Case and Malformed-Input Coverage Plan

status: completed

## Goal

Reconcile the roadmap with the parser coverage already delivered by the exact
UTF-8 grammar and its XCTest matrix, without changing public behavior.

## Evidence

- `testAcceptedPrefixWidthAndCaseMatrix` exercises mixed-case payloads at all
  four supported widths across no prefix, `#`, `0x`/`0X`, and `#0x`/`#0X`.
- `testRejectsPartialOverflowAndMalformedPrefixes` covers trailing data,
  overflow, incompatible prefix order, doubled prefixes, and repeated prefixes.
- Adjacent tests reject Unicode lookalikes, controls, unsupported lengths,
  signed-looking input, and non-hex bytes before parsing.
- `scripts/check-baseline.py` requires those named tests and their boundary
  fixtures, preventing the completed matrix from silently regressing.

## Work Completed

1. Confirmed the roadmap item was already satisfied by the current XCTest suite.
2. Removed the completed item from future priorities and recorded it in the baseline.
3. Added an executable documentation contract so the stale priority cannot return.
4. Linked this evidence from contributor and user-facing maintenance guidance.

No parser source change was required.

## Verification Completed

- Observed `python3 scripts/check-baseline.py` fail on the missing completion
  record before adding this plan and the synchronized documentation.
- Passed `make check`, `make lint`, `make test`, `make build`,
  `python3 -m py_compile scripts/check-baseline.py`, and `git diff --check` after
  the documentation update; Swift and Xcode were unavailable and explicitly
  skipped by the Make gates.
- Two isolated hostile mutations were rejected: restoring the completed
  roadmap item and removing the accepted case-matrix test name from this plan.
