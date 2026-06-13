#!/usr/bin/env python3

from pathlib import Path
import plistlib
import re
import shutil
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
PLAN_DIR = ROOT / "docs/plans"
SWIFT5_PLAN = "docs/plans/2026-06-12-swift5-xctest-modernization.md"
LABELED_API_PLAN = "docs/plans/2026-06-12-labeled-api-runtime-coverage.md"
FAILABLE_PARSER_PLAN = "docs/plans/2026-06-13-hextocolor-failable-parser.md"
TRANSPARENT_ALPHA_PLAN = "docs/plans/2026-06-13-hextocolor-transparent-alpha-boundary.md"
EXPECTED_WORKFLOW = """name: Check

on:
  pull_request:
  push:
  workflow_dispatch:

permissions:
  contents: read

concurrency:
  group: check-${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  check:
    runs-on: macos-15
    timeout-minutes: 10
    steps:
      - name: Check out repository
        uses: actions/checkout@df4cb1c069e1874edd31b4311f1884172cec0e10 # v6.0.3
        with:
          persist-credentials: false
      - name: Run parser and XCTest baseline
        run: make test
"""
EXPECTED_MAKEFILE = """.PHONY: build check lint test

lint: check

test: check
\t@if command -v xcodebuild >/dev/null 2>&1; then ./build.sh; else printf '%s\\n' "Skipping XCTest: xcodebuild is not installed."; fi

build: test

check:
\tpython3 scripts/check-baseline.py
"""


def fail(message):
    print(f"check-baseline: {message}", file=sys.stderr)
    sys.exit(1)


def read(path):
    full_path = ROOT / path
    if not full_path.is_file():
        fail(f"missing required file: {path}")
    return full_path.read_text(errors="replace")


def require(condition, message):
    if not condition:
        fail(message)


def require_all(text, tokens, message):
    missing = [token for token in tokens if token not in text]
    require(not missing, f"{message}; missing: {', '.join(missing)}")


def lint_plist(path):
    with (ROOT / path).open("rb") as plist_file:
        plistlib.load(plist_file)


required_files = [
    ".gitignore",
    "AGENTS.md",
    "CHANGES.md",
    "LICENSE",
    "Makefile",
    "README.md",
    "SECURITY.md",
    "VISION.md",
    "build.sh",
    ".github/workflows/check.yml",
    "HexToColor.podspec",
    "HexToColor.xcodeproj/project.pbxproj",
    "HexToColor.xcodeproj/xcshareddata/xcschemes/HexToColor.xcscheme",
    "HexToColor.xcodeproj/xcshareddata/xcschemes/HexToColorTests.xcscheme",
    "HexToColor/Hex.swift",
    "HexToColor/HexToColor.h",
    "HexToColor/Info.plist",
    "HexToColorTests/HexToColorTests.swift",
    "HexToColorTests/Info.plist",
    "docs/plans/2026-06-08-hextocolor-baseline.md",
    "docs/plans/2026-06-08-hextocolor-whitespace-baseline.md",
    "docs/plans/2026-06-08-hextocolor-zero-x-prefix.md",
    "docs/plans/2026-06-09-hextocolor-rgb-shorthand.md",
    "docs/plans/2026-06-09-hextocolor-rgba-alpha.md",
    "docs/plans/2026-06-09-hextocolor-signed-character-guard.md",
    "docs/plans/2026-06-09-hextocolor-hash-zero-x-prefix.md",
    "docs/plans/2026-06-09-make-gate-aliases.md",
    "docs/plans/2026-06-09-hextocolor-invalid-length-coverage.md",
    "docs/plans/2026-06-09-hextocolor-prefixed-alpha-coverage.md",
    "docs/plans/2026-06-10-hextocolor-prefix-alpha-matrix.md",
    "docs/plans/2026-06-10-hosted-project-validation.md",
    SWIFT5_PLAN,
    LABELED_API_PLAN,
    FAILABLE_PARSER_PLAN,
    TRANSPARENT_ALPHA_PLAN,
]

for required_file in required_files:
    read(required_file)

require(not (ROOT / ".travis.yml").exists(),
        "obsolete Xcode 7 Travis configuration must stay removed")
