# Hora Notifications Standard (Material 3 Bleeding, strict family standard)

## What this is

**Every Hora Android app sends notifications following the Material 3 "bleeding notification" design** — full-bleed background colours, Dynamic Colour integration, and the app's Malayalam initial as a monochrome 24×24dp small icon. Notifications are immediately recognizable as Hora family members while respecting the system's Material You theme and the app's own brand accent colour.

## Problem this solves

Before: Pathivu and Varisankya notifications looked unrelated — inconsistent icon treatment, no full-bleed colour, no visual cue that they're from the same family.

After: All Hora notifications share a unified structural design while each app remains visually distinct (via its own Malayalam initial + Material You dynamic colour).

## Quick reference

### Template (all three platforms)

```kotlin
NotificationCompat.Builder(context, CHANNEL_ID)
    .setSmallIcon(R.drawable.ic_notification)            // your app's engine-generated icon
    .setContentTitle("Summary (bold, primary)")          
    .setContentText("Optional detail (secondary)")       
    .setSubText("App Name • Time")                        
    .setStyle(BigTextStyle().bigText("Multi-line…"))     
    .setColor(ContextCompat.getColor(context, R.color.md_theme_primary, null))
    .setColorized(true)                                  // Full-bleed background
    .setPriority(NotificationCompat.PRIORITY_HIGH)       
    .setAutoCancel(true)                                 
    .setContentIntent(pendingIntent)                     
    .setVibrate(if (PreferenceHelper.isHapticsEnabled(context)) longArrayOf(0, 200) else longArrayOf(0))
    .build()
```

## Implementation guide

### 1. Small icon (24×24dp vector drawable) — reuse your existing engine-generated one, don't hand-draw a new one

**Check first: your app almost certainly already has the right icon.** Every family app's
`brand/launcher-icon/gen_launcher_icon.py` run (all apps have done this since the icon-geometry
overhaul, beta.35-era) already produces `app/src/main/res/drawable/ic_notification.xml` —
a solid disc with the app's *real* Baloo Chettan 2 Malayalam glyph knocked out (`evenOdd` path,
purpose-built for 24dp legibility, not a naive shrink of the launcher icon). **Use that file and
`setSmallIcon(R.drawable.ic_notification)` directly — do not copy a new `ic_notification_hora.xml`
placeholder.**

**Real incident (Pathivu, 2026-07-10/11):** the notifications-standard rollout copied the
hand-drawn placeholder below into `ic_notification_hora.xml` and switched `setSmallIcon()` to
it, silently regressing the notification shade from the correct engine-generated disc+glyph to a
crude single-stroke approximation. The user caught it as "the notification shade icon is messed
up now, it was correct" — a full release cycle after the regression shipped. Fixed by reverting
`setSmallIcon()` to `R.drawable.ic_notification` and deleting the placeholder file.
**Muthal/Varisankya: check your own `setSmallIcon()` call — if it points at
`ic_notification_hora`, you may have the same regression** (Varisankya's own agent already
caught and declined this trap during its adoption pass — see the wiki adoption table).

**If your app genuinely has no `ic_notification.xml`** (pre-dates the launcher-icon engine, or was
never regenerated) — regenerate it, don't hand-draw one: `python gen_launcher_icon.py <app>` writes
it via `notification_icon()`, matching the launcher wordmark's letterform. **There is no hand-drawn
fallback** — a copy-pasteable placeholder XML used to live here and it caused the exact regression
described above (twice — Pathivu and Muthal both hit it). If the engine can't run in your
environment, stop and get the file some other way (ask the user, or run it in a session that has
the deps) rather than substituting a hand-drawn approximation.

### 2. Configure the notification channel

```kotlin
fun createNotificationChannel(context: Context) {
    val channel = NotificationChannel(
        CHANNEL_ID,
        "App Notifications",
        NotificationManager.IMPORTANCE_HIGH  // Expanded by default
    ).apply {
        description = "Task reminders and updates from the app"
        enableVibration(true)
        vibrationPattern = longArrayOf(0, 200)  // Subtle 200ms tick
        // Light colour (system ignores if Dynamic Colour overrides — that's OK)
        lightColor = Color.CYAN
    }
    context.getSystemService(NotificationManager::class.java)
        .createNotificationChannel(channel)
}
```

**Call this once during app startup** (e.g., in `Application.onCreate()` or lazy in `MainActivity.onCreate()` on first load).

### 3. Send a notification (minimal example)

```kotlin
fun sendNotification(context: Context, title: String, detail: String?, timestamp: String) {
    val builder = NotificationCompat.Builder(context, CHANNEL_ID)
        .setSmallIcon(R.drawable.ic_notification)  // your app's engine-generated icon — not a placeholder
        .setContentTitle(title)  // "24 Pathivus to go today"
        .setSubText("Pathivu • $timestamp")
        
    // Optional: add detail text
    if (!detail.isNullOrEmpty()) {
        builder.setContentText(detail)  // "Start your day strong"
    }
    
    // Optional: add multi-line content via BigTextStyle
    val bigText = """
        Start your day strong
        • Anandhichechik day
        • Wake-up before 10:30 am
        • Good bath
    """.trimIndent()
    builder.setStyle(NotificationCompat.BigTextStyle().bigText(bigText))
    
    // Colour + haptics
    builder
        .setColor(ContextCompat.getColor(context, R.color.md_theme_primary, null))
        .setColorized(true)  // Full-bleed background
        .setPriority(NotificationCompat.PRIORITY_HIGH)
        .setAutoCancel(true)
        .setContentIntent(
            PendingIntent.getActivity(
                context,
                0,
                Intent(context, MainActivity::class.java),
                PendingIntent.FLAG_UPDATE_CURRENT | PendingIntent.FLAG_IMMUTABLE
            )
        )
        .setVibrate(
            if (PreferenceHelper.isHapticsEnabled(context))
                longArrayOf(0, 200)
            else
                longArrayOf(0)
        )
    
    // Send
    NotificationManagerCompat.from(context).notify(NOTIF_ID, builder.build())
}
```

