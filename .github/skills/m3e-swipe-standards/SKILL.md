---
name: m3e-swipe-standards
description: Smooth, sticky, haptic swipe-to-act on list rows for Hora-family Android apps — the gesture feel AND the wiring rule that stops a kept (non-removed) row from sticking off-screen.
---

# M3E swipe-action standards

The family's list swipe-to-act (Pathivu swipe-to-mark-done, Varisankya swipe-to-mark-paid) is one
shared feel: a sticky, springy, haptic right-swipe that reveals an accent panel + check icon, then
settles back into place. The row is **never removed** — the swipe just toggles state.

Reference impls (copy `SwipeActionCallback` per app; it references the app's own `R`/colors):
Varisankya `util/SwipeHelpers.kt` + `SubscriptionActionHelper`; Pathivu the same `SwipeHelpers.kt`
+ `HabitActionHelper`. Keep the behaviour below identical.

## The gesture (SwipeActionCallback : ItemTouchHelper.SimpleCallback)
- **Right-swipe only** for the action; paint the reveal (accent background + check) in `onChildDraw`.
- **Sticky damping** for the "sticks, then tears past" feel: within a `STICK_ZONE` (~0.15 of width)
  the row follows the finger at `STICK_FOLLOW_RATIO` (~0.45); past it, 1:1. Apply the damped dX to
  BOTH the row translation and the painted reveal width.
- **Escalating haptics** (all via the gated preference helper — see `m3e-haptic-standards`): a light
  tick on first nudge (~0.05 of width), a stronger tick at the sticky-zone exit (~0.15).
- **Keep ItemTouchHelper's natural recover** (standard `getSwipeThreshold` ≈ 0.4). That recover IS the
  smooth, bouncy spring-back — do NOT replace it with an instant `translationX = 0` snap or a
  "no-commit" (`getSwipeThreshold`/`getSwipeEscapeVelocity` maxed-out) hack: those stop the stuck but
  feel stuttery and cheap.

## The wiring rule — THIS is what prevents the stuck (get it right)
The row isn't removed, so it must be restored AND the data write must not fight the recover:
1. In `onSwipeRight`, call `adapter.notifyItemChanged(position)` **synchronously** (not `post`ed) —
   this springs the row smoothly back.
2. Fire the data write **only after the spring-back animation settles** — NEVER an immediate async
   write in `onSwipeRight`. Its `updateData`/DiffUtil rebind otherwise lands mid-recover, cancels it,
   and leaves the row **stuck off-screen at the edge**.
   - Deferring behind a confirmation sheet (Varisankya) satisfies this — the write fires long after.
   - With no confirmation (Pathivu), defer **event-based, not on a fixed timer** (a timer races on
     slow devices): `recyclerView.postOnAnimation { recyclerView.itemAnimator?.isRunning { <write> } }`.

## Checklist
- [ ] `SwipeActionCallback` copied per app; sticky damping + escalating haptics + natural recover intact.
- [ ] `onSwipeRight` does a SYNCHRONOUS `notifyItemChanged`.
- [ ] Data write fires only after animations settle (confirm sheet or `itemAnimator.isRunning`), never immediately.
- [ ] Verified on-device: smooth, no stutter, the row never sticks at the edge.