subprocess.check_call(["sh", "-n", "build.sh"], cwd=str(ROOT))
require((ROOT / "build.sh").stat().st_mode & 0o111, "build.sh must be executable")
lint_plist("HexToColor/Info.plist")
lint_plist("HexToColorTests/Info.plist")

hex_source = read("HexToColor/Hex.swift")
tests = read("HexToColorTests/HexToColorTests.swift")
build_script = read("build.sh")
makefile = read("Makefile")
podspec = read("HexToColor.podspec")
project = read("HexToColor.xcodeproj/project.pbxproj")
readme = read("README.md")
security = read("SECURITY.md")
vision = read("VISION.md")
changes = read("CHANGES.md")
gitignore = read(".gitignore")
workflow = read(".github/workflows/check.yml")
swift5_plan = read(SWIFT5_PLAN)
labeled_api_plan = read(LABELED_API_PLAN)
failable_parser_plan = read(FAILABLE_PARSER_PLAN)
transparent_alpha_plan = read(TRANSPARENT_ALPHA_PLAN)

require_all(hex_source, [
    "public func parseHexColor(_ hex: String) -> UIColor?",
    "public func toColor(_ hex: String) -> UIColor",
    'trimmingCharacters(in: .whitespacesAndNewlines)',
    'colorString.hasPrefix("#")',
    'colorString.hasPrefix("0X")',
    "colorString.removeFirst()",
    "colorString.removeFirst(2)",
    "colorString.count == 3 || colorString.count == 4",
    'colorString.map { "\\($0)\\($0)" }.joined()',
    "colorString.count == 6 || colorString.count == 8",
    'CharacterSet(charactersIn: "0123456789ABCDEF")',
    "allowedHexCharacters.inverted",
    "scanner.scanHexInt64(&colorValue)",
    "scanner.isAtEnd",
    "alphaValue = colorValue & 0x000000FF",
    "alphaValue = 0xFF",
    "return nil",
    "return parseHexColor(hex) ?? .gray",
    '@available(*, deprecated, renamed: "toColor(_:)")',
    "public func toColor(hex: String) -> UIColor",
    "return toColor(hex)",
], "Swift 5 parser contract is incomplete")
require(hex_source.count("return nil") == 3,
        "all malformed parser paths must return nil from the failable API")
require(hex_source.count("?? .gray") == 1,
        "only the compatibility API may apply the gray fallback")

for test_name in [
    "testWhite",
    "testLowercaseWithoutHash",
    "testZeroXPrefix",
    "testHashZeroXPrefix",
    "testZeroXFourDigitShorthandWithAlpha",
    "testZeroXEightDigitRGBAWithAlpha",
    "testHashZeroXFourDigitShorthandWithAlpha",
    "testHashZeroXEightDigitRGBAWithAlpha",
    "testThreeDigitShorthand",
    "testFourDigitShorthandWithAlpha",
    "testEightDigitRGBAWithAlpha",
    "testDeprecatedLabeledAPICompatibility",
    "testFailableParserDistinguishesValidGrayFromInvalidInput",
    "testTransparentRGBAIsValidAtBothWidths",
    "testTrimsWhitespaceAndNewlines",
    "testInvalidLengthReturnsGray",
    "testInvalidCharactersReturnGray",
    "testSignedHexReturnsGray",
]:
    require(test_name in tests, f"missing color parser test: {test_name}")
for prefixed_alpha_input in ["0xF0A8", "0x33669980", "#0xF0A8", "#0x33669980"]:
    require(f'toColor("{prefixed_alpha_input}")' in tests,
            f"missing prefixed alpha input coverage: {prefixed_alpha_input}")
require_all(tests, ["func assertColor(_ color: UIColor", "accuracy:"],
            "XCTest helpers must use current Swift assertion syntax")
require("XCTAssertEqualWithAccuracy" not in tests,
        "Swift 2 XCTest assertion syntax must stay removed")
require("255.0, green: 255.0" not in tests,
        "tests must compare UIColor components in the 0...1 range")
require('toColor("#FFFF")' not in tests and 'toColor("#FF")' in tests and
        'toColor("#FFFFF")' in tests and 'toColor("#FFFFFFFFF")' in tests,
        "invalid-length tests must use unsupported lengths")
require('toColor(hex: "#33669980")' in tests,
        "deprecated labeled API must be exercised by XCTest")
