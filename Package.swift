// swift-tools-version:5.9

import PackageDescription

let package = Package(
    name: "HexToColor",
    platforms: [
        .iOS(.v12),
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
            sources: ["Hex.swift"]
        ),
        .testTarget(
            name: "HexToColorTests",
            dependencies: ["HexToColor"],
            path: "HexToColorTests",
            sources: ["HexToColorTests.swift"]
        ),
    ],
    swiftLanguageVersions: [.v5]
)
