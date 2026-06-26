# Simulator ID Selection Implementation Plan

Status: Completed

## Goal

Make automatic iOS simulator discovery unambiguous without changing caller-supplied destination or simulator-name overrides.

## Tasks

1. Add a failing portable contract for duplicate simulator names.
2. Add a POSIX AWK selector for the first available iPhone UDID.
3. Use the selected UDID in the automatic Xcode destination.
4. Document the default behavior and maintenance result.
5. Run local checks and hosted Apple-platform tests.

## Verification Completed

- Observed the portable baseline fail on the missing simulator-ID selector before implementation.
- Passed `make check`, `make test`, `python3 -m py_compile scripts/check-baseline.py`, `sh -n build.sh`, and `git diff --check` locally; Swift and Xcode were unavailable and explicitly skipped by `make test`.
- Both hosted Check runs passed on the implementation head.
- SwiftPM executed 25 AppKit tests with zero failures, and Xcode executed 25 iOS simulator tests with zero failures.
- The Codex review helper was attempted against `origin/master` but could not authenticate; an exact-head manual review found no actionable findings.
