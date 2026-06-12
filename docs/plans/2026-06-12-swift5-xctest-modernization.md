# Swift 5 XCTest Modernization

status: completed

## Context

HexToColor's parser behavior was well characterized in XCTest source, but the
project still used Swift 2-era APIs and hosted CI only listed the project. The
tests therefore did not compile or execute on the current macOS runner.

## Completed Scope

- Migrated the parser implementation and XCTest assertions to Swift 5 syntax.
- Preserved the unlabeled `toColor(_:)` call shape and added a deprecated
  labeled `toColor(hex:)` compatibility wrapper.
- Set Swift 5 explicitly on the framework and test targets.
- Raised the checked-in Xcode project deployment floor to iOS 12, the minimum
  supported by the hosted current-Xcode runner.
- Aligned the CocoaPods Swift and deployment compatibility declarations while
  leaving release versioning and the source tag unchanged.
- Made `build.sh` discover an available iPhone simulator unless callers provide
  `IOS_DESTINATION` or `IOS_SIMULATOR_NAME`.
- Run the actual XCTest suite through `make test` in hosted macOS CI.
- Disabled persisted checkout credentials while retaining immutable checkout,
  read-only permissions, cancellation, and the bounded runner.
- Retired the obsolete Xcode 7 Travis configuration so hosted validation has a
  single current-Xcode source of truth.

## Verification

- `make check`
- `sh -n build.sh`
- hosted `./build.sh` on `macos-15`
- mutations removing the Swift language settings, XCTest step, compatibility
  wrapper, or simulator discovery must fail
- `git diff --check`

The CocoaPods release version and source tag remain at 0.0.1 and are not
republished by this change. A future release should validate the podspec against
the final tagged Swift 5 source.