### 4. Multi-line content (lists, expansion)

**For multiple items** (Varisankya's "8 payments due soon" → list of 8), use `InboxStyle()`:

```kotlin
val inbox = NotificationCompat.InboxStyle()
    .setBigContentTitle("8 payments due soon")
    .addLine("Tomorrow • Asianet Internet: INR 884.0")
    .addLine("Tomorrow • Autopay • ET Money Mirae As…")
    .addLine("Tomorrow • Autopay • ET Money Quant EL…")
    .addLine("In 2 days • Azure Cloud: INR 301.1")
    .addLine("In 4 days • Camp Nou LPG: INR 3000.0")
    .addLine("… +3 more")  // System auto-adds if > 5 lines

builder.setStyle(inbox)
```

**For a single long text block** (Pathivu's habit list), use `BigTextStyle()`:

```kotlin
val big = NotificationCompat.BigTextStyle()
    .setBigContentTitle("24 Pathivus to go today")
    .bigText("""
        Start your day strong
        • Anandhichechik day
        • Wake-up before 10:30 am
        • Good bath
        • Shampoo hair
        • Stretching
        • Brush before sleep
        • Anandhichechim day
        • Face care
        • Pix Elvach to sleep
        • Plan food
    """.trimIndent())

builder.setStyle(big)
```

Both expand when the user pulls down the notification shade (or swipes to expand); both maintain the same full-bleed colour scheme.

### 5. Integration with PreferenceHelper (vibration gating)

Already done in hora-core's shared Android source. Just use it:

```kotlin
.setVibrate(
    if (PreferenceHelper.isHapticsEnabled(context))
        longArrayOf(0, 200)
    else
        longArrayOf(0)  // No vibration if disabled
)
```

The user's haptics preference automatically gates notification vibration, matching the scroll haptics standard.

## Validation checklist

Before shipping, verify:

- [ ] **Small icon renders crisp at 24×24dp** — no blurring, anti-aliasing artifacts
- [ ] **Icon is monochrome** (white or light grey fill, no colour gradients)
- [ ] **Icon is immediately recognizable** as your app's Malayalam initial (test by showing non-Malayalam-reading users)
- [ ] **Notification appears with full-bleed background** (not grey/transparent border around it)
- [ ] **Background colour changes with system theme** (dark background in dark mode, light in light mode — system via `colorContainer` token)
- [ ] **Text is readable on the background** (title bold, secondary text outline colour)
- [ ] **Timestamp + app name appear in subtext** (not missing or cut off)
- [ ] **Multi-line content expands cleanly** (no text overlap, bullets/newlines preserved)
- [ ] **Vibration works if haptics enabled** — try toggling `PreferenceHelper.setHapticsEnabled(false)` and re-sending
- [ ] **Vibration is off if haptics disabled** — silent vibration pattern `longArrayOf(0)` produces no buzz
- [ ] **Tapping notification opens the app** to the right screen (habit list, payment list, etc.), not the launcher
- [ ] **Tested on both API 31+** (Material You devices) and **API 26–30** (fallback Dynamic Colours)

## Common mistakes

1. **Using a coloured icon** — icon must be monochrome (white fill). System auto-tints it; you don't hardcode the tint.
2. **Forgetting `setColorized(true)`** — without this, the notification won't have a full-bleed background.
3. **Using a 48×48dp or larger small icon** — system expects 24×24dp. Larger icons get scaled down (blurry).
4. **Hardcoding colours in the icon** — use `@android:color/white` and let the system theme it.
5. **Not creating a notification channel** — Android 8+ requires it; without it, notifications won't show.
6. **Ignoring vibration gating** — always check `PreferenceHelper.isHapticsEnabled()` before vibrating.
7. **Missing `setSubText()`** — include app name + time so users know which app sent the notification.
8. **Overflowing text** — test multi-line content on real devices; use `…` for overflow if needed.

## Files to copy/reference

- **Icon:** none to copy — use your app's own `res/drawable/ic_notification.xml` (regenerate via
  `python gen_launcher_icon.py <app>` if it's missing). No example-icons/ directory exists in this
  skill; it was removed after causing the icon-regression incident described above.
- **Kotlin code:** See `example-code/NotificationHelper.kt` for a reusable notification sender

## When to use this skill

1. **You're shipping a reminder/notification** — use this standard for structure, icon, and colour.
2. **You're redesigning notifications** — compare your current approach against the template above.
3. **You're adding a new notification type** — use the same builder config, just change title/content.
4. **Testing cross-platform consistency** — send a Pathivu notification and a Varisankya notification side by side; they should look like family members.

## Related standards

- `PreferenceHelper` — haptics gating and utilities (shared Android source)
- `Material 3 Expressive` — the theme and colour tokens driving notification appearance
- `Scroll Haptics` — the sibling haptic feedback standard for UI interactions
- Material Design: [Android notification guidelines](https://material.io/design/platform-guidance/android-bars.html#notifications)

## Changelog

- **2026-07-09** — Standard locked, icon templates and code examples finalized. All three apps (Pathivu, Varisankya, Muthal) ready to adopt.
