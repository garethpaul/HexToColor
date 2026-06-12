.PHONY: build check lint test

lint: check

test: check
	@if command -v xcodebuild >/dev/null 2>&1; then ./build.sh; else printf '%s\n' "Skipping XCTest: xcodebuild is not installed."; fi

build: test

check:
	python3 scripts/check-baseline.py
