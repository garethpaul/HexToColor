#!/bin/sh

set -eu

SCRIPT_DIR=$(CDPATH= cd "$(dirname "$0")" && pwd)
PROJECT=${XCODE_PROJECT:-HexToColor.xcodeproj}
SCHEME=${XCODE_SCHEME:-HexToColorTests}
CONFIGURATION=${CONFIGURATION:-Debug}

if ! command -v xcodebuild >/dev/null 2>&1; then
    printf '%s\n' "xcodebuild is required to run HexToColor tests." >&2
    exit 127
fi

if [ -n "${IOS_DESTINATION:-}" ]; then
    DESTINATION=$IOS_DESTINATION
elif [ -n "${IOS_SIMULATOR_NAME:-}" ]; then
    DESTINATION="platform=iOS Simulator,name=${IOS_SIMULATOR_NAME}"
else
    SIMULATOR_ID=$(xcrun simctl list devices available | awk -F '[()]' -f "$SCRIPT_DIR/scripts/select-ios-simulator-id.awk")
    if [ -z "$SIMULATOR_ID" ]; then
        printf '%s\n' "No available iPhone simulator was found." >&2
        exit 1
    fi
    DESTINATION="platform=iOS Simulator,id=${SIMULATOR_ID}"
fi

xcodebuild \
    -project "$PROJECT" \
    -scheme "$SCHEME" \
    -destination "$DESTINATION" \
    -sdk iphonesimulator \
    -configuration "$CONFIGURATION" \
    build test
