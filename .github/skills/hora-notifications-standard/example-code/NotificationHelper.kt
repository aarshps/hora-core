package com.hora.shared.notification

import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.content.Context
import android.content.Intent
import android.graphics.Color
import androidx.core.app.NotificationCompat
import androidx.core.app.NotificationManagerCompat
import androidx.core.content.ContextCompat

/**
 * Hora Notifications Standard — Material 3 Bleeding Notification helper.
 *
 * **Usage:**
 * 1. Call [createNotificationChannel] once during app startup (e.g., Application.onCreate)
 * 2. Call [sendNotification] whenever you need to send a notification
 *
 * **Icon setup:**
 * Use your app's existing engine-generated app/src/main/res/drawable/ic_notification.xml
 * (from gen_launcher_icon.py's notification_icon()) via R.drawable.ic_notification below.
 * Only if that file genuinely doesn't exist yet, fall back to copying
 * example-icons/ic_notification_hora_<APP>.xml → ic_notification_hora.xml and swap the
 * two R.drawable.ic_notification references below to R.drawable.ic_notification_hora.
 *
 * **Customization per app:**
 * - Replace CHANNEL_ID with your app's notification channel ID (e.g., "com.hora.pathivu.reminders")
 * - Replace getString(R.string.app_name) with your app's display name if different
 * - Adjust targetActivity if your app needs to open to a different screen (not MainActivity)
 */
object NotificationHelper {

    // -- Configuration (customize per app) --

    private const val CHANNEL_ID = "com.hora.app.notifications"
    private const val NOTIF_ID_BASE = 1000  // Notification IDs; increment per unique notification

    // -- Public API --

    /**
     * Create the notification channel. Call once during app startup.
     * **Required for Android 8+ (API 26+); call is safe on earlier APIs but does nothing.**
     */
    fun createNotificationChannel(context: Context) {
        val channel = NotificationChannel(
            CHANNEL_ID,
            "App Notifications",
            NotificationManager.IMPORTANCE_HIGH  // Expanded by default
        ).apply {
            description = "Task reminders and updates from the app"
            enableVibration(true)
            vibrationPattern = longArrayOf(0, 200)  // Subtle 200ms tick
            lightColor = Color.CYAN  // Material You will override if available
        }
        context.getSystemService(NotificationManager::class.java)
            .createNotificationChannel(channel)
    }

    /**
     * Send a simple notification (title + optional subtitle + optional expanded content).
     *
     * @param context Android context
     * @param title Main notification title (bold, primary text). E.g., "24 Pathivus to go today"
     * @param subtitle Optional secondary text below title. E.g., "Start your day strong"
     * @param expandedContent Optional multi-line text for the expanded view. If null, only title+subtitle shown.
     *                          Use newlines for multi-line. E.g.: "Habit 1\nHabit 2\n• Habit 3"
     * @param timestamp Formatted timestamp for subtext. E.g., "now" or "3h ago"
     * @param appName App name for subtext. Defaults to getString(R.string.app_name) if null.
     * @param targetActivity Activity class to open when notification is tapped. Defaults to MainActivity.
     * @param notificationId Unique ID for this notification (allows multiple simultaneous notifications). Defaults to 1001.
     */
    fun sendNotification(
        context: Context,
        title: String,
        subtitle: String? = null,
        expandedContent: String? = null,
        timestamp: String = "now",
        appName: String? = null,
        targetActivity: Class<*>? = null,
        notificationId: Int = NOTIF_ID_BASE + 1
    ) {
        val appDisplayName = appName ?: context.getString(context.resources.getIdentifier("app_name", "string", context.packageName))

        val builder = NotificationCompat.Builder(context, CHANNEL_ID)
            .setSmallIcon(context.resources.getIdentifier("ic_notification", "drawable", context.packageName))
            .setContentTitle(title)
            .setSubText("$appDisplayName • $timestamp")  // Metadata: app name + time
            .setColorized(true)  // Full-bleed background
            .setColor(
                ContextCompat.getColor(
                    context,
                    context.resources.getIdentifier("md_theme_primary", "color", context.packageName),
                    null
                )
            )
            .setPriority(NotificationCompat.PRIORITY_HIGH)  // Expanded by default
            .setAutoCancel(true)  // Dismiss on tap

        // Optional: subtitle/secondary text
        if (!subtitle.isNullOrEmpty()) {
            builder.setContentText(subtitle)
        }

        // Optional: expanded multi-line content
        if (!expandedContent.isNullOrEmpty()) {
            val bigTextStyle = NotificationCompat.BigTextStyle()
                .setBigContentTitle(title)
                .bigText(expandedContent)
            builder.setStyle(bigTextStyle)
        }

        // Tap action: open the app
        val intent = Intent(context, targetActivity ?: getDefaultTargetActivity(context))
            .setFlags(Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TOP)
        val pendingIntent = PendingIntent.getActivity(
            context,
            notificationId,
            intent,
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )
        builder.setContentIntent(pendingIntent)

        // Haptics: gated on user preference
        // Import this from the app's own PreferenceHelper (shared Android source)
        // val hapticEnabled = PreferenceHelper.isHapticsEnabled(context)
        // For now, assume haptic preference exists and set vibration pattern accordingly
        // (Apps integrate their own PreferenceHelper.isHapticsEnabled() call here)
        builder.setVibrate(
            longArrayOf(0, 200)  // TODO: gate on PreferenceHelper.isHapticsEnabled(context)
        )

        // Send
        NotificationManagerCompat.from(context).notify(notificationId, builder.build())
    }

