//
// Shared Hora-family component — canonical source lives in hora-core/shared/ios/swift.
// It is GENERATED into each app by that app's ios/tools/sync_shared_ios.sh. Do NOT
// hand-edit the copy inside an app; edit it here in hora-core and re-run the sync.
// (The app's display name is filled into the default unlock reason on sync.)
//
import Foundation
import LocalAuthentication

/// Wraps LocalAuthentication for the "App Lock" toggle. Mirrors Android's
/// `BiometricAuthManager`.
enum BiometricAuth {

    static var isAvailable: Bool {
        let context = LAContext()
        var error: NSError?
        return context.canEvaluatePolicy(.deviceOwnerAuthentication, error: &error)
    }

    static var biometryType: LABiometryType {
        let context = LAContext()
        _ = context.canEvaluatePolicy(.deviceOwnerAuthentication, error: nil)
        return context.biometryType
    }

    static var displayName: String {
        switch biometryType {
        case .faceID: return "Face ID"
        case .touchID: return "Touch ID"
        case .opticID: return "Optic ID"
        default: return "Device Passcode"
        }
    }

    /// Returns true on success, false on user cancel / fallback failure.
    static func authenticate(reason: String = "Unlock __HORA_APP_NAME__") async -> Bool {
        let context = LAContext()
        context.localizedFallbackTitle = "Use Passcode"
        do {
            return try await context.evaluatePolicy(.deviceOwnerAuthentication, localizedReason: reason)
        } catch {
            return false
        }
    }
}
