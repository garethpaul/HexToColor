# Location-Independent HexToColor Verification

status: completed

## Context

Rooted recipes support external callers, but GNU Make still split an absolute
Makefile path containing spaces before deriving the checkout root.

## Priority

This is the next narrow automation reliability gap. Fixing it keeps local and
hosted wrappers consistent without changing color parsing, public APIs,
project settings, dependencies, or workflow policy.

## Scope

1. Derive the repository root from a quoted, validated single `MAKEFILE_LIST`
   path that preserves spaces.
2. Invoke the Python checker and conditional XCTest script through rooted
   paths.
3. Add a recursive-safe spaced-path full gate and synchronized contracts.
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

- Derived `ROOT` from a quoted single Makefile path, reject `MAKEFILES`,
  overridden metadata, and additional loaded Makefiles, invoke the Python
  checker through its absolute path, and change into the checkout before
  running `build.sh`.
- Added exact Makefile, completed-plan, external-run, authority-rejection, and
  synchronized-guidance contracts.
- Preserved Swift sources, tests, podspec, Xcode project, and workflow files.

## Verification Completed

- Root and external-directory Make gates passed for `lint`, `test`, `build`,
  and `check`; Linux correctly reported the existing XCTest toolchain skip.
- Spaced-checkout checks passed under GNU Make 4.2 and 4.4.
- `MAKEFILES` preloads and additional Makefiles before or after the repository
  Makefile fail closed instead of collapsing path separators into `ROOT`.
- The root-derivation mutation failed.
- The checker-invocation mutation failed.
- The XCTest-script mutation failed.
- The plan-status mutation failed.
- The plan-evidence mutation failed.
- The documentation mutation failed.
- Checker compilation, shell syntax, podspec syntax, plist parsing, workflow
  YAML parsing, diff hygiene, exact intended-path review, secret scanning, and
  generated-artifact inspection passed.
