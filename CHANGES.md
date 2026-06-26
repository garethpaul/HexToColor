# Changes

## 2026-06-26 15:09 UTC - P3 - Align cross-platform library descriptions

### Summary

Corrected stale UIColor-only sample wording now that the maintained public
surface supports UIKit and AppKit through `HexColor`.

### Work completed

- Updated public parser comments to describe platform colors.
- Replaced sample-style README, security, and agent summaries with the
  maintained UIKit/AppKit library scope while retaining the iOS-only legacy
  release boundary.
- Added a portable contract that rejects regression to UIKit-only wording.

### Validation

- RED portable baseline — rejected the stale source comments and README overview.
- `make check`, `make lint`, `make test`, and `make build` — passed locally;
  Swift package and Xcode execution skipped because those toolchains are absent.
- Exact-head Check runs `28246877617` and `28246879410` — passed in 2m39s and
  4m50s, executing the AppKit SwiftPM and UIKit XCTest surfaces.
- CodeQL run `28246876636` — passed Actions, Python, and Swift analysis; Swift
  completed in 17m52s.
- Codex review helper — blocked by repeated OpenAI API HTTP 401 failures on both
  heads; immutable exact-head manual review found no actionable findings.

### Next action

- No follow-up is required for this completed description-alignment cycle.

## 2026-06-26 03:55 UTC - P3 - parser coverage roadmap reconciliation

### Summary

Reconciled the parser roadmap with the existing mixed-case and malformed-input test matrix.

### Work completed

- Confirmed the accepted-prefix matrix already covers mixed-case payloads at
  every supported width.
- Confirmed focused tests already reject malformed prefixes, partial parses,
  overflow, Unicode lookalikes, controls, signed-looking input, and invalid lengths.
- Removed the completed testing item from future priorities and added a static
  contract that prevents it from returning as stale roadmap work.

### Threads

- None; this was a focused evidence and documentation reconciliation.

### Files changed

- `scripts/check-baseline.py` - enforce the completed roadmap state.
- `README.md`, `VISION.md`, and `AGENTS.md` - synchronize user, roadmap, and contributor guidance.
- `docs/plans/2026-06-25-parser-case-malformed-coverage.md` - record the audit and evidence.

### Validation

- The new contract failed before the completion record existed, then all four
  Make gates, Python compilation, and diff checks passed after synchronization;
  Swift and Xcode were unavailable and explicitly skipped.
- Two isolated hostile mutations proved the checker rejects both the stale
  roadmap item and removal of the named coverage evidence.

### Bugs / findings

- P3: the roadmap still requested case and malformed-input tests that were already present and guarded.

### Blockers

- None.

### Next action

- Keep future parser work limited to a demonstrated behavior gap rather than duplicating this matrix.

## 2026-06-26 01:22 UTC - P2 - unambiguous simulator discovery

### Summary

Automatic Xcode test discovery now selects an available iPhone by UDID instead
of a model name that can be duplicated across installed iOS runtimes.

### Work completed

- Added a portable AWK selector for the first available iPhone UDID.
- Preserved explicit `IOS_DESTINATION` and `IOS_SIMULATOR_NAME` overrides.
- Added a duplicate-name fixture contract and updated build documentation.

### Threads

- None; the focused build-script change was completed directly.

### Files changed

- `build.sh` and `scripts/select-ios-simulator-id.awk` - select the automatic destination by ID.
- `scripts/check-baseline.py` - execute the selector against duplicate model names.
- `README.md`, `VISION.md`, and `docs/plans/2026-06-25-simulator-id-selection*.md` - record the behavior and design.

### Validation

- `make check`, `make test`, Python compilation, shell syntax, and diff checks passed locally; Swift and Xcode were unavailable and explicitly skipped.
- Both hosted Check runs passed; SwiftPM and Xcode each executed 25 tests with zero failures.
- Codex review could not authenticate; exact-head manual review found no actionable findings.

### Bugs / findings

- P2: name-only automatic destinations can be ambiguous when multiple installed runtimes contain the same iPhone model.

### Blockers

