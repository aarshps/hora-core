# Shared iOS source (`shared/ios/swift/`)

Canonical Swift used **verbatim** (modulo one display-name token) by 2+ Hora apps. Each app
pulls these in with `bash ios/tools/sync_shared_ios.sh` (customised from
`templates/sync_shared_ios.sh`); the generated copies carry a "do not hand-edit" header and a
provenance manifest at `ios/tools/.hora-core-synced-ios`. Edit the canonical file here and
re-run the sync — never hand-edit the copy inside an app. This mirrors the Android shared layer
(`shared/android/`) and the web shared styles (`shared/web/res/css/`).

| File | Destination | Notes |
| --- | --- | --- |
| `Haptics.swift` | `Services/Haptics.swift` | M3E-aligned haptic helper, gated on `Preferences.shared.hapticsEnabled`. Verbatim. |
| `BiometricAuth.swift` | `Services/BiometricAuth.swift` | LocalAuthentication "App Lock" wrapper. `__HORA_APP_NAME__` → the app's display name in the default unlock reason. |
| `SelectionSheet.swift` | `Views/SelectionSheet.swift` | Glass bottom-sheet single-choice picker — the SwiftUI counterpart of Android's `SelectionBottomSheet`. Verbatim. |

## Adding a shared file
1. Put the canonical Swift under `shared/ios/swift/` with the generated-file header. Use
   `__HORA_APP_NAME__` for the app display name where one is unavoidable; otherwise keep it
   verbatim (no other app-specific identifiers).
2. Add it to the `FILES=( "name:dest" )` map in `templates/sync_shared_ios.sh` and in each
   app's `ios/tools/sync_shared_ios.sh`.
3. Re-run the sync in each app and let CI (`ios-build.yml`) validate the build.

## Bar for inclusion
Same as the rest of `shared/`: at least **two** family apps must use it, and it must be free of
app-specific logic (only the display-name token is allowed). Anything carrying app-specific
strings, colours, or business logic stays in the app.
