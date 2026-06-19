//
//  Hex.swift
//  HexToColor
//
//  Created by Gareth Jones on 1/7/16.
//  Copyright © 2016 GPJ. All rights reserved.
//

#if canImport(UIKit)
import UIKit
public typealias HexColor = UIColor
#elseif canImport(AppKit)
import AppKit
public typealias HexColor = NSColor
#else
#error("HexToColor requires UIKit or AppKit")
#endif

private let trimmedASCIIWhitespace: Set<UInt8> = [0x09, 0x0A, 0x0D, 0x20]

private func hexNibble(_ byte: UInt8) -> UInt8? {
    switch byte {
    case 0x30...0x39:
        return byte - 0x30
    case 0x41...0x46:
        return byte - 0x41 + 10
    case 0x61...0x66:
        return byte - 0x61 + 10
    default:
        return nil
    }
}

private func makeColor(red: UInt8, green: UInt8, blue: UInt8, alpha: UInt8) -> HexColor {
    let redComponent = CGFloat(red) / 255.0
    let greenComponent = CGFloat(green) / 255.0
    let blueComponent = CGFloat(blue) / 255.0
    let alphaComponent = CGFloat(alpha) / 255.0

#if canImport(UIKit)
    return HexColor(
        red: redComponent,
        green: greenComponent,
        blue: blueComponent,
        alpha: alphaComponent
    )
#else
    return HexColor(
        srgbRed: redComponent,
        green: greenComponent,
        blue: blueComponent,
        alpha: alphaComponent
    )
#endif
}

// Parses a hex string into a UIColor.
//
public func parseHexColor(_ hex: String) -> HexColor? {
    var bytes = hex.utf8[...]

    while let first = bytes.first, trimmedASCIIWhitespace.contains(first) {
        bytes.removeFirst()
    }
    while let last = bytes.last, trimmedASCIIWhitespace.contains(last) {
        bytes.removeLast()
    }

    if bytes.first == 0x23 {
        bytes.removeFirst()
    }
    if bytes.count >= 2 {
        let prefixEnd = bytes.index(after: bytes.startIndex)
        if bytes[bytes.startIndex] == 0x30 &&
            (bytes[prefixEnd] == 0x78 || bytes[prefixEnd] == 0x58) {
            bytes.removeFirst(2)
        }
    }

    let digitCount = bytes.count
    guard digitCount == 3 || digitCount == 4 || digitCount == 6 || digitCount == 8 else {
        return nil
    }

    var digits: [UInt8] = []
    digits.reserveCapacity(digitCount)
    for byte in bytes {
        guard let digit = hexNibble(byte) else {
            return nil
        }
        digits.append(digit)
    }

    let isShorthand = digitCount <= 4
    func component(at index: Int) -> UInt8 {
        if isShorthand {
            return digits[index] * 0x11
        }
        return digits[index * 2] << 4 | digits[index * 2 + 1]
    }

    return makeColor(
        red: component(at: 0),
        green: component(at: 1),
        blue: component(at: 2),
        alpha: digitCount == 4 || digitCount == 8 ? component(at: 3) : 0xFF
    )
}

// Converts a hex string into a UIColor, falling back to gray for compatibility.
//
public func toColor(_ hex: String) -> HexColor {
    return parseHexColor(hex) ?? .gray
}

@available(*, deprecated, renamed: "toColor(_:)")
public func toColor(hex: String) -> HexColor {
    return toColor(hex)
}
