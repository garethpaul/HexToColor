# Failable Hex Color Parser

status: planned

## Context

The public `toColor` API returns `.gray` for malformed input. That preserves the
original convenience behavior, but callers cannot distinguish a parse failure
from a valid gray color such as `#808080`.

## Priority

An additive failable API gives callers explicit validation without breaking the
existing unlabeled or deprecated labeled call shapes. One shared parser path
also prevents valid-format behavior from drifting between APIs.

## Requirements

- R1. Add public `parseHexColor(_:) -> UIColor?` for explicit parse success or
  failure.
- R2. Preserve whitespace trimming, `#`, `0x`, and `#0x` prefixes, RGB/RGBA
  shorthand, full RGB/RGBA widths, and lowercase input.
- R3. Return `nil` for unsupported lengths, non-hex characters, signed-looking
  input, or incomplete scanner consumption.
- R4. Keep `toColor(_:)` returning `.gray` on failure by delegating to the
  failable parser.
- R5. Keep deprecated `toColor(hex:)` delegating through the compatibility path.
- R6. Add XCTest coverage that distinguishes valid gray from malformed input
  and static contracts that reject duplicated parser logic or wrapper drift.

## Implementation Units

### U1. Extract the failable public parser

- **Files:** `HexToColor/Hex.swift`
- Move normalization, validation, scanning, and component conversion into
  `parseHexColor(_:)`; keep wrappers minimal.

### U2. Extend behavior coverage

- **Files:** `HexToColorTests/HexToColorTests.swift`,
  `scripts/check-baseline.py`
- Prove valid gray returns a color, malformed input returns `nil`, and existing
  wrapper behavior remains unchanged.

### U3. Document the additive API

- **Files:** `README.md`, `SECURITY.md`, `VISION.md`, `CHANGES.md`
- Explain when callers should use explicit parse failure versus compatibility
  fallback.

## Scope Boundaries

- Do not change supported input syntax or RGBA component ordering.
- Do not remove or rename either existing `toColor` function.
- Do not change package version or deployment metadata without a release.

## Verification

- `make lint`
- `make test`
- `make build`
- `make check`
- `sh -n build.sh`
- `ruby -c HexToColor.podspec`
- `git diff --check`
- Hostile mutations removing the optional return, parser delegation, focused
  tests, completed status, or verification evidence must be rejected.
