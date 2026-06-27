.PHONY: build check lint test

override empty :=
override space := $(empty) $(empty)
override makefile_space := __HEXTOCOLOR_MAKEFILE_SPACE__
override encoded_makefile_list := $(patsubst $(makefile_space)%,%,$(subst $(space),$(makefile_space),$(MAKEFILE_LIST)))
override ROOT := $(subst $(makefile_space),$(space),$(abspath $(dir $(lastword $(encoded_makefile_list)))))

lint: check

test: check
	@if command -v swift >/dev/null 2>&1; then cd "$(ROOT)" && swift test; else printf '%s\n' "Skipping Swift package tests: swift is not installed."; fi
	@if command -v xcodebuild >/dev/null 2>&1; then cd "$(ROOT)" && ./build.sh; else printf '%s\n' "Skipping XCTest: xcodebuild is not installed."; fi

build: test

check:
	@python3 "$(ROOT)/scripts/check-baseline.py"
	@python3 "$(ROOT)/scripts/test-make-spaced-path.py"