require_all(tests, [
    'parseHexColor("#808080")',
    'XCTAssertNil(parseHexColor("#FF"))',
    'XCTAssertNil(parseHexColor("#FFFFFG"))',
    'XCTAssertNil(parseHexColor("-FFFFF"))',
], "failable parser must distinguish valid gray from malformed input")
require_all(tests, [
    'for input in ["#0000", "#00000000"]',
    "let parsed = parseHexColor(input)",
    "XCTAssertNotNil(parsed)",
    "assertColor(toColor(input)",
], "transparent RGBA must remain a successful failable and compatibility parse")
require(tests.count("alpha: 0.0") == 2,
        "transparent RGBA coverage must assert zero alpha for both parser paths")

require_all(build_script, [
    "set -eu",
    "IOS_DESTINATION",
    "IOS_SIMULATOR_NAME",
    "xcrun simctl list devices available",
    "No available iPhone simulator was found.",
    '-destination "$DESTINATION"',
    "build test",
], "build.sh must discover or accept a current simulator destination")
require("iPhone 5" not in build_script,
        "build.sh must not restore a retired fixed simulator default")

require(project.count("SWIFT_VERSION = 5.0;") == 4,
        "framework and test configurations must explicitly use Swift 5")
require(project.count("IPHONEOS_DEPLOYMENT_TARGET = 12.0;") == 4,
        "all project configurations must retain the iOS 12 deployment floor")
require("SWIFT_VERSION = 2" not in project,
        "Swift 2 project settings must stay removed")

require(makefile == EXPECTED_MAKEFILE,
        "Makefile must exactly preserve static and executable verification gates")
require_all(podspec, [
    's.platform     = :ios, "12.0"',
    's.swift_version = "5.0"',
    's.version      = "0.0.1"',
    's.social_media_url   = "https://twitter.com/gpj"',
], "podspec must declare current compatibility without inventing a release")

require(workflow == EXPECTED_WORKFLOW,
        "GitHub Actions must exactly match the bounded, least-privilege macOS XCTest workflow")

require_all(readme.lower(), [
    "make lint", "make test", "make build", "make check", "swift 5", "ios 12",
    "invalid hex", "whitespace", "0x", "shorthand", "alpha", "unsupported lengths",
    "#0x", "0xrgba", "#0xrrggbbaa", "non-hex", "signed",
    "parsehexcolor(_:)", "returns `nil`", "valid gray color",
    "fully transparent rgba",
    "persist checkout credentials", "real xctest suite",
], "README must document parser behavior and executable hosted verification")
require_all(vision.lower(), [
    "make lint", "make test", "make build", "make check", "swift 5", "ios 12",
    "invalid hex", "whitespace", "0x", "shorthand", "alpha", "unsupported lengths",
    "#0x", "0x-prefixed shorthand and rgba", "non-hex", "real xctest suite",
    "parsehexcolor(_:)", "explicit failure",
    "fully transparent rgba",
], "VISION must describe the current parser and hosted validation baseline")
require_all(changes, [
    "public", "toColor(hex:)", "scanHexInt", "make lint", "make test", "make build",
    "make check", "whitespace", "0x", "shorthand", "alpha", "non-hex",
    "unsupported lengths", "#0x", "prefixed shorthand and RGBA", "Swift 5", "iOS 12",
    "real XCTest", "credential persistence disabled",
    "parseHexColor(_:)", "valid gray color",
    "fully transparent RGBA",
], "CHANGES must record parser and current-Xcode verification work")
require_all(security, ["Security Policy", "privately", "malformed", "parseHexColor(_:)", "reported", "valid gray color"],
            "SECURITY must retain reporting and malformed-input guidance")

