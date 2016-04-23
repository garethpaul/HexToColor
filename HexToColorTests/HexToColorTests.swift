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
    
    override func setUp() {
        super.setUp()
        // Put setup code here. This method is called before the invocation of each test method in the class.
    }
    
    override func tearDown() {
        // Put teardown code here. This method is called after the invocation of each test method in the class.
        super.tearDown()
    }
    
    func testWhite() {
        // This is an example of a functional test case.
        // Use XCTAssert and related functions to verify your tests produce the correct results.
        let color = toColor("#FFFFFF")
        let white = UIColor(red: 255.0, green: 255.0, blue: 255.0, alpha: 1.0)
        XCTAssert(color == white)
    }
    
    func testPerformanceExample() {
        // This is an example of a performance test case.
        self.measureBlock {
            // Put the code you want to measure the time of here.
        }
    }
    
}
