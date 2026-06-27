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
UNICODE_NORMALIZATION_PLAN = "docs/plans/2026-06-13-hextocolor-unicode-normalization-boundary.md"
LOCATION_INDEPENDENT_MAKE_PLAN = "docs/plans/2026-06-13-location-independent-make.md"
SWIFT_PACKAGE_PLAN = "docs/plans/2026-06-17-001-feat-swift-package-manager-plan.md"
PARSER_COVERAGE_PLAN = "docs/plans/2026-06-25-parser-case-malformed-coverage.md"
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
EXPECTED_MAKEFILE = """.PHONY: __repository-make-authority build check lint test
.SECONDEXPANSION:

ifneq ($(strip $(MAKEFILES)),)
$(error MAKEFILES must be empty; repository verification requires this Makefile to be loaded alone)
endif
override MAKEFILES :=
ifneq ($(origin MAKEFILE_LIST),file)
$(error MAKEFILE_LIST must not be overridden)
endif
override ROOT := $(shell sed_path=/usr/bin/sed; [ -x "$$sed_path" ] || sed_path=/bin/sed; [ -x "$$sed_path" ] || exit 1; path=$$(printf '%s' '$(subst ','"'"',$(value MAKEFILE_LIST))' | "$$sed_path" 's/^ //'); [ -f "$$path" ] || exit 1; directory=$${path%/*}; [ "$$directory" != "$$path" ] || directory=.; CDPATH= cd -- "$$directory" && /bin/pwd -P)
export ROOT
ifeq ($(strip $(ROOT)),)
$(error repository Makefile must be loaded alone)
endif

build check lint test:: $$(if $$(filter file,$$(origin MAKEFILE_LIST)),,$$(error MAKEFILE_LIST must not be overridden))
build check lint test:: $$(if $$(shell sed_path=/usr/bin/sed && [ -x "$$$$sed_path" ] || sed_path=/bin/sed && [ -x "$$$$sed_path" ] && path=$$$$(printf '%s' '$$(subst ','"'"',$$(MAKEFILE_LIST))' | "$$$$sed_path" 's/^ //') && [ -f "$$$$path" ] && printf '%s' ok),,$$(error repository Makefile must be loaded alone))
build check lint test:: __repository-make-authority

__repository-make-authority::
	@:

lint:: check

test:: check
	@if command -v swift >/dev/null 2>&1; then cd "$(ROOT)" && swift test; else printf '%s\\n' "Skipping Swift package tests: swift is not installed."; fi
	@if command -v xcodebuild >/dev/null 2>&1; then cd "$(ROOT)" && ./build.sh; else printf '%s\\n' "Skipping XCTest: xcodebuild is not installed."; fi

build:: test

check::
	@python3 "$(ROOT)/scripts/check-baseline.py"
	@python3 "$(ROOT)/scripts/test-make-spaced-path.py"
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
    "Package.swift",
    "README.md",
    "SECURITY.md",
    "VISION.md",
    "build.sh",
    "scripts/select-ios-simulator-id.awk",
    "scripts/test-make-spaced-path.py",
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
    UNICODE_NORMALIZATION_PLAN,
    LOCATION_INDEPENDENT_MAKE_PLAN,
    SWIFT_PACKAGE_PLAN,
    PARSER_COVERAGE_PLAN,
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
simulator_selector = read("scripts/select-ios-simulator-id.awk")
makefile = read("Makefile")
package_manifest = read("Package.swift")
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
unicode_normalization_plan = read(UNICODE_NORMALIZATION_PLAN)
location_independent_make_plan = read(LOCATION_INDEPENDENT_MAKE_PLAN)
swift_package_plan = read(SWIFT_PACKAGE_PLAN)
parser_coverage_plan = read(PARSER_COVERAGE_PLAN)

require_all(hex_source, [
    "#if canImport(UIKit)",
    "#elseif canImport(AppKit)",
    "public typealias HexColor = UIColor",
    "public typealias HexColor = NSColor",
    "private let trimmedASCIIWhitespace: Set<UInt8> = [0x09, 0x0A, 0x0D, 0x20]",
    "private func hexNibble(_ byte: UInt8) -> UInt8?",
    "case 0x30...0x39:",
    "case 0x41...0x46:",
    "case 0x61...0x66:",
    "public func parseHexColor(_ hex: String) -> HexColor?",
    "var bytes = hex.utf8[...]",
    "digitCount == 3 || digitCount == 4 || digitCount == 6 || digitCount == 8",
    "guard let digit = hexNibble(byte)",
    "return digits[index] * 0x11",
    "return digits[index * 2] << 4 | digits[index * 2 + 1]",
    "alpha: digitCount == 4 || digitCount == 8 ? component(at: 3) : 0xFF",
    "return nil",
    "return parseHexColor(hex) ?? .gray",
    '@available(*, deprecated, renamed: "toColor(_:)")',
    "public func toColor(hex: String) -> HexColor",
    "return toColor(hex)",
], "Swift 5 parser contract is incomplete")
require(not any(token in hex_source for token in ["Scanner", "CharacterSet", "uppercased()", "trimmingCharacters"]),
        "parser must not normalize Unicode or delegate exact grammar to Scanner")
require(hex_source.count("return nil") == 3,
        "all malformed parser paths must return nil from the failable API")
require(hex_source.count("?? .gray") == 1,
        "only the compatibility API may apply the gray fallback")
require_all(hex_source, [
    "// Parses a hex string into a platform color.",
    "// Converts a hex string into a platform color, falling back to gray for compatibility.",
], "public parser comments must describe the shared UIKit and AppKit color surface")

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
    "testUnicodeCaseExpansionDoesNotCreateValidHex",
    "testTrimsWhitespaceAndNewlines",
    "testOnlyDocumentedASCIIWhitespaceIsTrimmed",
    "testRejectsUnicodeLookalikesAndControlsBeforeParsing",
    "testRejectsPartialOverflowAndMalformedPrefixes",
    "testRGBAUsesTrailingAlphaByte",
    "testAllByteValuesRoundTripThroughRGBAParser",
    "testAcceptedPrefixWidthAndCaseMatrix",
    "testInvalidLengthReturnsGray",
    "testInvalidCharactersReturnGray",
    "testSignedHexReturnsGray",
]:
    require(test_name in tests, f"missing color parser test: {test_name}")
for prefixed_alpha_input in ["0xF0A8", "0x33669980", "#0xF0A8", "#0x33669980"]:
    require(f'toColor("{prefixed_alpha_input}")' in tests,
            f"missing prefixed alpha input coverage: {prefixed_alpha_input}")
require_all(tests, ["func assertColor(_ color: HexColor", "accuracy:"],
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
require('XCTAssertNil(parseHexColor("#ﬀ0000"))' in tests and
        'assertColor(toColor("#ﬀ0000")' in tests,
        "Unicode case-expansion input must fail explicitly and use compatibility gray")
require_all(tests, [
    '"\\u{00A0}#336699\\u{00A0}"',
    '"#ＦＦ0000"',
    '"#А00000"',
    '"#FF\\u{0000}0000"',
    '"#FFFFFFFFFFFFFFFF"',
    'parseHexColor("#01020304")',
    "for value in 0...255",
    'for prefix in ["", "#", "0x", "0X", "#0x", "#0X"]',
], "tests must exercise Unicode, control, overflow, alpha-order, and byte-range boundaries")

duplicate_name_fixture = """== Devices ==
-- iOS 17.5 --
    iPhone 15 (11111111-1111-1111-1111-111111111111) (Shutdown)
