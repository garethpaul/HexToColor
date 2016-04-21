#!/bin/sh

set -eu

function ci_lib() {
    NAME=$1
    xcodebuild -project HexToColor.xcodeproj \
               -scheme "HexToColorTests" \
               -destination "platform=iOS Simulator,name=${NAME}" \
               -sdk iphonesimulator \
               -configuration "Debug" \
               build test
}
ci_lib "iPhone 5"
