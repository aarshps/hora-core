---
name: android-platform-standards
description: Modern Android platform baseline for Hora-family apps — target the latest stable Android, mandatory edge-to-edge + window insets, Credential Manager auth, and native-API-over-compat-shim architecture.
---

# Modern Android platform standards

Hora apps track the latest stable Android and use its native capabilities directly rather
than carrying legacy compatibility layers. The rule is "target the newest platform +
edge-to-edge + proper insets" — **not** a specific version number. (The family currently
sits around SDK 35–36; keep `minSdk` high enough to use native APIs without compat shims.)

## 1. Edge-to-edge is mandatory
- Enable it natively: `enableEdgeToEdge()` / `WindowCompat.setDecorFitsSystemWindows(window,
  false)` in the base activity. Don't rely on legacy `fitsSystemWindows`.
- **Every bottom sheet handles its own insets** so content isn't hidden behind the
  navigation bar.
- Apply window insets explicitly (top → app bar; bottom → scroll padding + FAB offset).

## 2. Modern security & auth
- Use **Credential Manager** (`androidx.credentials`) for sign-in (e.g. Google) — the
  legacy `GoogleSignInClient` is banned.
- Use `androidx.biometric` `BiometricPrompt` with `BIOMETRIC_STRONG` where biometrics apply.

## 3. Clean architecture (no legacy debt)
- Prefer native platform APIs over AndroidX compat wrappers where the native API already
  exists at your `minSdk` and the wrapper only adds bulk for older OSes you don't support.
- Keep core/lifecycle dependencies current.

## 4. UX expectations
- Support the **predictive back** gesture natively (manifest opt-in + per-screen previews).
- Use newer `HapticFeedbackConstants` freely (e.g. `CONFIRM`, `REJECT`) — see
  `m3e-haptic-standards`.
- **No launcher long-press shortcuts.** Hora apps ship **no** static (`res/xml/shortcuts.xml` + the
  manifest `android.app.shortcuts` meta-data) **or** dynamic (`ShortcutManager`) app shortcuts — the
  long-press app-icon menu stays empty. They were tried (e.g. add-habit / stats) and dropped as
  low-value clutter; every primary action already has an obvious in-app entry point. Remove the xml,
  the manifest meta-data, any `ACTION_*` intent handling, and the orphaned icons/strings together.

## Checklist
- [ ] Edge-to-edge enabled natively; bottom sheets + lists handle insets.
- [ ] Auth via Credential Manager; no legacy sign-in client.
- [ ] Native APIs preferred over compat shims where `minSdk` allows.
- [ ] Predictive back supported.
- [ ] No launcher long-press shortcuts (static or dynamic).
