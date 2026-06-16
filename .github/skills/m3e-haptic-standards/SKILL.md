---
name: m3e-haptic-standards
description: Premium "felt" haptic standards for Hora-family Android apps — curate haptics by interaction weight, and always gate them behind a user preference.
---

# M3E haptic standards

For a premium "felt" experience, curate haptics by the weight of the interaction rather
than buzzing on everything. Map each interaction to a framework
`HapticFeedbackConstants` value:

| Interaction | Role | Constant (typical) |
| --- | --- | --- |
| Scrolling milestones | Mechanical tick | `CLOCK_TICK` / `SEGMENT_TICK` |
| Success / save / commit | Confirmation | `CONFIRM` (fallback `LONG_PRESS`) |
| Error / reject | Reject | `REJECT` |
| Toggle / click | Light tick | `VIRTUAL_KEY` / `KEYBOARD_TAP` |
| Long press | Contextual | `LONG_PRESS` |
| Selection delta (dropdowns, sheets) | Tick per change | `SEGMENT_TICK` |

## Rules
- **Always gate haptics behind a user preference.** Route every haptic through one helper
  that early-returns when the user has haptics off — never call `performHapticFeedback`
  directly from activities/adapters. Respecting the toggle is non-negotiable.
- **Scroll feel:** attach a scroll-milestone tick to any list carrying core data.
- **Selection feel:** fire a tick on each selection delta in pickers/bottom sheets.
- Reserve success/error haptics for genuine commit/failure events, not routine taps.

## Checklist
- [ ] Every haptic call goes through the guarded, preference-respecting helper.
- [ ] Interaction→constant mapping matches the table.
- [ ] Lists with core data have scroll-milestone haptics.
