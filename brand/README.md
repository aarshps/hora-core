# Hora family — brand & design

Shared visual identity for the Hora app family. Anything here is meant to be reused by
two or more apps so they look and feel like siblings.

## What goes here

- **Color & type tokens** — the Material 3 Expressive palette and type scale shared
  across apps.
- **[Launcher icon](launcher-icon/README.md)** — the Malayalam wordmark style every Hora
  app's icon follows (each app's short name drawn in the shared hand-authored style). The
  folder holds the **canonical reference** (Varisankya's "വരി" vector + preview) and the
  exact **target metrics** (colour, face, stem weight, bounding-circle fill) a new app's
  icon must match; the `hora-launcher-icon` skill is the step-by-step generation procedure.
- **[Notification status-bar icon](notification-icon/README.md)** — the solid-disc /
  hollow-glyph generator every app copies and customizes. Extracted from Varisankya
  (the first app to need it); Pathivu and future siblings reuse the identical
  construction with their own initial.
- **Shared imagery / logos** — family-level marks, not app-specific screenshots.

## What does not go here

- App-specific screenshots, store listings, or one-off assets — keep those in the
  app's own repo.
- Anything secret or licensed in a way that forbids redistribution (this repo is
  public).

> Populate further as assets are extracted from the apps; keep tokens in a single
> source so the family stays visually consistent.
