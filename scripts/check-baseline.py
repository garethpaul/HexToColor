#!/usr/bin/env python3

from pathlib import Path
import plistlib
import shutil
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "docs/plans/2026-06-08-hextocolor-baseline.md"
SHORTHAND_PLAN = ROOT / "docs/plans/2026-06-09-hextocolor-rgb-shorthand.md"
ALPHA_PLAN = ROOT / "docs/plans/2026-06-09-hextocolor-rgba-alpha.md"
SIGNED_PLAN = ROOT / "docs/plans/2026-06-09-hextocolor-signed-character-guard.md"
HASH_ZERO_X_PLAN = ROOT / "docs/plans/2026-06-09-hextocolor-hash-zero-x-prefix.md"
MAKE_GATES_PLAN = ROOT / "docs/plans/2026-06-09-make-gate-aliases.md"
INVALID_LENGTH_PLAN = ROOT / "docs/plans/2026-06-09-hextocolor-invalid-length-coverage.md"
PREFIXED_ALPHA_PLAN = ROOT / "docs/plans/2026-06-09-hextocolor-prefixed-alpha-coverage.md"


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


def lint_plist(path):
    with (ROOT / path).open("rb") as plist_file:
        plistlib.load(plist_file)


required_files = [
    ".gitignore",
    "CHANGES.md",
    "LICENSE",
    "Makefile",
    "README.md",
    "SECURITY.md",
    "VISION.md",
    "build.sh",
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
]

for required_file in required_files:
    read(required_file)

subprocess.check_call(["sh", "-n", "build.sh"], cwd=str(ROOT))
require((ROOT / "build.sh").stat().st_mode & 0o111, "build.sh must be executable")
lint_plist("HexToColor/Info.plist")
lint_plist("HexToColorTests/Info.plist")

hex_source = read("HexToColor/Hex.swift")
tests = read("HexToColorTests/HexToColorTests.swift")
makefile = read("Makefile")
podspec = read("HexToColor.podspec")
readme = read("README.md")
vision = read("VISION.md")
changes = read("CHANGES.md")
gitignore = read(".gitignore")
plan = PLAN.read_text(errors="replace") if PLAN.exists() else ""
whitespace_plan = read("docs/plans/2026-06-08-hextocolor-whitespace-baseline.md")
zero_x_plan = read("docs/plans/2026-06-08-hextocolor-zero-x-prefix.md")
shorthand_plan = SHORTHAND_PLAN.read_text(errors="replace") if SHORTHAND_PLAN.exists() else ""
alpha_plan = ALPHA_PLAN.read_text(errors="replace") if ALPHA_PLAN.exists() else ""
signed_plan = SIGNED_PLAN.read_text(errors="replace") if SIGNED_PLAN.exists() else ""
hash_zero_x_plan = HASH_ZERO_X_PLAN.read_text(errors="replace") if HASH_ZERO_X_PLAN.exists() else ""
invalid_length_plan = INVALID_LENGTH_PLAN.read_text(errors="replace") if INVALID_LENGTH_PLAN.exists() else ""
prefixed_alpha_plan = PREFIXED_ALPHA_PLAN.read_text(errors="replace") if PREFIXED_ALPHA_PLAN.exists() else ""

require("public func toColor(hex: String) -> UIColor" in hex_source,
        "Hex parser must expose the documented public toColor API")
require("scanner.scanHexInt(&rgbValue)" in hex_source and "scanner.atEnd" in hex_source,
        "Hex parser must reject partially scanned invalid hex strings")
require("rangeOfCharacterFromSet" in hex_source and "invertedSet" in hex_source,
        "Hex parser must explicitly reject non-hex characters before scanning")
require('cString.hasPrefix("0X")' in hex_source and "advancedBy(2)" in hex_source,
        "Hex parser must strip 0x-prefixed RGB strings before length validation")
require("cString.characters.count == 3" in hex_source and "expandedString.append(character)" in hex_source,
        "Hex parser must expand three-character RGB shorthand")
require("cString.characters.count == 4" in hex_source and "cString.characters.count != 8" in hex_source,
        "Hex parser must accept RGBA shorthand and eight-character RGBA strings")
require("alphaValue = rgbValue & 0x000000FF" in hex_source and "alphaValue = 0xFF" in hex_source,
        "Hex parser must derive alpha for RGBA input and default RGB alpha to opaque")
require("return UIColor.grayColor()" in hex_source,
        "Hex parser must keep the documented gray fallback")
