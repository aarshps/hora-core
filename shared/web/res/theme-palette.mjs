/*
 * Canonical Hora family web palette — the single source of truth for the
 * `--md-*` colour VALUES every Hora web app uses.
 *
 * Family web design language: **neutral surfaces + uniform accents**. The surface
 * scale is a clean **monochrome neutral** (no brand tint), identical across apps;
 * the accent is the **uniform family accent** (a brand-neutral indigo/periwinkle),
 * not a per-app brand colour — so the whole family reads as one app, with no
 * ad-hoc per-brand styling offsets.
 *
 * How apps consume it (each app keeps its own light/dark toggle plumbing — a
 * `data-theme` attribute vs a `.dark`/`.light` class — so only the VALUES are
 * shared, not the selectors):
 *   - Varisankya: `web/scripts/gen-theme.mjs` imports this (synced to
 *     `web/scripts/theme-palette.mjs`) and emits `app/theme.css` with its own selectors.
 *   - An app hand-authoring `theme.css` matches these exact values.
 *
 * Edit here in hora-core and re-sync; never hand-edit the synced copy.
 */

export const LIGHT = {
  // Monochrome neutral surface scale
  background: "#fafafa",
  surface: "#fafafa",
  surfaceContainerLowest: "#ffffff",
  surfaceContainerLow: "#f5f5f5",
  surfaceContainer: "#ededed",
  surfaceContainerHigh: "#e0e0e0",
  surfaceContainerHighest: "#d6d6d6",
  surfaceVariant: "#e0e0e0",
  onSurface: "#1c1b1f",
  onSurfaceVariant: "#404040",
  outline: "#79747e",
  outlineVariant: "#c4c4c4",
  // Uniform family accent (brand-neutral indigo) + error
  primary: "#475d92",
  onPrimary: "#ffffff",
  primaryContainer: "#f5f5f5",
  onPrimaryContainer: "#475d92",
  secondaryContainer: "#ededed",
  onSecondaryContainer: "#404040",
  error: "#b3392f",
  onError: "#ffffff",
  errorContainer: "rgba(179, 57, 47, 0.12)",
  onErrorContainer: "#b3392f",
};

export const DARK = {
  // Monochrome neutral surface scale
  background: "#121212",
  surface: "#121212",
  surfaceContainerLowest: "#0f0f0f",
  surfaceContainerLow: "#1a1a1a",
  surfaceContainer: "#212121",
  surfaceContainerHigh: "#2b2b2b",
  surfaceContainerHighest: "#333333",
  surfaceVariant: "#2b2b2b",
  onSurface: "#ececec",
  onSurfaceVariant: "#b3b3b3",
  outline: "#8c8c8c",
  outlineVariant: "#3a3a3a",
  // Uniform family accent (brand-neutral periwinkle) + error
  primary: "#aec6ff",
  onPrimary: "#102f60",
  primaryContainer: "#1a1a1a",
  onPrimaryContainer: "#aec6ff",
  secondaryContainer: "#212121",
  onSecondaryContainer: "#b3b3b3",
  error: "#e08077",
  onError: "#0f0f0f",
  errorContainer: "rgba(224, 128, 119, 0.15)",
  onErrorContainer: "#e08077",
};
