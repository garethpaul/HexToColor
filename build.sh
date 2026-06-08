#!/bin/sh

set -eu

PROJECT=${XCODE_PROJECT:-HexToColor.xcodeproj}
SCHEME=${XCODE_SCHEME:-HexToColorTests}
SIMULATOR_NAME=${IOS_SIMULATOR_NAME:-iPhone 5}
DESTINATION=${IOS_DESTINATION:-platform=iOS Simulator,name=${SIMULATOR_NAME}}
CONFIGURATION=${CONFIGURATION:-Debug}

if ! command -v xcodebuild >/dev/null 2>&1; then
    printf '%s\n' "xcodebuild is required to run HexToColor tests." >&2
    exit 127
fi

xcodebuild \
    -project "$PROJECT" \
    -scheme "$SCHEME" \
    -destination "$DESTINATION" \
    -sdk iphonesimulator \
    -configuration "$CONFIGURATION" \
    build test
