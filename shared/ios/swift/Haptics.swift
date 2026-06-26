//
// Shared Hora-family component — canonical source lives in hora-core/shared/ios/swift.
// It is GENERATED into each app by that app's ios/tools/sync_shared_ios.sh. Do NOT
// hand-edit the copy inside an app; edit it here in hora-core and re-run the sync.
//
import UIKit

/// Centralised haptic feedback — mirrors Android's M3E haptic philosophy
/// (click/tick/success/error). All calls are gated on `Preferences.hapticsEnabled`.
enum Haptics {

    static func tick() {
        guard Preferences.shared.hapticsEnabled else { return }
        UISelectionFeedbackGenerator().selectionChanged()
    }

    static func click() {
        guard Preferences.shared.hapticsEnabled else { return }
        UIImpactFeedbackGenerator(style: .light).impactOccurred()
    }

    static func success() {
        guard Preferences.shared.hapticsEnabled else { return }
        UINotificationFeedbackGenerator().notificationOccurred(.success)
    }

    static func warning() {
        guard Preferences.shared.hapticsEnabled else { return }
        UINotificationFeedbackGenerator().notificationOccurred(.warning)
    }

    static func error() {
        guard Preferences.shared.hapticsEnabled else { return }
        UINotificationFeedbackGenerator().notificationOccurred(.error)
    }

    static func heavyClick() {
        guard Preferences.shared.hapticsEnabled else { return }
        UIImpactFeedbackGenerator(style: .heavy).impactOccurred()
    }
}
