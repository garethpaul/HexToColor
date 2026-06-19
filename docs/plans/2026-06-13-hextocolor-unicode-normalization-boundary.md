# Validate Hex Before Unicode Case Normalization

status: completed

## Context

`parseHexColor` uppercases the entire input before validating its character
set. Some non-ASCII Unicode scalars expand during case conversion; for example,
the `ﬀ` ligature can become the two ASCII characters `FF`. An input containing
non-hex source characters can therefore become valid-looking hex before the
parser checks it.

## Priority

This is the highest-value remaining isolated parser boundary because the public
failable API promises explicit rejection of malformed input. Validation should
describe the caller's source characters, not a compatibility transformation
performed afterward.

## Scope

1. Trim whitespace and remove supported prefixes without uppercasing content.
2. Validate source characters against ASCII uppercase and lowercase hex digits.
3. Preserve existing lowercase, shorthand, RGBA, transparent-alpha, prefix,
   and gray-fallback behavior.
4. Add focused XCTest coverage and mutation-sensitive static contracts.

## Verification Plan

- Run all four Make gates, checker compilation, workflow parsing, shell and
  podspec syntax, `git diff --check`, and intended-file artifact and secret
  scans. Local XCTest skips remain truthful when Xcode is unavailable.
- Restore pre-validation uppercasing, remove the Unicode regression, and weaken
  the ASCII character set; every hostile mutation must fail.
- Push a stacked pull request and take one bounded exact-head workflow and
  code-scanning snapshot without polling.

## Risk And Rollback

ASCII inputs retain their current results. Inputs that rely on Unicode case
expansion into ASCII hex now fail explicitly or use the compatibility gray
fallback. Rollback restores acceptance of transformed non-ASCII input; no
stored data or package format changes exist.

## Work Completed

- Deferred uppercasing until after source length and ASCII hex validation.
- Preserved lowercase `0x` and uppercase `0X` prefixes explicitly without
  relying on whole-string normalization.
- Added focused XCTest, static ordering contracts, project guidance, and
  completed-plan evidence requirements.

## Verification Completed

- All four Make gates passed the static baseline.
- XCTest was skipped because `xcodebuild` is not installed locally; hosted macOS
  XCTest remains the executable authority.
- `sh -n build.sh`, `ruby -c HexToColor.podspec`, Python checker compilation,
  workflow YAML parsing, and `git diff --check` passed.
- The pre-validation uppercasing mutation failed.
- The Unicode regression removal mutation failed.
- The ASCII character-set weakening mutation failed.
- Intended-file artifact and secret-pattern scans passed.
- The hosted macOS XCTest and CodeQL snapshot is recorded after push using
  bounded exact-head queries without polling.
