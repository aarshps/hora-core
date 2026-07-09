# Hora family — brand & design

Shared visual identity for the Hora app family. Anything here is meant to be reused by
two or more apps so they look and feel like siblings.

## What goes here

- **Color & type tokens** — the Material 3 Expressive palette and type scale shared
  across apps.
- **[App icons + brand-mark wide cards](launcher-icon/README.md)** — the unified
  **Baloo Chettan 2 wordmark** engine (`gen_launcher_icon.py`) that generates *every*
  icon and brand mark for an app from one spec, on every surface: Android launcher (all
  densities + monochrome + legacy/round), the notification status-bar icon (solid disc
  with the app's initial knocked out), iOS AppIcon, web favicon/PWA icons, the Play 512,
  the Play Store feature graphic, the web app's Open Graph/Twitter social-share image,
  and each repo's GitHub social-preview card (plus hora-core's own family-lockup
  preview showing all three wordmarks side by side). One algorithm, one look, every
  app, every surface — see `conventions.md` → "Brand mark standard" for the full
  enumerated list and the strict MUST rule (no hand-authored icon or unbranded platform
  default anywhere). The folder holds the engine, the bundled font (OFL), and the
  legacy "വരി" reference vector; the `hora-launcher-icon` skill is the procedure.

- **[Notification design standard](../docs/conventions.md#notification-design-standard-material-3-bleeding-strict-family-standard)** —
  Material 3 "bleeding notification" design applied family-wide. Every Android app sends
  notifications with full-bleed background colour (via `setColorized(true)`), the app's
  Malayalam initial as a monochrome 24×24dp small icon (system auto-tints based on Material
  You theme), and consistent text hierarchy (title + secondary + optional multi-line expansion).
  Notifications are immediately recognizable as Hora family while respecting the system
  theme. Reference: `hora-notifications-standard` skill + example icon/code assets.

## What does not go here

- App-specific screenshots, store listings, or one-off assets — keep those in the
  app's own repo.
- Anything secret or licensed in a way that forbids redistribution (this repo is
  public).

> Populate further as assets are extracted from the apps; keep tokens in a single
> source so the family stays visually consistent.
