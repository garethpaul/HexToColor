# HexToColor

<!-- README-OVERVIEW-IMAGE -->
![Project overview](docs/readme-overview.svg)

## Overview

`garethpaul/HexToColor` is an Apple platform application or Objective-C/Swift sample. Convenience Methods for UIColor

This README is based on the checked-in source, manifests, scripts, and repository metadata on the `master` branch. The project language mix found during review was: Swift (2), C/C++ headers (1), shell (1).

## Repository Contents

- `CHANGES.md` - concise history of maintenance changes
- `Makefile` - local verification entry point
- `README.md` - project overview and local usage notes
- `build.sh`
- `HexToColor` - source or example code
- `HexToColor.xcodeproj` - Xcode project file
- `HexToColorTests` - source or example code
- `HexToColor.podspec` - CocoaPods metadata
- `scripts/check-baseline.py` - static parser and Xcode metadata checks
- `SECURITY.md` - security reporting and disclosure guidance
- `VISION.md` - project direction and maintenance guardrails

Additional scan context:

- Source directories: HexToColor, HexToColorTests
- Dependency and build manifests: HexToColor.podspec
- Entry points or build surfaces: Makefile, build.sh, HexToColor.xcodeproj
- Test-looking files: HexToColorTests/HexToColorTests.swift, HexToColorTests/Info.plist

## Getting Started

### Prerequisites

- Git
- macOS with Xcode for building Apple platform projects

### Setup

```bash
git clone https://github.com/garethpaul/HexToColor.git
cd HexToColor
```

The setup commands above are derived from repository files. Legacy mobile, Python, or JavaScript samples may require older SDKs or package versions than a modern workstation uses by default.

## Running or Using the Project

- Open `HexToColor.xcodeproj` in Xcode, choose the app or sample scheme, and run it on the matching simulator/device.
- Current revisions that contain `Package.swift` can be added through Xcode's
  Swift Package Manager integration using this repository URL. The existing
  `0.0.1` tag predates the manifest, so select a later revision or future tag.
  The package supports UIKit on iOS 12+ and AppKit on macOS 10.13+ through the
  shared `HexColor` type alias.
- Run `make test` or `./build.sh` when the required platform toolchain is
  installed. The script selects an available iPhone by its unique simulator ID
  unless `IOS_DESTINATION` or `IOS_SIMULATOR_NAME` is set.
- GitHub Actions runs `make test` on macOS, executing Swift package tests under
  AppKit and compiling the Swift 5 framework at its iOS 12 deployment floor for
  the real XCTest suite on an iOS simulator. The checkout step does not persist checkout credentials.
- The obsolete Xcode 7 Travis job is retired, leaving one current hosted
  verification path.

## Testing and Verification

- Run `make lint` or `make check` for static parser, plist, podspec,
  build-script, and Xcode project guardrails. Run `make test` or `make build`
  for those checks plus Swift package tests when Swift is installed
  and the XCTest suite when Xcode is installed.
- Xcode's test action or `xcodebuild test` with the appropriate scheme and destination
- Use `parseHexColor(_:)` when malformed input must be distinguishable from a
  valid gray color; it returns `nil` on failure. The compatibility
  `toColor(_:)` API and deprecated `toColor(hex:)` call shape retain the gray
  fallback. Hosted XCTest executes the labeled path against RGBA parsing so
  compatibility is not only checked statically.
  Surrounding ASCII space, tab, carriage return, and line feed are trimmed;
  other Unicode whitespace and control characters are rejected.
  RGB, RGBA, RRGGBB, and RRGGBBAA payloads are supported with no prefix, `#`,
  `0x`/`0X`, or the legacy `#0x`/`#0X` prefix. Hex digits are ASCII and
  case-insensitive. The final component is alpha for RGBA inputs; RGB alpha
  defaults to opaque, and
  invalid hex strings fall back to the platform gray color. Unsupported lengths
stay on the gray fallback path. Signed, fullwidth, homoglyph, control, or
otherwise non-hex characters are rejected directly from UTF-8 bytes before any
Unicode normalization. The exact parser does not permit partial or overflowing
scanner parses. Tests cover both `0x` and `#0x` prefixes
  at shorthand and full RGBA widths. Fully transparent RGBA remains a valid
  non-`nil` parse and does not take the gray compatibility fallback.

When the required SDK or runtime is unavailable, use static checks and source review first, then verify on a machine that has the matching platform toolchain.

This library creates color values only. It does not create views, set
accessibility labels, or make color-only status communication accessible;
callers remain responsible for labels, contrast, and non-color cues.

## Configuration and Secrets

- No required secret or credential file was identified in the repository scan. If you add integrations later, keep secrets out of git.

## Security and Privacy Notes

- Review changes touching network requests, sockets, or service endpoints; examples from the scan include HexToColor/Info.plist, HexToColorTests/Info.plist.
- Review changes touching file, media, JSON, XML, CSV, OCR, or data parsing; examples from the scan include HexToColor/Info.plist, HexToColorTests/Info.plist.

## Maintenance Notes

- See `docs/plans/2026-06-10-hosted-project-validation.md` for the hosted Xcode
  project parsing boundary.
- See `docs/plans/2026-06-12-swift5-xctest-modernization.md` for the current
  Swift language, iOS deployment, simulator discovery, and hosted XCTest gate.
- The CocoaPods specification declares Swift 5 and iOS 12 compatibility; its
  release version and source tag remain at 0.0.1 until a future release.
- This looks like an Apple platform project or sample. Xcode, Swift, CocoaPods, and deployment target versions may need to match the original project era.
- Set `IOS_SIMULATOR_NAME` or `IOS_DESTINATION` to override the automatically
  selected available iPhone simulator used by `./build.sh`.
- Every Make verification target derives the checkout root from the loaded
  Makefile, so an absolute Makefile path works from any working directory.
- See `SECURITY.md` for vulnerability reporting and safe research guidance.
- See `VISION.md` for project direction and contribution guardrails.
- See `docs/plans/2026-06-08-hextocolor-whitespace-baseline.md` for the current whitespace parsing guardrail.
- See `docs/plans/2026-06-08-hextocolor-zero-x-prefix.md` for the current `0x` prefix parsing guardrail.
- See `docs/plans/2026-06-09-hextocolor-rgb-shorthand.md` for the current shorthand parsing guardrail.
- See `docs/plans/2026-06-09-hextocolor-signed-character-guard.md` for the current signed-character parsing guardrail.
- See `docs/plans/2026-06-09-hextocolor-hash-zero-x-prefix.md` for the current
  hash-prefixed `0x` normalization guardrail.
- See `docs/plans/2026-06-09-hextocolor-invalid-length-coverage.md` for
  unsupported lengths now that RGBA shorthand is valid.
- See `docs/plans/2026-06-09-hextocolor-prefixed-alpha-coverage.md` for
  prefixed shorthand and RGBA alpha coverage.
- See `docs/plans/2026-06-10-hextocolor-prefix-alpha-matrix.md` for the complete
  `0x`/`#0x` shorthand and full RGBA prefix matrix.
- See `docs/plans/2026-06-12-labeled-api-runtime-coverage.md` for executed
  coverage of the deprecated labeled API.
- See `docs/plans/2026-06-09-make-gate-aliases.md` for local verification
  target guardrails.
- See `docs/plans/2026-06-17-001-feat-swift-package-manager-plan.md` for the
  Swift Package Manager product, target, and hosted manifest-validation contract.

## Contributing

Keep changes small and tied to the project that is already present in this repository. For code changes, document the toolchain used, avoid committing generated dependency directories or local configuration, and update this README when setup or verification steps change.
