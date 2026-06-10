# Hosted Project Validation

status: completed

## Context

HexToColor had deterministic parser/source checks and an installed-Xcode
project listing, but no hosted workflow. The legacy `build.sh` defaults to an
iPhone 5 simulator and should remain an explicit compatibility test rather than
the default current-Xcode gate.

## Changes

- Added pinned, least-privilege macOS GitHub Actions validation for pushes,
  pull requests, and manual runs.
- Run `make check` on fixed `macos-15`, including current-Xcode project parsing,
  with cancellation of superseded runs and a timeout.
- Kept legacy simulator tests explicit through configurable `build.sh`.

## Verification

- `make check`
- Workflow YAML parse
- Hosted `macos-15` GitHub Actions run
