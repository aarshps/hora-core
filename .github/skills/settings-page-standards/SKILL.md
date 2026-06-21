---
name: settings-page-standards
description: The Hora-family Settings screen design language — large/collapsing title, titled grouped cards, chip/segmented selectors, a profile header, and a dedicated sign-out button — across Android, iOS, and web.
---

# Settings page standards

Every Hora app's Settings screen shares one design language (reference: **Varisankya**). The content
differs per app (Pathivu: tracking/day-start/week-start/archived; Varisankya: currency/notification-days),
but the **structure and components are identical**. Keep these consistent; only swap the rows.

## Shared anatomy (all platforms)
- A **large title** ("Settings") that collapses/pins on scroll.
- A **profile header** card at top: avatar + display name + email.
- The body is a vertical stack of **titled cards** (rounded ~28dp, filled surface-container), each
  led by its **section name as an in-card header** — NOT a small label floating above the card.
- Inside a card: rows are `title + subtitle + trailing control`. Trailing control is a **switch**
  (on/off), a **segmented/chip selector** (small enumerations like theme, font, haptics), or a
  **value chip / SelectionRow** that opens a picker sheet (day-start, week-start, currency, time).
- Multi-row cards separate rows with a thin **divider**.
- **Sign out** (and Delete account, where present) are **full-width buttons at the very bottom**,
  in the error/danger colour — never buried as a plain text row mid-list.

## Android (`SettingsActivity` + `activity_settings.xml`)
- `CoordinatorLayout` bg `?attr/colorSurfaceContainerLow`; `AppBarLayout` + **`CollapsingToolbarLayout`**
  (height 152dp, `scroll|exitUntilCollapsed|snap`, `titleCollapseMode=scale`,
  expanded `TextAppearance.App.DisplaySmall`, collapsed `TextAppearance.App.TitleLarge`). Back arrow
  via `setSupportActionBar` + `setDisplayHomeAsUpEnabled` + `setHomeAsUpIndicator(ic_back)` +
  `setDisplayShowTitleEnabled(false)`; handle `onSupportNavigateUp`.
- Each section = `MaterialCardView` (`materialCardViewFilledStyle`, `colorSurfaceContainer`,
  `card_corner_radius_large` = 28dp, stroke 0, margins `card_margin_horizontal`=16 /
  `group_section_spacing`=12, padding `card_padding_*`=16) with a `TextAppearance.App.TitleLarge`
  header, then `TitleSmall`+`BodySmall` rows.
- Apply **grouped corner shaping at runtime** so stacked cards read as one block: first/middle/last/
  single via `ShapeAppearance.App.{First,Middle,Last,Single}Item` (`setupCardGrouping`). The logout
  card is excluded (its own 24dp radius).
- Selectors are `ChipGroup` (single-selection) styled by the shared `ChipHelper.styleChipGroup`
  (selected = filled primary squircle, unselected = pill). Display "value" chips (current
  day-start/week-start/time) are checked chips styled via `ChipHelper.styleChip`.
- A **dark-mode** control (System/Light/Dark chips) writes an `AppCompatDelegate` night-mode int to
  prefs and is applied at startup in the `Application` (`setDefaultNightMode`) so it **persists across
  cold starts**.

## iOS (`SettingsView.swift`)
- `ScrollView { VStack(spacing: 16) { … } }`, `.navigationBarTitleDisplayMode(.large)`, rounded
  design font throughout.
- `GlassFormCard` (`.glassEffect(in: .rect(cornerRadius: 28))`) per section, led by `SectionLabel`
  (uppercase, tracked). Rows use `LabelStack` (title+subtitle) + `Toggle`, or `SelectionRow`
  (label→value→chevron) that presents a glass `SelectionSheet`. `ProfileCard` at top.
- Appearance uses a `.segmented` `Picker`. Sign out / Delete account are bottom `.buttonStyle(.glass)
  .controlSize(.extraLarge)` buttons (delete `.tint(.red)`).

## Web (`settings`)
- A scroll of rounded titled cards (`SectionLabel` inside each), a profile card at top, an Appearance
  **segmented pill** (selected = accent / on-primary), switches for toggles, native selects/inputs
  for enumerations, and **bottom full-width Sign out (outline) + Delete account (danger)** buttons.
- Use the app's own design tokens (`--accent`, `--danger`, `--surface-*`, `--on-surface*`); don't
  hard-code colours.

## Checklist
- [ ] Large/collapsing title; profile header card.
- [ ] Titled cards (section name inside the card), grouped/rounded, with dividers between rows.
- [ ] Switches / chip-or-segmented selectors / value-chip→sheet, consistent per the row's kind.
- [ ] Sign out (+ Delete) are full-width error-coloured buttons at the bottom.
- [ ] Dark-mode choice persists across restarts (where the app offers one).
