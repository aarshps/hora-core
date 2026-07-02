---
name: splash-and-home-standards
description: The Hora-family splash screen and Home screen anatomy — identical structure across Android, iOS, and web for every family app (reference — Varisankya/Pathivu). Settings has its own skill (settings-page-standards).
---

# Splash & Home screen standards

Every Hora app boots and lands the same way on every platform. The **content** differs per
app (Varisankya: subscriptions; Pathivu: habits; Muthal: institution ledger) but the
**structure is identical**. Reference implementation: **Varisankya** (Pathivu matches).

## Splash screen

### Android (`androidx.core:core-splashscreen`)
- Theme (in `values/themes.xml`):
  ```xml
  <style name="Theme.App.Starting" parent="Theme.SplashScreen">
      <!-- windowSplashScreenBackground stays default (system) -->
      <item name="windowSplashScreenAnimatedIcon">@drawable/ic_splash_icon_centered</item>
      <item name="postSplashScreenTheme">@style/Theme.<App></item>
  </style>
  ```
- `drawable/ic_splash_icon_centered.xml` is a layer-list wrapping the launcher icon,
  108dp, centered:
  ```xml
  <layer-list><item android:drawable="@mipmap/ic_launcher" android:gravity="center"
      android:width="108dp" android:height="108dp"/></layer-list>
  ```
- The manifest sets `android:theme="@style/Theme.App.Starting"` on **both** the
  `<application>` and the launcher activity.
- `MainActivity.onCreate` calls `installSplashScreen()` **before** `super.onCreate()`, and
  uses `setKeepOnScreenCondition { … }` to hold the splash until the app knows its first
  frame: auth state resolved + (if App-Lock is enabled) biometric gate passed + first data
  snapshot ready. Never flash the login screen at a signed-in user.

### iOS
- No storyboard. XcodeGen `Info.plist` properties:
  `UILaunchScreen: { UIColorName: AccentColor }` — the system generates the launch frame.

### Web
- No splash asset. While Firebase auth resolves, render a centered **boot frame** — the
  app icon card + app name (the same visual as the sign-in card, minus the button). The
  shell must never flash the sign-in view at a signed-in user.

## Home screen

### Android (`activity_main.xml`)
Top-level: `CoordinatorLayout`, background `?attr/colorSurface`.

⚠️ **Insets pitfall (caused a real "empty gap above the toolbar" bug):** the
`AppBarLayout`'s own `fitsSystemWindows="true"` already consumes/pads for the status
bar. Do **not** also apply a manual `WindowInsetsCompat` top-padding to the root — that
double-applies the status-bar inset. A window-insets listener on the root should only
handle the **bottom** inset (FAB margin + list/scroll clearance), exactly as Varisankya's
`MainActivity` does.

1. **App bar** — `AppBarLayout` (`fitsSystemWindows`, elevation 0dp, `liftOnScroll=false`)
   → `MaterialToolbar` (height `?attr/actionBarSize`, `contentInsetStart/End=24dp`):
   - **Left — "jewel logo" + name:** a `MaterialCardView` (radius 10dp,
     `colorSurfaceContainerHigh`, elevation 0) holding a 32dp `@mipmap/ic_launcher_round`
     `ImageView`, then the app name 14dp to the right — `textAppearanceHeadlineSmall`,
     22sp, bold, letterSpacing −0.02, `includeFontPadding=false`.
   - **Right — profile avatar:** 32dp `ShapeableImageView` (circular overlay), fed the
     Google account `photoUrl` by a lightweight coroutine loader (`URL(...).openStream()`
     → `BitmapFactory` on IO, set on Main) — no image-loading library. Tapping it opens
     **Settings** (sign-out lives in Settings, never on the home toolbar).
2. **Body** — `SwipeRefreshLayout` → `NestedScrollView` (`fillViewport`) → vertical
   `LinearLayout` containing:
   - a **skeleton include** (`layout_home_skeleton`: skeleton hero + N skeleton rows,
     surfaces `colorSurfaceContainerHigh(est)` — see `skeleton-loading-standards`),
     visible while loading;
   - the **content wrapper** (`gone` until first data): the **hero card**
     (`MaterialCardView`, radius 28dp, `colorSurfaceContainerHigh`, 16dp margins, 20dp
     padding; a `LabelLarge` primary-coloured bold label with letterSpacing 0.1 over a
     bold auto-size Display number), the app's **list** (`RecyclerView`,
     `nestedScrollingEnabled=false`, `clipToPadding=false`, bottom padding), and the
     **empty-state container**.
3. **FAB** — `ExtendedFloatingActionButton`
   (`Widget.Material3.ExtendedFloatingActionButton.Tertiary`), `bottom|end`, margin 16dp,
   `ic_add` icon + short label ("Add").
4. **Signed-out state** — the same activity hides app bar/body/FAB and shows a centered
   **login container**: app icon, app name, tagline, "Continue with Google" button.

### iOS (`HomeView.swift`)
- `NavigationStack`; large-title = app name; trailing toolbar item = profile avatar
  (opens Settings). Hero glass card (28pt corners) with label + Display number, then the
  grouped list, `EmptyState` when empty; bottom-trailing extended add button. Rounded
  design font throughout.

### Web (`App` / `Home`)
Already codified as the four family-look rules (Shared-Web wiki) + shared components:
neutral surfaces + uniform accent, the shared **`AppBar`** (leading = settings gear,
**centered title**, trailing = app action e.g. history), the hero card, **`.grouped-list`**
items, the shared extended **`Fab`**, `EmptyState`, and a `SignIn` card when signed out.

## Settings
See **`settings-page-standards`** — large collapsing title, profile header card, titled
grouped cards, chip/segmented selectors, bottom full-width Sign out (+ Delete account).

## Checklist
- [ ] Android: `Theme.App.Starting` on application + launcher activity; `installSplashScreen()`
      + keep-condition; no login-screen flash for signed-in users.
- [ ] Android home: jewel-logo toolbar + avatar→Settings; SwipeRefresh + NestedScroll;
      skeleton → hero → list → empty state; extended FAB; login container for signed-out.
- [ ] iOS: `UILaunchScreen` plist config; NavigationStack large title; hero card + list +
      extended add button; avatar/settings in toolbar.
- [ ] Web: boot frame while auth resolves; AppBar/Fab/grouped-list/EmptyState from shared/web.
- [ ] Settings per `settings-page-standards` on all three platforms.