-- iOS 18.5 --
    iPhone 15 (22222222-2222-2222-2222-222222222222) (Shutdown)
"""
selected_simulator = subprocess.run(
    ["awk", "-F", "[()]", "-f", str(ROOT / "scripts/select-ios-simulator-id.awk")],
    input=duplicate_name_fixture,
    text=True,
    capture_output=True,
    check=True,
).stdout.strip()
require(selected_simulator == "11111111-1111-1111-1111-111111111111",
        "simulator selector must return the first available iPhone UDID")
require_all(simulator_selector, ["iPhone", "length($2) == 36", "print $2", "exit"],
            "simulator selector must validate and return one iPhone UDID")

require_all(build_script, [
    "set -eu",
    "IOS_DESTINATION",
    "IOS_SIMULATOR_NAME",
    "scripts/select-ios-simulator-id.awk",
    "xcrun simctl list devices available",
    "No available iPhone simulator was found.",
    'DESTINATION="platform=iOS Simulator,id=${SIMULATOR_ID}"',
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
require_all(package_manifest, [
    "// swift-tools-version:5.9",
    'name: "HexToColor"',
    ".iOS(.v12)",
    ".macOS(.v10_13)",
    ".library(",
    'targets: ["HexToColor"]',
    ".target(",
    'path: "HexToColor"',
    'exclude: ["Info.plist"]',
    'sources: ["Hex.swift"]',
    ".testTarget(",
    'dependencies: ["HexToColor"]',
    'path: "HexToColorTests"',
    'sources: ["HexToColorTests.swift"]',
    "swiftLanguageVersions: [.v5]",
], "Package.swift must preserve the iOS 12/macOS 10.13 Swift 5 library and XCTest graph")
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
    "#0x", "rgb, rgba, rrggbb, and rrggbbaa", "non-hex", "signed",
    "parsehexcolor(_:)", "returns `nil`", "valid gray color",
    "fully transparent rgba",
    "ascii space, tab, carriage return, and line feed", "appkit", "swift package tests",
    "accessibility labels",
    "persist checkout credentials", "real xctest suite",
    "absolute makefile path", "any working directory",
], "README must document parser behavior and executable hosted verification")
require("UIKit and AppKit library" in readme and
        "Convenience Methods for UIColor" not in readme and
        "application or Objective-C/Swift sample" not in readme,
        "README overview must describe the maintained cross-platform library")
agents = read("AGENTS.md")
require("UIKit and AppKit `HexColor` library" in agents and
        "Convenience Methods for UIColor" not in agents and
        "application or Objective-C/Swift sample" not in agents,
        "AGENTS overview must describe the maintained cross-platform library")
require_all(vision.lower(), [
    "make lint", "make test", "make build", "make check", "swift 5", "ios 12",
    "invalid hex", "whitespace", "0x", "shorthand", "alpha", "unsupported lengths",
    "#0x", "0x-prefixed shorthand and rgba", "non-hex", "real xctest suite",
    "parsehexcolor(_:)", "explicit failure",
    "fully transparent rgba",
    "ascii space, tab, carriage return, and line feed", "appkit", "swift package tests",
], "VISION must describe the current parser and hosted validation baseline")
require("Add tests for additional case and malformed strings if supported" not in vision,
        "VISION must not list completed case and malformed-input coverage as future work")
require_all(vision, [
    "Mixed-case payloads across every accepted prefix and width are covered",
    "Malformed prefixes, partial parses, overflow, Unicode lookalikes, and controls",
    "are rejected and locked into the static baseline contract",
], "VISION must record completed case and malformed-input coverage")
require_all(changes, [
    "public", "toColor(hex:)", "scanHexInt", "make lint", "make test", "make build",
    "make check", "whitespace", "0x", "shorthand", "alpha", "non-hex",
    "unsupported lengths", "#0x", "prefixed shorthand and RGBA", "Swift 5", "iOS 12",
    "real XCTest", "credential persistence disabled",
    "parseHexColor(_:)", "valid gray color",
    "fully transparent RGBA",
    "Make verification target", "external directories",
    "AppKit", "Swift package tests", "Unicode whitespace",
], "CHANGES must record parser and current-Xcode verification work")
require_all(changes, [
    "Reconciled the parser roadmap with the existing mixed-case and malformed-input test matrix",
    PARSER_COVERAGE_PLAN,
], "CHANGES must record the completed parser-coverage roadmap item")
require_all(security, ["Security Policy", "privately", "malformed", "parseHexColor(_:)", "reported", "valid gray color"],
            "SECURITY must retain reporting and malformed-input guidance")
require_all(readme.lower(), [
    "swift package manager",
    "0.0.1` tag predates the manifest",
    "swift package tests",
], "README must document tested SwiftPM integration and the pre-manifest release boundary")
require_all(vision, [
    "Swift Package Manager exposes the existing source and XCTest layout",
    "Publish a future tag that includes the Swift package manifest",
], "VISION must record the SwiftPM distribution and release boundary")
require_all(changes, [
    "Swift Package Manager metadata",
    "hosted manifest parsing through `make test`",
], "CHANGES must record SwiftPM distribution and verification")

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
    UNICODE_NORMALIZATION_PLAN,
    LOCATION_INDEPENDENT_MAKE_PLAN,
    SWIFT_PACKAGE_PLAN,
    PARSER_COVERAGE_PLAN,
]
for plan_path in completed_plans:
    require("status: completed" in read(plan_path),
            f"completed plan marker missing: {plan_path}")
require_all(parser_coverage_plan, [
    "status: completed",
    "testAcceptedPrefixWidthAndCaseMatrix",
    "testRejectsPartialOverflowAndMalformedPrefixes",
    "No parser source change was required",
    "python3 scripts/check-baseline.py",
], "parser coverage plan must record the completed evidence and verification")
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
unicode_normalization_statuses = re.findall(r"^status: .+$", unicode_normalization_plan, flags=re.MULTILINE)
unicode_normalization_sections = unicode_normalization_plan.split("## Verification Completed\n", 1)
unicode_normalization_verification = unicode_normalization_sections[1] if len(unicode_normalization_sections) == 2 else ""
unicode_normalization_required_evidence = (
    "All four Make gates passed",
    "XCTest was skipped because `xcodebuild` is not installed locally",
    "sh -n build.sh",
    "ruby -c HexToColor.podspec",
    "pre-validation uppercasing mutation failed",
    "Unicode regression removal mutation failed",
    "ASCII character-set weakening mutation failed",
    "hosted macOS XCTest and CodeQL snapshot",
)
require(unicode_normalization_statuses == ["status: completed"] and
        all(item in unicode_normalization_verification for item in unicode_normalization_required_evidence) and
        re.search(r"\b(?:pending|todo|tbd|not run)\b", unicode_normalization_verification, re.IGNORECASE) is None,
        "Unicode normalization plan must record completed status and actual local verification")
swift_package_statuses = re.findall(r"^status: .+$", swift_package_plan, flags=re.MULTILINE)
swift_package_sections = swift_package_plan.split("## Verification Completed\n", 1)
swift_package_verification = swift_package_sections[1] if len(swift_package_sections) == 2 else ""
swift_package_required_evidence = (
    "All four Make gates passed",
    "external-directory `make -f",
    "Swift manifest parsing was skipped because `swift` is not installed locally",
    "XCTest was skipped because `xcodebuild` is not installed locally",
    "sh -n build.sh",
    "ruby -c HexToColor.podspec",
    "python3 -m py_compile scripts/check-baseline.py",
    "git diff --check",
    "Six isolated hostile mutations were rejected",
)
require(swift_package_statuses == ["status: completed"] and
        all(item in swift_package_verification for item in swift_package_required_evidence) and
        re.search(r"\b(?:pending|todo|tbd|not run)\b", swift_package_verification, re.IGNORECASE) is None,
        "Swift package plan must record completed status and actual local verification")
location_independent_make_statuses = re.findall(r"^status: .+$", location_independent_make_plan, flags=re.MULTILINE)
location_independent_make_sections = location_independent_make_plan.split("## Verification Completed\n", 1)
location_independent_make_verification = location_independent_make_sections[1] if len(location_independent_make_sections) == 2 else ""
location_independent_make_required_evidence = (
    "Root and external-directory Make gates passed",
    "root-derivation mutation failed",
    "checker-invocation mutation failed",
    "XCTest-script mutation failed",
    "plan-status mutation failed",
    "plan-evidence mutation failed",
    "documentation mutation failed",
)
require(location_independent_make_statuses == ["status: completed"] and
        all(item in location_independent_make_verification for item in location_independent_make_required_evidence) and
        re.search(r"\b(?:pending|todo|tbd|not run)\b", location_independent_make_verification, re.IGNORECASE) is None,
        "location-independent Make plan must record completed status and actual verification")
require_all(readme.lower(), ["utf-8 bytes", "unicode normalization", "homoglyph", "control"],
            "README must document the exact pre-normalization grammar")
require_all(security.lower(), ["ascii hex", "unicode normalization", "control characters"],
            "security guidance must document the exact parser boundary")
require("Parse only ASCII hex source bytes without Unicode case normalization" in vision and
        "Unicode whitespace" in changes and
        "before Unicode normalization" in read("AGENTS.md"),
        "project guidance must preserve the exact Unicode rejection boundary")

for ignore_entry in ["build/", "DerivedData/", "xcuserdata/", ".DS_Store"]:
    require(ignore_entry in gitignore, f"{ignore_entry} must stay ignored")

if shutil.which("xcodebuild"):
    subprocess.check_call(["xcodebuild", "-list", "-project", "HexToColor.xcodeproj"], cwd=str(ROOT))
else:
    print("check-baseline: xcodebuild not found; skipped Xcode project listing")

print("HexToColor baseline checks passed.")
