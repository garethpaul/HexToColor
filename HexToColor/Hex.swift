//
//  Hex.swift
//  HexToColor
//
//  Created by Gareth Jones on 1/7/16.
//  Copyright © 2016 GPJ. All rights reserved.
//

import UIKit

// Converts a hex string into a UIColor.
//
public func toColor(_ hex: String) -> UIColor {
    var colorString = hex.trimmingCharacters(in: .whitespacesAndNewlines).uppercased()

    if colorString.hasPrefix("#") {
        colorString.removeFirst()
    }

    if colorString.hasPrefix("0X") {
        colorString.removeFirst(2)
    }

    if colorString.count == 3 || colorString.count == 4 {
        colorString = colorString.map { "\($0)\($0)" }.joined()
    }

    guard colorString.count == 6 || colorString.count == 8 else {
        return .gray
    }

    let allowedHexCharacters = CharacterSet(charactersIn: "0123456789ABCDEF")
    guard colorString.rangeOfCharacter(from: allowedHexCharacters.inverted) == nil else {
        return .gray
    }

    var colorValue: UInt64 = 0
    let scanner = Scanner(string: colorString)
    guard scanner.scanHexInt64(&colorValue), scanner.isAtEnd else {
        return .gray
    }

    let redValue: UInt64
    let greenValue: UInt64
    let blueValue: UInt64
    let alphaValue: UInt64
    if colorString.count == 8 {
        redValue = (colorValue & 0xFF000000) >> 24
        greenValue = (colorValue & 0x00FF0000) >> 16
        blueValue = (colorValue & 0x0000FF00) >> 8
        alphaValue = colorValue & 0x000000FF
    } else {
        redValue = (colorValue & 0xFF0000) >> 16
        greenValue = (colorValue & 0x00FF00) >> 8
        blueValue = colorValue & 0x0000FF
        alphaValue = 0xFF
    }

    return UIColor(
        red: CGFloat(redValue) / 255.0,
        green: CGFloat(greenValue) / 255.0,
        blue: CGFloat(blueValue) / 255.0,
        alpha: CGFloat(alphaValue) / 255.0
    )
}

@available(*, deprecated, renamed: "toColor(_:)")
public func toColor(hex: String) -> UIColor {
    return toColor(hex)
}
