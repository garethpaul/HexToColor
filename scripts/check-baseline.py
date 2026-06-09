#!/usr/bin/env python3

from pathlib import Path
import plistlib
import shutil
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "docs/plans/2026-06-08-hextocolor-baseline.md"


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
]

for required_file in required_files:
    read(required_file)

subprocess.check_call(["sh", "-n", "build.sh"], cwd=str(ROOT))
require((ROOT / "build.sh").stat().st_mode & 0o111, "build.sh must be executable")
lint_plist("HexToColor/Info.plist")
lint_plist("HexToColorTests/Info.plist")

hex_source = read("HexToColor/Hex.swift")
tests = read("HexToColorTests/HexToColorTests.swift")
podspec = read("HexToColor.podspec")
readme = read("README.md")
vision = read("VISION.md")
changes = read("CHANGES.md")
gitignore = read(".gitignore")
plan = PLAN.read_text(errors="replace") if PLAN.exists() else ""
whitespace_plan = read("docs/plans/2026-06-08-hextocolor-whitespace-baseline.md")
zero_x_plan = read("docs/plans/2026-06-08-hextocolor-zero-x-prefix.md")

require("public func toColor(hex: String) -> UIColor" in hex_source,
        "Hex parser must expose the documented public toColor API")
require("scanner.scanHexInt(&rgbValue)" in hex_source and "scanner.atEnd" in hex_source,
        "Hex parser must reject partially scanned invalid hex strings")
require('cString.hasPrefix("0X")' in hex_source and "advancedBy(2)" in hex_source,
        "Hex parser must strip 0x-prefixed RGB strings before length validation")
require("return UIColor.grayColor()" in hex_source,
        "Hex parser must keep the documented gray fallback")
for test_name in [
    "testWhite",
    "testLowercaseWithoutHash",
    "testZeroXPrefix",
    "testTrimsWhitespaceAndNewlines",
    "testInvalidLengthReturnsGray",
    "testInvalidCharactersReturnGray",
]:
    require(test_name in tests, f"missing color parser test: {test_name}")
require("255.0, green: 255.0" not in tests,
        "tests must compare UIColor components in the 0...1 range")
require("IOS_DESTINATION" in read("build.sh") and "IOS_SIMULATOR_NAME" in read("build.sh"),
        "build.sh must support simulator destination overrides")
require("https://twitter.com/gpj" in podspec,
        "podspec social URL must use HTTPS")
require("make check" in readme and "invalid hex" in readme.lower() and "whitespace" in readme.lower() and "0x" in readme.lower(),
        "README must document local checks, trimming, and invalid hex fallback")
require("make check" in vision and "invalid hex" in vision.lower() and "whitespace" in vision.lower() and "0x" in vision.lower(),
        "VISION must describe the current baseline")
require("public" in changes and "toColor(hex:)" in changes and
        "scanHexInt" in changes and "make check" in changes and "whitespace" in changes and "0x" in changes,
        "CHANGES must record parser and check baseline work")
require("status: completed" in plan, "baseline plan must be marked completed")
require("status: completed" in whitespace_plan, "whitespace plan must be marked completed")
require("status: completed" in zero_x_plan, "0x prefix plan must be marked completed")
for ignore_entry in ["build/", "DerivedData/", "xcuserdata/", ".DS_Store"]:
    require(ignore_entry in gitignore, f"{ignore_entry} must stay ignored")

if shutil.which("xcodebuild"):
    subprocess.check_call(["xcodebuild", "-list", "-project", "HexToColor.xcodeproj"], cwd=str(ROOT))
else:
    print("check-baseline: xcodebuild not found; skipped Xcode project listing")

print("HexToColor baseline checks passed.")
