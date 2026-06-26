# AGENTS.md

## Repository purpose

`garethpaul/HexToColor` is an Apple platform application or Objective-C/Swift sample. Convenience Methods for UIColor

## Project structure

- `Makefile` - repository verification targets
- `scripts` - baseline checks and helper scripts
- `docs` - plans, notes, and generated README assets
- `HexToColor.xcodeproj` - Xcode project
- `HexToColor` - repository source or sample assets
- `HexToColorTests` - repository source or sample assets

## Development commands

- Install dependencies: no repository-specific install command is documented.
- Full baseline: `make check`
- Hosted/local XCTest gate: `make test`
- Build alias: `make build`
- Local Apple development: `open HexToColor.xcodeproj`
- If a command above skips because a platform toolchain is missing, verify on a machine with that SDK before claiming platform behavior is tested.

## Coding conventions

- Language mix noted in the README: Swift (2), C/C++ headers (1), shell (1).
- Preserve legacy Xcode project settings and signing assumptions unless the change is explicitly about modernization.

## Testing guidance

- Test-related files detected: `HexToColor.podspec`, `HexToColor.xcodeproj/xcshareddata/xcschemes/HexToColorTests.xcscheme`, `HexToColorTests/HexToColorTests.swift`
- Start with the narrowest relevant test or Make target, then run `make check` before handing off if the change is not documentation-only.
- Keep README verification notes in sync when commands, fixtures, or supported toolchains change.

## PR / change guidance

- Keep diffs focused on the requested repository and avoid unrelated modernization or formatting churn.
- Preserve public APIs, sample behavior, file formats, and documented environment variables unless the task explicitly changes them.
- Update tests, README notes, or docs/plans when behavior, security posture, or validation commands change.
- Call out skipped platform validation, legacy toolchain assumptions, and any risky files touched in the final summary.

## Safety and gotchas

- No required secret or credential file was identified in the repository scan. If you add integrations later, keep secrets out of git.
- This looks like an Apple platform project or sample. Xcode, Swift, CocoaPods, and deployment target versions may need to match the original project era.
- Set `IOS_SIMULATOR_NAME` or `IOS_DESTINATION` to override the automatically discovered available iPhone simulator.
- The project and test targets use Swift 5 with an iOS 12 deployment floor; preserve the deprecated labeled `toColor(hex:)` wrapper when changing the unlabeled public API.
- The parser accepts exact ASCII hex bytes and trims only ASCII space, tab, carriage return, and line feed; reject Unicode and control input before Unicode normalization.
- Validate caller-supplied ASCII hex characters before Unicode case normalization so non-ASCII expansion cannot create valid input.
- See `SECURITY.md` for vulnerability reporting and safe research guidance.
- See `VISION.md` for project direction and contribution guardrails.
- See `docs/plans/2026-06-08-hextocolor-whitespace-baseline.md` for the current whitespace parsing guardrail.
- See `docs/plans/2026-06-25-parser-case-malformed-coverage.md` before proposing
  new case or malformed-input tests; it records the completed matrix and the
  remaining requirement to justify genuinely new parser behavior.

## Agent workflow

1. Inspect the README, Makefile, manifests, and the files directly related to the request.
2. Make the smallest source or docs change that satisfies the task; avoid generated, vendored, or local-environment files unless required.
3. Run the narrowest useful validation first, then `make check` or the documented package/platform gate when available.
4. If a required SDK, service credential, or external runtime is unavailable, record the skipped command and why.
5. Summarize changed files, commands run, and remaining risks or follow-up validation.