- No merge blocker remains. Xcode is unavailable locally, and the Codex CLI is not authenticated, so hosted tests and manual exact-head review supplied the missing evidence.

### Next action

- Re-run hosted checks for the evidence-only head, then squash merge if green.

## 2026-06-19

- Replaced Foundation scanner and Unicode-wide trimming with an exact UTF-8
  grammar that trims only ASCII space, tab, carriage return, and line feed and
  rejects Unicode whitespace, controls, homoglyphs, partial parses, and overflow.
- Added AppKit support through the shared `HexColor` type alias while preserving
  the existing UIKit function call shapes and gray compatibility fallback.
- Upgraded hosted verification from manifest parsing to executable Swift package tests,
  removed unhandled plist warnings, and retained simulator XCTest.
- Added byte-range property coverage plus focused alpha-order, malformed-prefix,
  Unicode, control-character, and whitespace mutation cases.

## 2026-06-17

- Added Swift Package Manager metadata for the existing iOS 12, Swift 5 source
  and XCTest layout, with hosted manifest parsing through `make test`.

## 2026-06-13

- Made every Make verification target derive the checkout root so parser and
  XCTest gates work from external directories.
- Validated ASCII hex source characters before uppercasing so Unicode case
  expansion cannot turn malformed input into accepted color data.
- Added hosted XCTest coverage proving fully transparent RGBA is a valid
  failable parse and does not take the gray compatibility fallback.
- Added public `parseHexColor(_:) -> UIColor?` so callers can distinguish
  malformed input from a valid gray color while both existing `toColor` call
  shapes retain their gray compatibility fallback.

## 2026-06-12

- Added hosted XCTest coverage for the deprecated `toColor(hex:)` call shape
  and verified that it delegates through full RGBA component parsing.
- Migrated the parser and XCTest target from Swift 2-era syntax to Swift 5 while
  preserving unlabeled calls and a deprecated labeled compatibility wrapper.
- Raised the Xcode project deployment floor to iOS 12 and made `build.sh`
  discover an available simulator when no destination override is provided.
- Aligned CocoaPods compatibility metadata with Swift 5 and iOS 12 while
  leaving release versioning unchanged.
- Changed hosted macOS validation from project listing only to the real XCTest
  suite through `make test`, with checkout credential persistence disabled.
- Removed the obsolete Xcode 7 Travis job so the current GitHub Actions XCTest
  workflow is the sole hosted validation contract.

## 2026-06-10

- Completed the alpha parsing test matrix for `0x` and `#0x` prefixes at both
  shorthand and full RGBA widths.
- Added pinned macOS GitHub Actions validation for parser/source guardrails and
  current-Xcode project parsing.

## 2026-06-09

- Added coverage for prefixed shorthand and RGBA alpha forms such as `0xRGBA`
  and `#0xRRGGBBAA`.
- Added `make lint`, `make test`, and `make build` aliases so local verification
  has the expected pre-push gate targets in addition to `make check`.
- Added parser support and focused coverage for three-character RGB shorthand
  strings such as `#F0A`, while preserving gray fallback for malformed lengths.
- Added parser support and focused coverage for RGBA alpha strings such as
  `#F0A8` and `#33669980`.
- Rejected signed-looking and other non-hex characters before scanner
  conversion so malformed values stay on the gray fallback path.
- Added explicit coverage and docs for `#0x`-prefixed RGB strings, which
  normalize through the same parser path as `0xRRGGBB`.
- Updated invalid-length coverage to use unsupported lengths now that
  four-character RGBA shorthand is valid.

## 2026-06-08

- Added `make check` for static Xcode, podspec, plist, and parser guardrails.
- Kept the package API consumable by exposing the public `toColor(hex:)` function.
- Rejected partial `NSScanner.scanHexInt` parses so invalid hex strings return gray.
- Replaced the placeholder performance test with focused valid and invalid hex parser tests.
- Added parser coverage for whitespace and newline trimming.
- Added parser support and coverage for `0x`-prefixed RGB strings.
- Made `build.sh` POSIX-safe and configurable through Xcode destination environment variables.
