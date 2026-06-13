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
    func assertColor(_ color: UIColor, red: CGFloat, green: CGFloat, blue: CGFloat, alpha: CGFloat) {
        var actualRed: CGFloat = 0
        var actualGreen: CGFloat = 0
        var actualBlue: CGFloat = 0
        var actualAlpha: CGFloat = 0

        XCTAssertTrue(color.getRed(&actualRed, green: &actualGreen, blue: &actualBlue, alpha: &actualAlpha))
        XCTAssertEqual(red, actualRed, accuracy: 0.001)
        XCTAssertEqual(green, actualGreen, accuracy: 0.001)
        XCTAssertEqual(blue, actualBlue, accuracy: 0.001)
        XCTAssertEqual(alpha, actualAlpha, accuracy: 0.001)
    }
    
    func testWhite() {
        let color = toColor("#FFFFFF")
        assertColor(color, red: 1.0, green: 1.0, blue: 1.0, alpha: 1.0)
    }

    func testLowercaseWithoutHash() {
        let color = toColor("00ff7f")
        assertColor(color, red: 0.0, green: 1.0, blue: 127.0 / 255.0, alpha: 1.0)
    }

    func testZeroXPrefix() {
        let color = toColor("0x112233")
        assertColor(color, red: 17.0 / 255.0, green: 34.0 / 255.0, blue: 51.0 / 255.0, alpha: 1.0)
    }

    func testHashZeroXPrefix() {
        let color = toColor("#0x112233")
        assertColor(color, red: 17.0 / 255.0, green: 34.0 / 255.0, blue: 51.0 / 255.0, alpha: 1.0)
    }

    func testZeroXFourDigitShorthandWithAlpha() {
        let color = toColor("0xF0A8")
        assertColor(color, red: 1.0, green: 0.0, blue: 170.0 / 255.0, alpha: 136.0 / 255.0)
    }

    func testZeroXEightDigitRGBAWithAlpha() {
        let color = toColor("0x33669980")
        assertColor(color, red: 51.0 / 255.0, green: 102.0 / 255.0, blue: 153.0 / 255.0, alpha: 128.0 / 255.0)
    }

    func testHashZeroXFourDigitShorthandWithAlpha() {
        let color = toColor("#0xF0A8")
        assertColor(color, red: 1.0, green: 0.0, blue: 170.0 / 255.0, alpha: 136.0 / 255.0)
    }

    func testHashZeroXEightDigitRGBAWithAlpha() {
        let color = toColor("#0x33669980")
        assertColor(color, red: 51.0 / 255.0, green: 102.0 / 255.0, blue: 153.0 / 255.0, alpha: 128.0 / 255.0)
    }

    func testThreeDigitShorthand() {
        let color = toColor("#F0A")
        assertColor(color, red: 1.0, green: 0.0, blue: 170.0 / 255.0, alpha: 1.0)
    }

    func testFourDigitShorthandWithAlpha() {
        let color = toColor("#F0A8")
        assertColor(color, red: 1.0, green: 0.0, blue: 170.0 / 255.0, alpha: 136.0 / 255.0)
    }

    func testEightDigitRGBAWithAlpha() {
        let color = toColor("#33669980")
        assertColor(color, red: 51.0 / 255.0, green: 102.0 / 255.0, blue: 153.0 / 255.0, alpha: 128.0 / 255.0)
    }

    func testDeprecatedLabeledAPICompatibility() {
        let color = toColor(hex: "#33669980")
        assertColor(color, red: 51.0 / 255.0, green: 102.0 / 255.0, blue: 153.0 / 255.0, alpha: 128.0 / 255.0)
    }

    func testFailableParserDistinguishesValidGrayFromInvalidInput() {
        guard let gray = parseHexColor("#808080") else {
            XCTFail("Valid gray should parse successfully")
            return
        }

        assertColor(gray, red: 128.0 / 255.0, green: 128.0 / 255.0, blue: 128.0 / 255.0, alpha: 1.0)
        XCTAssertNil(parseHexColor("#FF"))
        XCTAssertNil(parseHexColor("#FFFFFG"))
        XCTAssertNil(parseHexColor("-FFFFF"))
    }

    func testTrimsWhitespaceAndNewlines() {
        let color = toColor(" \n#336699\t")
        assertColor(color, red: 51.0 / 255.0, green: 102.0 / 255.0, blue: 153.0 / 255.0, alpha: 1.0)
    }

    func testInvalidLengthReturnsGray() {
        assertColor(toColor("#FF"), red: 0.5, green: 0.5, blue: 0.5, alpha: 1.0)
        assertColor(toColor("#FFFFF"), red: 0.5, green: 0.5, blue: 0.5, alpha: 1.0)
        assertColor(toColor("#FFFFFFFFF"), red: 0.5, green: 0.5, blue: 0.5, alpha: 1.0)
    }

    func testInvalidCharactersReturnGray() {
        assertColor(toColor("#FFFFFG"), red: 0.5, green: 0.5, blue: 0.5, alpha: 1.0)
    }

    func testSignedHexReturnsGray() {
        assertColor(toColor("+FFFFF"), red: 0.5, green: 0.5, blue: 0.5, alpha: 1.0)
        assertColor(toColor("-FFFFF"), red: 0.5, green: 0.5, blue: 0.5, alpha: 1.0)
    }
}
