# Location-Independent HexToColor Verification

status: planned

## Context

The maintained baseline passes from the checkout, but an absolute Makefile
invocation from another directory resolves both `scripts/check-baseline.py`
and `build.sh` relative to the caller.

## Priority

This is the next narrow automation reliability gap. Fixing it keeps local and
hosted wrappers consistent without changing color parsing, public APIs,
project settings, dependencies, or workflow policy.

## Scope

1. Derive the repository root from `MAKEFILE_LIST`.
2. Invoke the Python checker and conditional XCTest script through rooted
   paths.
3. Add completed-plan, external-run, guidance, and hostile-mutation contracts.
4. Preserve Swift sources, tests, podspec, Xcode project, and workflow files.

## Verification Plan

- Run lint, test, build, and check from the checkout and a temporary directory
  through the absolute Makefile path.
- Run checker compilation, shell syntax, project parsing where available, and
  `git diff --check`.
- Reject root, checker, XCTest-script, plan status/evidence, and documentation
  mutations.
- Inspect exact intended paths, secrets, and generated artifacts.

## Risk And Rollback

The change affects verification path resolution only. Rollback restores the
caller-relative recipes; no runtime state or migration exists.

## Work Completed

Pending implementation.

## Verification Completed

Pending implementation and validation. Run `make check` before completion.
