/**
 * Hora family web haptics — the M3E pattern vocabulary (tick / click / success /
 * warning / error) shared with the native Android (`PreferenceHelper`) and iOS
 * (`Haptics.swift`) helpers, over the Vibration API (works on Android Chrome; a
 * no-op where unsupported, e.g. iOS Safari — purely an enhancement).
 *
 * The "haptics enabled" preference is **injected** (`isEnabled`) so this stays
 * free of any app-specific storage key — each app wires its own setting in a thin
 * local `lib/haptics.ts`:
 *
 *   import { createHaptics } from "./haptics-core";
 *   export const haptics = createHaptics(() => prefs.getHaptics());
 *
 * Canonical in hora-core/shared/web/lib/.
 */
export type Haptics = {
  tick: () => void;
  click: () => void;
  success: () => void;
  warning: () => void;
  error: () => void;
};

export function createHaptics(isEnabled: () => boolean): Haptics {
  function vibrate(pattern: number | number[]) {
    if (!isEnabled()) return;
    if (typeof navigator !== "undefined" && "vibrate" in navigator) {
      try {
        navigator.vibrate(pattern);
      } catch {
        /* ignore — vibration is best-effort */
      }
    }
  }
  return {
    tick: () => vibrate(5),
    click: () => vibrate(10),
    success: () => vibrate([8, 30, 8]),
    warning: () => vibrate(20),
    error: () => vibrate([20, 40, 20]),
  };
}
