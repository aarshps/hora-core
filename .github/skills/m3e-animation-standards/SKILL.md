---
name: m3e-animation-standards
description: Material 3 Expressive (M3E) animation, transition, and touch-physics standards for Hora-family Android apps — duration tokens, cascading list entrances, shared-axis transitions, scroll/FAB behaviour.
---

# Material 3 Expressive (M3E) animation standards

M3E is more dramatic than baseline M3: pronounced scale depth, fast entrances with long
"emphasized" easing tails, heavy touch physics. These are the family-wide rules; each app
implements them with its own helper/constants (don't hardcode the numbers inline).

## Duration tokens
Define three named duration constants app-wide and reference them everywhere — never
hardcode milliseconds in views or XML:
- **short** ~100–200ms — rapid snaps, interactive-press recovery bounce.
- **medium** ~300–400ms — standard layout/state changes.
- **long** ~500ms — activity/fragment shared-axis transitions and large list entrances
  (the signature "fast entrance, long emphasized tail").

## Cascading list entrances
List items must not merely slide up — they cascade from a deeper Z scale:
- Start at `scaleX/scaleY ≈ 0.85`, animate to `1.0` while translating up ~50px.
- Run over the **long** (~500ms) emphasized curve, staggered by item position.

## Cinematic screen transitions
Use `MaterialSharedAxis(MaterialSharedAxis.Z)` for primary activity-to-activity navigation.
The default window-animation duration is too short for M3E — **override `.duration` to the
long token (~500ms)** on both the enter/return and exit/reenter definitions.

## Scroll harmony, FAB, insets
- Attach scroll haptics to lists carrying core data (a mechanical tick on scroll
  milestones); always gate them behind the user's haptics preference (see
  `m3e-haptic-standards`).
- **FAB rule:** a `FloatingActionButton` over a scrollable list must fully `hide()` on
  scroll-down and `show()` on scroll-up. Don't use an Extended FAB for the main feed — it
  permanently obstructs too much vertical space.
- **Edge-to-edge padding:** give lists bottom padding ≈ `inset.bottom + FAB height + margin`
  (~88dp) so the last item can scroll above the resting FAB.

## Checklist
- [ ] No hardcoded animation durations — only the three named tokens.
- [ ] List entrances scale 0.85→1.0 + translate, on the long curve.
- [ ] Shared-axis Z transitions with `.duration` overridden to the long token.
- [ ] FAB hides on scroll-down; lists padded for the resting FAB.
