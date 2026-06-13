# Location-Independent HexToColor Verification

status: completed

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

- Derived `ROOT` from the loaded Makefile, invoked the Python checker through
  its absolute path, and changed into the checkout before running `build.sh`.
- Added exact Makefile, completed-plan, external-run, and synchronized-guidance
  contracts.
- Preserved Swift sources, tests, podspec, Xcode project, and workflow files.

## Verification Completed

- Root and external-directory Make gates passed for `lint`, `test`, `build`,
  and `check`; Linux correctly reported the existing XCTest toolchain skip.
- The root-derivation mutation failed.
- The checker-invocation mutation failed.
- The XCTest-script mutation failed.
- The plan-status mutation failed.
- The plan-evidence mutation failed.
- The documentation mutation failed.
- Checker compilation, shell syntax, podspec syntax, plist parsing, workflow
  YAML parsing, diff hygiene, exact intended-path review, secret scanning, and
  generated-artifact inspection passed.