for test_name in [
    "testWhite",
    "testLowercaseWithoutHash",
    "testZeroXPrefix",
    "testHashZeroXPrefix",
    "testZeroXFourDigitShorthandWithAlpha",
    "testHashZeroXEightDigitRGBAWithAlpha",
    "testThreeDigitShorthand",
    "testFourDigitShorthandWithAlpha",
    "testEightDigitRGBAWithAlpha",
    "testTrimsWhitespaceAndNewlines",
    "testInvalidLengthReturnsGray",
    "testInvalidCharactersReturnGray",
    "testSignedHexReturnsGray",
]:
    require(test_name in tests, f"missing color parser test: {test_name}")
require("255.0, green: 255.0" not in tests,
        "tests must compare UIColor components in the 0...1 range")
require('toColor("#FFFF")' not in tests and 'toColor("#FF")' in tests and 'toColor("#FFFFF")' in tests and 'toColor("#FFFFFFFFF")' in tests,
        "invalid-length tests must use unsupported lengths now that four-character RGBA shorthand is valid")
require("IOS_DESTINATION" in read("build.sh") and "IOS_SIMULATOR_NAME" in read("build.sh"),
        "build.sh must support simulator destination overrides")
require("https://twitter.com/gpj" in podspec,
        "podspec social URL must use HTTPS")
require(".PHONY: build check lint test" in makefile and "lint test build: check" in makefile,
        "Makefile must expose lint, test, build, and check gate targets")
require("make lint" in readme and "make test" in readme and "make build" in readme and "make check" in readme and "invalid hex" in readme.lower() and "whitespace" in readme.lower() and "0x" in readme.lower() and "shorthand" in readme.lower() and "alpha" in readme.lower(),
        "README must document local checks, trimming, alpha, and invalid hex fallback")
require("unsupported lengths" in readme.lower(),
        "README must document unsupported length fallback")
require("#0x" in readme.lower(),
        "README must document hash-prefixed 0x normalization")
require("0xrgba" in readme.lower() and "#0xrrggbbaa" in readme.lower(),
        "README must document prefixed alpha normalization")
require("non-hex" in readme.lower() and "signed" in readme.lower(),
        "README must document explicit non-hex and signed-character fallback")
require("make lint" in vision and "make test" in vision and "make build" in vision and "make check" in vision and "invalid hex" in vision.lower() and "whitespace" in vision.lower() and "0x" in vision.lower() and "shorthand" in vision.lower() and "alpha" in vision.lower() and "non-hex" in vision.lower(),
        "VISION must describe the current baseline")
require("unsupported lengths" in vision.lower(),
        "VISION must describe unsupported length fallback")
require("#0x" in vision.lower(),
        "VISION must describe hash-prefixed 0x normalization")
require("0x-prefixed shorthand and rgba" in vision.lower(),
        "VISION must describe prefixed alpha normalization")
require("public" in changes and "toColor(hex:)" in changes and
        "scanHexInt" in changes and "make lint" in changes and "make test" in changes and "make build" in changes and "make check" in changes and "whitespace" in changes and "0x" in changes and "shorthand" in changes and "alpha" in changes and "non-hex" in changes,
        "CHANGES must record parser and check baseline work")
require("unsupported lengths" in changes.lower(),
        "CHANGES must record unsupported length coverage")
require("#0x" in changes.lower(),
        "CHANGES must record hash-prefixed 0x coverage")
require("prefixed shorthand and rgba" in changes.lower(),
        "CHANGES must record prefixed alpha coverage")
require("status: completed" in plan, "baseline plan must be marked completed")
require("status: completed" in whitespace_plan, "whitespace plan must be marked completed")
require("status: completed" in zero_x_plan, "0x prefix plan must be marked completed")
require("status: completed" in shorthand_plan, "shorthand plan must be marked completed")
require("status: completed" in alpha_plan, "alpha plan must be marked completed")
require("status: completed" in signed_plan, "signed-character plan must be marked completed")
require("status: completed" in hash_zero_x_plan, "hash 0x prefix plan must be marked completed")
require("status: completed" in invalid_length_plan, "invalid length coverage plan must be marked completed")
require("status: completed" in prefixed_alpha_plan, "prefixed alpha coverage plan must be marked completed")
make_gates_plan = MAKE_GATES_PLAN.read_text(errors="replace") if MAKE_GATES_PLAN.exists() else ""
require("status: completed" in make_gates_plan, "Make gate alias plan must be marked completed")
for ignore_entry in ["build/", "DerivedData/", "xcuserdata/", ".DS_Store"]:
    require(ignore_entry in gitignore, f"{ignore_entry} must stay ignored")

if shutil.which("xcodebuild"):
    subprocess.check_call(["xcodebuild", "-list", "-project", "HexToColor.xcodeproj"], cwd=str(ROOT))
else:
    print("check-baseline: xcodebuild not found; skipped Xcode project listing")

print("HexToColor baseline checks passed.")
