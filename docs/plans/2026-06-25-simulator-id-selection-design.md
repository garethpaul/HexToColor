# Simulator ID Selection Design

Status: Approved

## Problem

The default `build.sh` path reads the first available iPhone model name and passes `platform=iOS Simulator,name=...` to `xcodebuild`. A developer with multiple installed iOS runtimes can have the same model name in more than one runtime, making the otherwise automatic destination ambiguous.

## Options

1. Parse the selected device's UDID into a small AWK helper and pass `platform=iOS Simulator,id=...`. This keeps the existing text-based `simctl` dependency, makes the default destination unique, and permits fixture-based portable testing.
2. Keep the inline name parser and add an OS version to the destination. This still depends on coordinating two fields from human-readable output and remains less direct than the unique identifier.
3. Parse `simctl --json` with a new JSON runtime dependency. This is structured but adds unnecessary build-script complexity and tooling assumptions.

## Decision

Use option 1. Preserve `IOS_DESTINATION` and `IOS_SIMULATOR_NAME` exactly as explicit caller overrides; only automatic discovery changes to a UDID.

## Verification

- Add a dependency-free fixture with duplicate iPhone names across two runtimes and require the selector to return the first device UDID.
- Require `build.sh` to use the selector and an `id=` destination in its automatic path.
- Run portable checks locally and the full SwiftPM/Xcode suite in hosted macOS CI.