completed_plans = [
    "docs/plans/2026-06-08-hextocolor-baseline.md",
    "docs/plans/2026-06-08-hextocolor-whitespace-baseline.md",
    "docs/plans/2026-06-08-hextocolor-zero-x-prefix.md",
    "docs/plans/2026-06-09-hextocolor-rgb-shorthand.md",
    "docs/plans/2026-06-09-hextocolor-rgba-alpha.md",
    "docs/plans/2026-06-09-hextocolor-signed-character-guard.md",
    "docs/plans/2026-06-09-hextocolor-hash-zero-x-prefix.md",
    "docs/plans/2026-06-09-make-gate-aliases.md",
    "docs/plans/2026-06-09-hextocolor-invalid-length-coverage.md",
    "docs/plans/2026-06-09-hextocolor-prefixed-alpha-coverage.md",
    "docs/plans/2026-06-10-hextocolor-prefix-alpha-matrix.md",
    "docs/plans/2026-06-10-hosted-project-validation.md",
    SWIFT5_PLAN,
    LABELED_API_PLAN,
    FAILABLE_PARSER_PLAN,
    TRANSPARENT_ALPHA_PLAN,
]
for plan_path in completed_plans:
    require("status: completed" in read(plan_path),
            f"completed plan marker missing: {plan_path}")
require_all(swift5_plan, [
    "make test", "Swift 5", "iOS 12", "persisted checkout credentials",
    "simulator discovery", "git diff --check",
], "Swift 5 modernization plan must record its completed contract")
labeled_api_statuses = re.findall(r"^status: .+$", labeled_api_plan, flags=re.MULTILINE)
labeled_api_sections = labeled_api_plan.split("## Verification Completed\n", 1)
labeled_api_verification = labeled_api_sections[1] if len(labeled_api_sections) == 2 else ""
labeled_api_required_evidence = (
    "All four Make gates",
    "push run `27393807170`",
    "pull-request run `27393810000`",
    "push run `27393956378`",
    "CodeQL setup run `27402321858`",
    "mutation removing the labeled invocation",
)
require(labeled_api_statuses == ["status: completed"] and
        all(item in labeled_api_verification for item in labeled_api_required_evidence) and
        re.search(r"\b(?:pending|todo|tbd|not run)\b", labeled_api_verification, re.IGNORECASE) is None,
        "labeled API plan must record completed status and actual verification")
failable_parser_statuses = re.findall(r"^status: .+$", failable_parser_plan, flags=re.MULTILINE)
failable_parser_sections = failable_parser_plan.split("## Verification Completed\n", 1)
failable_parser_verification = failable_parser_sections[1] if len(failable_parser_sections) == 2 else ""
failable_parser_required_evidence = (
    "All four Make gates",
    "XCTest was skipped because `xcodebuild` is",
    "sh -n build.sh",
    "ruby -c HexToColor.podspec",
    "python3 -m py_compile scripts/check-baseline.py",
    "git diff --check",
    "Seven isolated hostile mutations",
)
require(failable_parser_statuses == ["status: completed"] and
        all(item in failable_parser_verification for item in failable_parser_required_evidence) and
        re.search(r"\b(?:pending|todo|tbd|not run)\b", failable_parser_verification, re.IGNORECASE) is None,
        "failable parser plan must record completed status and actual verification")
transparent_alpha_statuses = re.findall(r"^status: .+$", transparent_alpha_plan, flags=re.MULTILINE)
transparent_alpha_sections = transparent_alpha_plan.split("## Verification Completed\n", 1)
transparent_alpha_verification = transparent_alpha_sections[1] if len(transparent_alpha_sections) == 2 else ""
transparent_alpha_required_evidence = (
    "All four Make gates passed",
    "XCTest was skipped because `xcodebuild` is not",
    "sh -n build.sh",
    "ruby -c HexToColor.podspec",
    "workflow YAML parsing",
    "Three isolated hostile mutations were rejected",
    "Hosted macOS XCTest and CodeQL evidence",
)
require(transparent_alpha_statuses == ["status: completed"] and
        all(item in transparent_alpha_verification for item in transparent_alpha_required_evidence) and
        re.search(r"\b(?:pending|todo|tbd|not run)\b", transparent_alpha_verification, re.IGNORECASE) is None,
        "transparent alpha plan must record completed status and actual local verification")

for ignore_entry in ["build/", "DerivedData/", "xcuserdata/", ".DS_Store"]:
    require(ignore_entry in gitignore, f"{ignore_entry} must stay ignored")

if shutil.which("xcodebuild"):
    subprocess.check_call(["xcodebuild", "-list", "-project", "HexToColor.xcodeproj"], cwd=str(ROOT))
else:
    print("check-baseline: xcodebuild not found; skipped Xcode project listing")

print("HexToColor baseline checks passed.")
