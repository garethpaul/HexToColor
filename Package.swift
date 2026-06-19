// swift-tools-version:5.9

import PackageDescription

let package = Package(
    name: "HexToColor",
    platforms: [
        .iOS(.v12),
        .macOS(.v10_13),
    ],
    products: [
        .library(
            name: "HexToColor",
            targets: ["HexToColor"]
        ),
    ],
    targets: [
        .target(
            name: "HexToColor",
            path: "HexToColor",
            exclude: ["Info.plist"],
            sources: ["Hex.swift"]
        ),
        .testTarget(
            name: "HexToColorTests",
            dependencies: ["HexToColor"],
            path: "HexToColorTests",
            exclude: ["Info.plist"],
            sources: ["HexToColorTests.swift"]
        ),
    ],
    swiftLanguageVersions: [.v5]
)
