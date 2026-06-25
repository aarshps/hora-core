---
name: web-platform-standards
description: Standard operating guidelines for Hora web projects (Next.js, Tailwind v4, TypeScript), covering layout responsive flow, glassmorphism, dynamic theme variables, and parity validations.
---

# Web Platform Standards

Every Hora web project (Next.js App Router, Tailwind CSS v4, TypeScript) must satisfy the following guidelines to guarantee a premium, responsive, and platform-aligned user experience.

## 1. Responsive & Fluid Layouts
- **Mobile-first Design:** Design target is a clean, premium mobile application. Maximum content width is capped at `max-w-md` (or centered container on wider screens) to maintain app-like density.
- **Header & Navigation:** Headers must scroll with content, but primary navigation controls/actions (e.g. Floating Action Buttons or navigation bars) must be pinned or structured naturally within the fluid frame.
- **Glassmorphism & Surface radiuses:** Use the standard CSS variables (`--radius-large`, `--radius-pill`) for cards, item groups, and buttons to keep in step with the Android/iOS layouts.

## 2. Theming & Color Palette
- **M3 Palette Seeding:** Seeds the Material 3 tonal palette from the app's brand icon color using the Material Color Utilities (`SchemeTonalSpot`). Do not use browser-level dynamic wallpaper colors.
- **Dark Mode Support:** All interactive elements must support light and dark mode toggles cleanly. Always bind theme attributes on the `:root` element (`data-theme="light"` or `data-theme="dark"`).
- **Native Color Schemes:** Set `color-scheme` property in CSS so native browser controls (pickers, scrollbars, dialogs) render using the correct light/dark theme color.

## 3. Parity & Validation Rules
- **Golden Parity Testing:** Every web project must consume the shared `golden-vectors.json` vectors to assert correctness of:
  - Recurrence unit arithmetic (clamping at month boundaries).
  - Indian-influenced currency formatting and suffix abbreviations (`compactFormat`).
- **Persistence Mirroring:** Mirror all transaction writes to the authoritative nested subcollection AND the flat mirror `payments` collection for performant read lookups (exactly like Android and iOS clients).