    /**
     * Send a notification with a bulleted/numbered list (up to ~5 items; overflow becomes "… +N more").
     * Uses InboxStyle for compact multi-line rendering.
     *
     * @param context Android context
     * @param title Main notification title
     * @param items List of items to display. E.g.: listOf(
     *              "Tomorrow • Asianet Internet: INR 884.0",
     *              "In 2 days • Azure Cloud: INR 301.1"
     *              )
     * @param timestamp Formatted timestamp for subtext
     * @param appName App name for subtext (if null, uses app's default)
     * @param targetActivity Activity to open on tap (if null, uses MainActivity)
     * @param notificationId Unique notification ID
     */
    fun sendListNotification(
        context: Context,
        title: String,
        items: List<String>,
        timestamp: String = "now",
        appName: String? = null,
        targetActivity: Class<*>? = null,
        notificationId: Int = NOTIF_ID_BASE + 2
    ) {
        val appDisplayName = appName ?: context.getString(context.resources.getIdentifier("app_name", "string", context.packageName))

        val inboxStyle = NotificationCompat.InboxStyle()
            .setBigContentTitle(title)

        items.take(5).forEach { item ->  // InboxStyle supports ~5 lines before overflow
            inboxStyle.addLine(item)
        }

        if (items.size > 5) {
            inboxStyle.addLine("… +${items.size - 5} more")
        }

        val builder = NotificationCompat.Builder(context, CHANNEL_ID)
            .setSmallIcon(context.resources.getIdentifier("ic_notification", "drawable", context.packageName))
            .setContentTitle(title)
            .setContentText(if (items.isNotEmpty()) items[0] else "No items")
            .setSubText("$appDisplayName • $timestamp")
            .setStyle(inboxStyle)
            .setColorized(true)
            .setColor(
                ContextCompat.getColor(
                    context,
                    context.resources.getIdentifier("md_theme_primary", "color", context.packageName),
                    null
                )
            )
            .setPriority(NotificationCompat.PRIORITY_HIGH)
            .setAutoCancel(true)

        // Tap action
        val intent = Intent(context, targetActivity ?: getDefaultTargetActivity(context))
            .setFlags(Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TOP)
        val pendingIntent = PendingIntent.getActivity(
            context,
            notificationId,
            intent,
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )
        builder.setContentIntent(pendingIntent)

        // Haptics (TODO: integrate PreferenceHelper.isHapticsEnabled)
        builder.setVibrate(longArrayOf(0, 200))

        NotificationManagerCompat.from(context).notify(notificationId, builder.build())
    }

    // -- Helpers --

    /**
     * Dismiss a notification by ID.
     */
    fun dismissNotification(context: Context, notificationId: Int) {
        NotificationManagerCompat.from(context).cancel(notificationId)
    }

    /**
     * Get the default target activity (MainActivity).
     * **Override this method per app if your entry point is different.**
     */
    private fun getDefaultTargetActivity(context: Context): Class<*> {
        // Default: assume MainActivity exists
        return try {
            Class.forName(context.packageName + ".MainActivity")
        } catch (e: ClassNotFoundException) {
            // Fallback: try to find the app's main launcher activity
            val packageManager = context.packageManager
            val intent = Intent(Intent.ACTION_MAIN)
                .addCategory(Intent.CATEGORY_LAUNCHER)
                .setPackage(context.packageName)
            val resolveInfo = packageManager.resolveActivity(intent, 0)
            if (resolveInfo != null) {
                Class.forName(resolveInfo.activityInfo.name)
            } else {
                // Last resort: return a dummy class (notification will still send, just can't tap)
                NotificationHelper::class.java
            }
        }
    }
}

/**
 * Example usage in an app (e.g., Pathivu):
 *
 * ```kotlin
 * // In Application.onCreate() or MainActivity.onCreate():
 * NotificationHelper.createNotificationChannel(this)
 *
 * // Send a simple habit reminder:
 * NotificationHelper.sendNotification(
 *     context = this,
 *     title = "24 Pathivus to go today",
 *     subtitle = "Start your day strong",
 *     expandedContent = "• Anandhichechik day\n• Wake-up before 10:30 am\n• Good bath",
 *     timestamp = "now",
 *     notificationId = 1001
 * )
 *
 * // Or send a list notification (e.g., Varisankya payments):
 * NotificationHelper.sendListNotification(
 *     context = this,
 *     title = "8 payments due soon",
 *     items = listOf(
 *         "Tomorrow • Asianet Internet: INR 884.0",
 *         "Tomorrow • Autopay • ET Money Mirae As…",
 *         "In 2 days • Azure Cloud: INR 301.1",
 *         "In 4 days • Camp Nou LPG: INR 3000.0"
 *     ),
 *     timestamp = "3h ago",
 *     notificationId = 2001
 * )
 * ```
 */
