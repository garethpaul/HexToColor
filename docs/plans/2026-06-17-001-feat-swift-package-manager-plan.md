---
title: "feat: Add Swift Package Manager distribution"
type: feat
date: 2026-06-17
status: completed
---

# feat: Add Swift Package Manager distribution

## Summary

Add a Swift Package Manager manifest that exposes the existing `HexToColor`
module and XCTest suite without moving source files or replacing the current
Xcode and CocoaPods distribution paths.

---

## Problem Frame

The library can currently be integrated through its Xcode project or podspec,
but it has no `Package.swift`. Modern Xcode consumers therefore cannot add the
repository as a native Swift package, and hosted verification cannot detect a
stale or malformed package manifest.

---

## Requirements

- R1. The repository must expose one automatic `HexToColor` library product
  backed by the existing Swift source.
- R2. The package must preserve the documented iOS 12 deployment floor and
  Swift 5 language compatibility.
- R3. The existing XCTest file must be represented as a package test target
  without relocating project files or including plist/header metadata as
  sources.
- R4. Hosted `make test` must parse the package manifest before running the
  current Xcode project suite; environments without Swift must report a
  truthful skip while retaining static verification.
- R5. Maintained checks and documentation must reject missing products,
  incorrect paths, weakened platform/language declarations, or removal of the
  package-manifest gate.

---

## Key Technical Decisions

- **Use custom target paths:** preserve the repository's existing
  `HexToColor/` and `HexToColorTests/` layout rather than introducing parallel
  `Sources/` and `Tests/` copies.
- **List Swift sources explicitly:** include only `Hex.swift` and
  `HexToColorTests.swift`, keeping plist and header metadata outside SwiftPM
  target discovery.
- **Leave library linkage automatic:** allow consuming applications to choose
  static or dynamic linkage instead of imposing a new binary contract.
- **Validate the manifest through the existing Make surface:** hosted macOS
  already executes `make test`, so package parsing belongs there rather than in
  a second workflow job.

---

## Implementation Units

### U1. Define the Swift package

- **Goal:** Make the repository consumable as a Swift package without changing
  public color parsing behavior.
- **Requirements:** R1, R2, R3.
- **Files:** `Package.swift`.
- **Approach:** Declare one iOS 12 library product, a source target over the
  current implementation file, and an XCTest target over the current test
  file, with Swift 5 language compatibility and no external dependencies.
- **Test scenarios:** Manifest output identifies the package, automatic library
  product, source and test targets, exact custom paths/sources, iOS 12 minimum,
  and Swift 5 mode.
- **Verification:** SwiftPM can parse the package graph on hosted macOS without
  source relocation or generated files.

### U2. Add package-manifest verification

- **Goal:** Make SwiftPM metadata part of every maintained test/build gate.
- **Requirements:** R4, R5.
- **Dependencies:** U1.
- **Files:** `Makefile`, `scripts/check-baseline.py`.
- **Approach:** Run `swift package dump-package` when Swift is installed,
  retain the existing Xcode availability behavior, and add exact static
  contracts for the manifest and Make integration.
- **Test scenarios:** Static mutations remove or alter the library product,
  deployment floor, target source/path, Swift language mode, or Make command;
  each mutation fails for its intended reason. Local Linux gates retain a
  truthful Swift/XCTest skip, while hosted macOS executes both.
- **Verification:** All Make aliases and external-directory invocation pass;
  the macOS workflow reaches package parsing through `make test`.

### U3. Document the supported distribution path

- **Goal:** Give consumers and maintainers an accurate SwiftPM integration and
  validation contract.
- **Requirements:** R4, R5.
- **Dependencies:** U1, U2.
- **Files:** `README.md`, `VISION.md`, `CHANGES.md`,
  `docs/plans/2026-06-17-001-feat-swift-package-manager-plan.md`.
- **Approach:** Record SwiftPM alongside Xcode/CocoaPods, explain the preserved
  iOS/Swift compatibility and hosted authority, and capture completed local and
  hosted evidence without claiming a package release.
- **Test scenarios:** Baseline checks reject stale guidance or incomplete plan
  evidence.
- **Verification:** Guidance, changelog, and completed-plan contracts agree
  with the shipped manifest and validation behavior.

---

## Scope Boundaries

### Deferred to Follow-Up Work

- Publishing a tagged package release or changing the podspec version.
- Restructuring sources into conventional `Sources/` and `Tests/` directories.

### Out of Scope

- Parser behavior, public API signatures, supported hex formats, or gray
  fallback semantics.
- Removing or regenerating the Xcode project, schemes, podspec, or existing
  hosted XCTest workflow.
- Adding package dependencies, resources, binary targets, plugins, or new
  Apple platforms.

---

## Risks And Dependencies

- Linux cannot compile this UIKit module with the host SDK, so local validation
  is limited to static contracts when Swift/Xcode is unavailable; hosted macOS
  remains the executable package-manifest authority.
- A custom-path manifest can silently include unintended files unless sources
  are explicit and mutation-tested.
- The Swift 5.9 tools declaration requires a maintained Xcode release while
  preserving Swift 5 source mode and the library's iOS 12 deployment floor.

---

## Sources And Research

- [Swift Package manifest reference](https://docs.swift.org/package-manager/PackageDescription/PackageDescription.html)
  defines library products, iOS platform floors, test targets, and Swift tools
  compatibility.
- [SwiftPM target path documentation](https://docs.swift.org/swiftpm/documentation/packagedescription/target/path/)
  supports repo-relative custom source locations and explicit exclusions or
  source lists.
- [Swift packages overview](https://www.swift.org/packages/) describes SwiftPM
  as the native package distribution path integrated with current Xcode.

---

## Work Completed

- Added one automatic `HexToColor` library product over the existing
  `HexToColor/Hex.swift` source and one test target over the existing XCTest
  file, with an iOS 12 platform floor and Swift 5 language mode.
- Extended `make test` to parse the package manifest when Swift is available,
  while preserving the existing Xcode availability check and every Make alias.
- Added maintained static contracts for the package graph, Make integration,
  consumer guidance, release boundary, changelog, and completed plan evidence.

## Verification Completed

- All four Make gates passed from the repository root: `make lint`,
  `make test`, `make build`, and `make check`.
- The external-directory `make -f "$REPOSITORY/Makefile" check` invocation
  passed, preserving location-independent validation.
- Swift manifest parsing was skipped because `swift` is not installed locally;
  the hosted macOS Make gate executes the same command when Swift is present.
- XCTest was skipped because `xcodebuild` is not installed locally; parser and
  test behavior were not modified by this distribution-only change.
- `sh -n build.sh`, `ruby -c HexToColor.podspec`,
  `python3 -m py_compile scripts/check-baseline.py`, and `git diff --check`
  passed.
- Six isolated hostile mutations were rejected for the library product, iOS
  floor, source path, Swift language mode, Make manifest command, and README
  release-boundary guidance.
