# HexToColor Invalid Length Coverage

status: completed

## Context

`toColor(hex:)` now accepts three-character RGB shorthand, four-character RGBA
shorthand, six-character RGB, and eight-character RGBA inputs. The previous
invalid-length test used `#FFFF`, which is now a valid RGBA shorthand color.

## Objectives

- Keep unsupported hex lengths on the documented gray fallback path.
- Update invalid-length XCTest coverage to avoid valid RGBA shorthand input.
- Extend the static baseline so unsupported-length coverage remains visible in
  tests and documentation.
- Document the behavior in README, VISION, and CHANGES.

## Verification

- `python3 scripts/check-baseline.py`
- `make lint`
- `make test`
- `make build`
- `make check`
- `git diff --check`
