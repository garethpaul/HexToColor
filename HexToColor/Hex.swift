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
public func toColor(hex: String) -> UIColor {
    var cString:String = hex.stringByTrimmingCharactersInSet(NSCharacterSet.whitespaceAndNewlineCharacterSet() as NSCharacterSet).uppercaseString
    
    if (cString.hasPrefix("#")) {
        cString = cString.substringFromIndex(cString.startIndex.advancedBy(1))
    }

    if (cString.hasPrefix("0X")) {
        cString = cString.substringFromIndex(cString.startIndex.advancedBy(2))
    }

    if (cString.characters.count == 3 || cString.characters.count == 4) {
        var expandedString = ""
        for character in cString.characters {
            expandedString.append(character)
            expandedString.append(character)
        }
        cString = expandedString
    }
    
    if (cString.characters.count != 6 && cString.characters.count != 8) {
        return UIColor.grayColor()
    }
    
    var rgbValue:UInt32 = 0
    let scanner = NSScanner(string: cString)
    if (!scanner.scanHexInt(&rgbValue) || !scanner.atEnd) {
        return UIColor.grayColor()
    }

    let redValue: UInt32
    let greenValue: UInt32
    let blueValue: UInt32
    let alphaValue: UInt32
    if (cString.characters.count == 8) {
        redValue = (rgbValue & 0xFF000000) >> 24
        greenValue = (rgbValue & 0x00FF0000) >> 16
        blueValue = (rgbValue & 0x0000FF00) >> 8
        alphaValue = rgbValue & 0x000000FF
    } else {
        redValue = (rgbValue & 0xFF0000) >> 16
        greenValue = (rgbValue & 0x00FF00) >> 8
        blueValue = rgbValue & 0x0000FF
        alphaValue = 0xFF
    }
    
    return UIColor(
        red: CGFloat(redValue) / 255.0,
        green: CGFloat(greenValue) / 255.0,
        blue: CGFloat(blueValue) / 255.0,
        alpha: CGFloat(alphaValue) / 255.0
    )
}
