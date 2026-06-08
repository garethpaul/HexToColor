//
//  HexToColorTests.swift
//  HexToColorTests
//
//  Created by Gareth on 7/1/16.
//  Copyright © 2016 GPJ. All rights reserved.
//

import XCTest

@testable import HexToColor

class HexToColorTests: XCTestCase {
    func assertColor(color: UIColor, red: CGFloat, green: CGFloat, blue: CGFloat, alpha: CGFloat) {
        var actualRed: CGFloat = 0
        var actualGreen: CGFloat = 0
        var actualBlue: CGFloat = 0
        var actualAlpha: CGFloat = 0

        XCTAssertTrue(color.getRed(&actualRed, green: &actualGreen, blue: &actualBlue, alpha: &actualAlpha))
        XCTAssertEqualWithAccuracy(red, actualRed, accuracy: 0.001)
        XCTAssertEqualWithAccuracy(green, actualGreen, accuracy: 0.001)
        XCTAssertEqualWithAccuracy(blue, actualBlue, accuracy: 0.001)
        XCTAssertEqualWithAccuracy(alpha, actualAlpha, accuracy: 0.001)
    }
    
    func testWhite() {
        let color = toColor("#FFFFFF")
        assertColor(color, red: 1.0, green: 1.0, blue: 1.0, alpha: 1.0)
    }

    func testLowercaseWithoutHash() {
        let color = toColor("00ff7f")
        assertColor(color, red: 0.0, green: 1.0, blue: 127.0 / 255.0, alpha: 1.0)
    }

    func testInvalidLengthReturnsGray() {
        assertColor(toColor("#FFF"), red: 0.5, green: 0.5, blue: 0.5, alpha: 1.0)
    }

    func testInvalidCharactersReturnGray() {
        assertColor(toColor("#FFFFFG"), red: 0.5, green: 0.5, blue: 0.5, alpha: 1.0)
    }
}
