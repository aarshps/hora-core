# Shared Web source (`shared/web/`)

Canonical Web building blocks every Hora app (Pathivu, Varisankya, future siblings) shares.
Each app consumes these by copying them in with a small per-app sync script — there is no
published package; the family's mechanism is "generated copies from hora-core" (the same model
as `.github/skills/` and `shared/{android,ios}/`).

**Golden rule:** edit a shared file **here**, then re-run the sync in each app. Never hand-edit
the generated copy inside an app (it is overwritten on the next sync). This mirrors the Android
(`shared/android/`) and iOS (`shared/ios/swift/`) shared layers.

## What's shared

| File | Consumed as | Notes |
| --- | --- | --- |
| `res/css/web_shared.css` | `web/app/web_shared.css` | The design system: `--md-*` → role-token mapping, the Tailwind `@theme` colour aliases, and the M3 component utility classes (`.card`, `.item-*`, `.sheet`, `.pill-*`, `.chip`, `.no-scrollbar`) + shape tokens. |
| `components/ServiceWorker.tsx` | `web/components/ServiceWorker.tsx` | Registers the offline-shell service worker once, client-side, in production. Verbatim. |
| `components/Sheet.tsx` | `web/components/Sheet.tsx` | Bottom-anchored modal sheet (mobile sheet / desktop card) — the web counterpart of the native BottomSheet / SwiftUI `.sheet`. Composes the `.sheet` utility; slide-up + scrim + Escape + scroll-lock. Verbatim. |
| `components/controls.tsx` | `web/components/controls.tsx` | M3 form controls — `Button`, `Switch`, `Field`, `TextInput`, `Select`, `Segmented`. Role-token themed; pure UI. Verbatim. |
| `components/SignIn.tsx` | `web/components/SignIn.tsx` | Google sign-in shell (presentational). Prop-driven (`appName`, `tagline`, `iconSrc`, `onSignIn`, `externalError`) — the caller supplies the app's auth + analytics wiring. Verbatim. |
| `components/ConfirmDialog.tsx` | `web/components/ConfirmDialog.tsx` | Confirmation dialog — Cancel / confirm button pair in a `Sheet`; `danger` swaps to the destructive button, `busy` disables + shows a working label. Prop-driven; the caller owns the action. Verbatim. |
| `components/AboutSheet.tsx` | `web/components/AboutSheet.tsx` | About sheet — app identity (icon + name + sub-label) + description, with an optional list of external legal links. Prop-driven (`appName`, `description`, `iconSrc`, `subLabel`, `links`) and string-free. Verbatim. |

## The 3-layer token architecture

Web theming is single-sourced through three layers (see the header of `web_shared.css`):

1. **`web/app/theme.css`** (app-specific) — the app's Material 3 `--md-*` tonal palette,
   generated from the brand seed (Varisankya) or hand-authored to match the native app
   (Pathivu keeps its Android-matched monochrome neutrals). Flips per light/dark.
2. **`web_shared.css`** (this, shared) — maps `--md-*` → semantic role tokens (`--bg`,
   `--surface*`, `--on-surface*`, `--outline*`, `--primary*`, `--error*`, …), declares the
   Tailwind `@theme` aliases, and ships the component classes. Theme-agnostic, identical per app.
3. **`web/app/globals.css`** (app-specific, thin) — `@import "tailwindcss"; @import "./theme.css";
   @import "./web_shared.css";` plus base styles only (font, `color-scheme`, body).

An app's theme-toggle plumbing (CSS class vs `data-` attribute) stays app-local — only the
**values** under those selectors live in `theme.css`. The role mapping references `--md-*`, so it
works regardless of which selector the app flips.

## Adding a shared file

1. Put the canonical file under `shared/web/` (CSS under `res/css/`, components under
   `components/`). Keep it free of app-specific identifiers — components take props or read role
   tokens; CSS references only `--md-*` / role tokens.
2. Add it to the `FILES` map in each app's `web/scripts/sync_shared_web.sh` (and the family
   template, if one is published).
3. Re-run the sync in each app and let the app's build (`next build`) validate it.

## Bar for inclusion

Same as the rest of `shared/`: at least **two** family apps must use it, and it must be free of
app-specific logic, strings, colours, or business data. Anything carrying those stays in the app
(e.g. `lib/firebase.ts`, the domain model + stats engine, analytics event maps, per-app screens).
