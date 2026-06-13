# Validate Hex Before Unicode Case Normalization

status: in_progress

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
