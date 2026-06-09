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
    
    if (cString.characters.count != 6) {
        return UIColor.grayColor()
    }
    
    var rgbValue:UInt32 = 0
    let scanner = NSScanner(string: cString)
    if (!scanner.scanHexInt(&rgbValue) || !scanner.atEnd) {
        return UIColor.grayColor()
    }
    
    return UIColor(
        red: CGFloat((rgbValue & 0xFF0000) >> 16) / 255.0,
        green: CGFloat((rgbValue & 0x00FF00) >> 8) / 255.0,
        blue: CGFloat(rgbValue & 0x0000FF) / 255.0,
        alpha: CGFloat(1.0)
    )
}
