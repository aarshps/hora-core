# Hora family — brand & design

Shared visual identity for the Hora app family. Anything here is meant to be reused by
two or more apps so they look and feel like siblings.

## What goes here

- **Color & type tokens** — the Material 3 Expressive palette and type scale shared
  across apps.
- **[App icons](launcher-icon/README.md)** — the unified **Baloo Chettan 2 wordmark**
  engine (`gen_launcher_icon.py`) that generates *every* icon for an app from one spec:
  Android launcher (all densities + monochrome + legacy/round), the notification
  status-bar icon (solid disc with the app's initial knocked out), iOS AppIcon, web
  favicon/PWA icons, and the Play 512. One algorithm, one look, both apps. The folder
  holds the engine, the bundled font (OFL), and the legacy "വരി" reference vector; the
  `hora-launcher-icon` skill is the procedure.
- **Shared imagery / logos** — family-level marks, not app-specific screenshots.

## What does not go here

- App-specific screenshots, store listings, or one-off assets — keep those in the
  app's own repo.
- Anything secret or licensed in a way that forbids redistribution (this repo is
  public).

> Populate further as assets are extracted from the apps; keep tokens in a single
> source so the family stays visually consistent.
