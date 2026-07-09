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
    .setSmallIcon(R.drawable.ic_notification_hora)       // 24×24dp monochrome
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

### 1. Create the small icon (24×24dp vector drawable)

Each app has its own icon reflecting its Malayalam initial. Copy the reference example below and adapt for your app's letter.

**File:** `app/src/main/res/drawable/ic_notification_hora.xml` (shared name across all apps; content is app-specific)

#### Pathivu example (പ — "pa")
```xml
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="24dp"
    android:height="24dp"
    android:viewportWidth="24"
    android:viewportHeight="24">
    <path android:fillColor="@android:color/white"
        android:pathData="M6.5,4c-1.38,0 -2.5,1.12 -2.5,2.5v11c0,1.38 1.12,2.5 2.5,2.5h11c1.38,0 2.5,-1.12 2.5,-2.5v-11c0,-1.38 -1.12,-2.5 -2.5,-2.5h-11zm5,3h3v3h-3v-3zm0,4h3v3h-3v-3zm-3,-2h2v2h-2v-2z" />
</vector>
```

**Design guidelines for your icon:**
- **Size:** 24×24dp viewport
- **Style:** Monochrome outline/simple fill, Material Symbols 2.0 aesthetic
- **Stroke:** Single uniform weight (no thin/heavy contrast)
- **Content:** The app's Malayalam initial glyph, **simplified for small scale**
  - Pathivu (പ): single main stroke without serifs or complex curves
  - Varisankya (വ): triangular/angular letterform, distinct shape
  - Muthal (മ): taller/more complex form, but distilled to essentials
- **Colour:** `@android:color/white` (vector drawable uses white; system auto-tints it based on theme)
- **Padding:** minimal (the glyph should nearly touch the 24×24 viewport edge for maximum visibility)

**Why simplified Malayalam glyphs?** At 24×24dp, fine details are lost. A full Baloo Chettan 2 rendering of പ/വ/മ is illegible. Instead, create a **stylized monogram** — a simple, recognizable lettermark that's:
- Instantly readable as the app's initial
- Scalable without detail loss
- Consistent with Material Symbols 2.0 line-art philosophy

**Inspiration:** See `shared/android/res/drawable/ic_*.xml` in hora-core for reference icon style.

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
        .setSmallIcon(R.drawable.ic_notification_hora)
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

- **Icon template:** See this skill's `example-icons/` folder
  - `ic_notification_hora_pathivu.xml`
  - `ic_notification_hora_varisankya.xml`
  - `ic_notification_hora_muthal.xml`
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
