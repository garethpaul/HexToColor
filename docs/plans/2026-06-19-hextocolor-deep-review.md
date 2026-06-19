# HexToColor deep review

status: completed

## Scope

Reviewed the complete linear pull-request stack `#3` through `#8`, ending at
commit `11cfdba`, across the public parser APIs, UIKit/Xcode target, Swift package
manifest, AppKit host behavior, tests, Make gates, documentation, and hosted
workflow.

## Findings and provenance

1. Swift Package Manager support in `#8` only parsed the manifest. Executing
   `swift test` failed because `Hex.swift` unconditionally imported UIKit, and
   both target directories emitted unhandled `Info.plist` warnings. This was
   introduced by `11cfdba` when the iOS-only source was exposed as a host-built
   package without an AppKit boundary.
2. The parser trimmed Foundation's Unicode-wide whitespace and newline set.
   Non-breaking space, vertical tab, form feed, and Unicode line separator were
   therefore accepted around otherwise valid colors despite the documented
   ASCII-validation boundary. The permissive trimming originated in `39ae0d3`
   and was carried forward by the later failable-parser and Unicode fixes.
3. Scanner conversion and whole-string normalization were unnecessary after
   exact width validation and obscured the accepted grammar. The replacement
   parses ASCII UTF-8 nibbles directly, preventing partial and overflowing
   scanner behavior by construction.

## Accepted contract

- Payload widths: RGB, RGBA, RRGGBB, and RRGGBBAA.
- Prefixes: none, `#`, `0x`/`0X`, and legacy `#0x`/`#0X`.
- Hex digits: ASCII `0-9`, `A-F`, and `a-f` only.
- Surrounding trim set: ASCII space, tab, carriage return, and line feed only.
- RGBA ordering: alpha is the trailing nibble or byte; RGB defaults to opaque.
- `parseHexColor(_:)` returns `nil` for malformed input. `toColor(_:)` and the
  deprecated `toColor(hex:)` preserve the platform-gray fallback.
- `HexColor` aliases `UIColor` under UIKit and `NSColor` under AppKit.

## Verification completed

- The new whitespace test failed first against the stacked PR head, proving
  acceptance of U+00A0, U+000B, U+000C, and U+2028.
- `make check`, `swift package dump-package`, Swift release build, Swift package
  tests, and iOS simulator XCTest passed locally.
- 25 tests passed under AppKit through SwiftPM and under UIKit through Xcode.
- A 256-value RGBA property loop and full 6-prefix/4-width matrix passed.
- Six isolated hostile mutations were killed: Unicode-whitespace widening,
  accepting `G`, broken prefix consumption, wrong alpha ordering, transparent
  RGB default, and forced gray fallback.
- Root and external-directory Make gates passed.
- Current-tree and 56-commit redacted Gitleaks scans found zero credentials.
- GitHub code-scanning, secret-scanning, and Dependabot open-alert counts were
  all zero.

## Residual risk

- The public `HexColor` type alias is source-compatible with existing UIKit
  callers but is a new exported API symbol; downstream binary compatibility was
  not measured because the project does not enable library evolution.
- CocoaPods remains iOS-only at version `0.0.1`; AppKit support is distributed
  through revisions containing the Swift package manifest until a new tag is
  published.
- No visual UI or accessibility behavior is implemented by this library.
  Callers remain responsible for contrast, labels, and non-color cues.
