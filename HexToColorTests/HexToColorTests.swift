//
//  HexToColorTests.swift
//  HexToColorTests
//
//  Created by Gareth on 7/1/16.
//  Copyright © 2016 GPJ. All rights reserved.
//

import XCTest

#if canImport(AppKit)
import AppKit
#endif

@testable import HexToColor

class HexToColorTests: XCTestCase {
    func assertColor(_ color: HexColor, red: CGFloat, green: CGFloat, blue: CGFloat, alpha: CGFloat) {
        var actualRed: CGFloat = 0
        var actualGreen: CGFloat = 0
        var actualBlue: CGFloat = 0
        var actualAlpha: CGFloat = 0

#if canImport(UIKit)
        XCTAssertTrue(color.getRed(&actualRed, green: &actualGreen, blue: &actualBlue, alpha: &actualAlpha))
#else
        guard let color = color.usingColorSpace(.sRGB) else {
            return XCTFail("Expected an sRGB-compatible color")
        }
        color.getRed(&actualRed, green: &actualGreen, blue: &actualBlue, alpha: &actualAlpha)
#endif
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

    func testUnicodeCaseExpansionDoesNotCreateValidHex() {
        XCTAssertNil(parseHexColor("#ﬀ0000"))
        assertColor(toColor("#ﬀ0000"), red: 0.5, green: 0.5, blue: 0.5, alpha: 1.0)
    }

    func testTransparentRGBAIsValidAtBothWidths() {
        for input in ["#0000", "#00000000"] {
            let parsed = parseHexColor(input)
            XCTAssertNotNil(parsed)
            guard let color = parsed else {
                continue
            }

            assertColor(color, red: 0.0, green: 0.0, blue: 0.0, alpha: 0.0)
            assertColor(toColor(input), red: 0.0, green: 0.0, blue: 0.0, alpha: 0.0)
        }
    }

    func testTrimsWhitespaceAndNewlines() {
        let color = toColor(" \n#336699\t")
        assertColor(color, red: 51.0 / 255.0, green: 102.0 / 255.0, blue: 153.0 / 255.0, alpha: 1.0)
    }

    func testOnlyDocumentedASCIIWhitespaceIsTrimmed() {
        XCTAssertNotNil(parseHexColor(" \t\r\n#336699\n\r\t "))

        for input in [
            "\u{00A0}#336699\u{00A0}",
            "\u{000B}#336699\u{000B}",
            "\u{000C}#336699\u{000C}",
            "\u{2028}#336699\u{2028}",
        ] {
            let scalars = input.unicodeScalars
                .map { String(format: "U+%04X", $0.value) }
                .joined(separator: " ")
            XCTAssertNil(parseHexColor(input), "Unexpectedly accepted \(scalars)")
        }
    }

    func testRejectsUnicodeLookalikesAndControlsBeforeParsing() {
        for input in [
            "#ＦＦ0000",
            "#А00000",
            "#ﬀ0000",
            "#FF\u{200B}0000",
            "#FF\u{0000}0000",
            "#FF 0000",
        ] {
            XCTAssertNil(parseHexColor(input))
        }
    }

    func testRejectsPartialOverflowAndMalformedPrefixes() {
        for input in [
            "#123456tail",
            "#123456789",
            "#FFFFFFFFFFFFFFFF",
            "#0x",
            "0x#123456",
            "##123456",
            "#0x0x123456",
        ] {
            XCTAssertNil(parseHexColor(input))
        }
    }

    func testRGBAUsesTrailingAlphaByte() {
        guard let color = parseHexColor("#01020304") else {
            return XCTFail("Expected valid RGBA color")
        }

        assertColor(color, red: 1.0 / 255.0, green: 2.0 / 255.0, blue: 3.0 / 255.0, alpha: 4.0 / 255.0)
    }

    func testAllByteValuesRoundTripThroughRGBAParser() {
        for value in 0...255 {
            let red = value
            let green = 255 - value
            let blue = value ^ 0xA5
            let alpha = (value &* 73) & 0xFF
            let input = String(format: "#%02X%02X%02X%02X", red, green, blue, alpha)

            guard let color = parseHexColor(input) else {
                XCTFail("Expected \(input) to parse")
                continue
            }

            assertColor(
                color,
                red: CGFloat(red) / 255.0,
                green: CGFloat(green) / 255.0,
                blue: CGFloat(blue) / 255.0,
                alpha: CGFloat(alpha) / 255.0
            )
        }
    }

    func testAcceptedPrefixWidthAndCaseMatrix() {
        let cases: [(payload: String, red: CGFloat, green: CGFloat, blue: CGFloat, alpha: CGFloat)] = [
            ("F0a", 1.0, 0.0, 170.0 / 255.0, 1.0),
            ("F0a8", 1.0, 0.0, 170.0 / 255.0, 136.0 / 255.0),
            ("336a9F", 51.0 / 255.0, 106.0 / 255.0, 159.0 / 255.0, 1.0),
            ("336a9F80", 51.0 / 255.0, 106.0 / 255.0, 159.0 / 255.0, 128.0 / 255.0),
        ]

        for prefix in ["", "#", "0x", "0X", "#0x", "#0X"] {
            for testCase in cases {
                let input = prefix + testCase.payload
                guard let color = parseHexColor(input) else {
                    XCTFail("Expected \(input) to parse")
                    continue
                }
                assertColor(
                    color,
                    red: testCase.red,
                    green: testCase.green,
                    blue: testCase.blue,
                    alpha: testCase.alpha
                )
            }
        }
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
