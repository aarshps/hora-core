/*
 * Shared Hora-family component — canonical source lives in hora-core/shared/android.
 * It is GENERATED into each app by that app's tools/sync_shared_android.sh. Do NOT
 * hand-edit the copy inside an app; edit it here in hora-core and re-run the sync.
 * (A package placeholder in this file is rewritten to the app's base package on sync.)
 */
package __HORA_PKG__.util

import android.content.Context
import android.graphics.Canvas
import android.graphics.Color
import android.graphics.Paint
import android.graphics.PorterDuff
import android.graphics.PorterDuffXfermode
import android.graphics.RectF
import android.graphics.drawable.Drawable
import android.os.Build
import android.view.HapticFeedbackConstants
import android.view.View
import androidx.core.content.ContextCompat
import androidx.recyclerview.widget.ItemTouchHelper
import androidx.recyclerview.widget.RecyclerView
import com.google.android.material.card.MaterialCardView
import com.google.android.material.color.MaterialColors
import __HORA_PKG__.R
import __HORA_PKG__.PreferenceHelper
import kotlin.math.abs

abstract class SwipeActionCallback(private val context: Context) : ItemTouchHelper.SimpleCallback(0, ItemTouchHelper.LEFT or ItemTouchHelper.RIGHT) {

    private val deleteIcon: Drawable? = ContextCompat.getDrawable(context, R.drawable.ic_delete_sweep)
    private val pauseIcon: Drawable? = ContextCompat.getDrawable(context, R.drawable.ic_pause)
    private val checkIcon: Drawable? = ContextCompat.getDrawable(context, R.drawable.ic_check_circle)

    private val intrinsicWidth = deleteIcon?.intrinsicWidth ?: 0
    private val intrinsicHeight = deleteIcon?.intrinsicHeight ?: 0

    private val deleteColor by lazy { ThemeHelper.getErrorColor(context) }
    private val inactiveColor by lazy { ThemeHelper.getSurfaceContainerHighestColor(context) }
    private val paidColor by lazy { ThemeHelper.getPrimaryColor(context) }

    private val clearPaint = Paint().apply { xfermode = PorterDuffXfermode(PorterDuff.Mode.CLEAR) }
    private val backgroundPaint = Paint().apply { style = Paint.Style.FILL }

    // Haptic State Tracking
    private val hapticStateMap = mutableMapOf<Long, HapticState>()
    private data class HapticState(
        var hasTriggeredStart: Boolean = false,
        var hasTriggeredRelease: Boolean = false,
        var hasTriggeredDeep: Boolean = false
    )

    private val DEEP_SWIPE_THRESHOLD = 0.5f

    // "Sticky → release" damping (mirrors Android notification swipe feel).
    // While the finger is inside the sticky zone, the item only follows at
    // STICK_FOLLOW_RATIO; past the zone it follows 1:1, carrying the offset
    // it accumulated inside the zone. Net effect: small touches "stick", a
    // firmer drag "tears" past the resistance.
    private val STICK_ZONE = 0.15f
    private val STICK_FOLLOW_RATIO = 0.45f

    private fun applyStickyDamping(dX: Float, viewWidth: Float): Float {
        if (viewWidth <= 0f) return dX
        val sign = if (dX < 0f) -1f else 1f
        val rawProgress = abs(dX) / viewWidth
        val dampedProgress = if (rawProgress <= STICK_ZONE) {
            rawProgress * STICK_FOLLOW_RATIO
        } else {
            STICK_ZONE * STICK_FOLLOW_RATIO + (rawProgress - STICK_ZONE)
        }
        return sign * dampedProgress * viewWidth
    }

    // Manual reorder via long-press drag (vertical) — disabled by default so the
    // swipe-only screens are unaffected; the home list opts in by flipping this.
    var dragEnabled = false
    private var didDrag = false

    /** Home's outer scroller; when a dragged row hits the top/bottom edge we scroll it
     *  (the RecyclerView itself is non-scrolling inside this NestedScrollView, so
     *  ItemTouchHelper's built-in auto-scroll never fires). */
    var dragScrollView: androidx.core.widget.NestedScrollView? = null
    private val edgeDensity get() = context.resources.displayMetrics.density

    private fun autoScrollEdges(viewHolder: RecyclerView.ViewHolder) {
        val sv = dragScrollView ?: return
        val svLoc = IntArray(2); sv.getLocationOnScreen(svLoc)
        val itemLoc = IntArray(2); viewHolder.itemView.getLocationOnScreen(itemLoc)
        val centerY = itemLoc[1] + viewHolder.itemView.height / 2f
        val top = svLoc[1]
        val bottom = svLoc[1] + sv.height
        val edge = 96f * edgeDensity
        val maxStep = 22f * edgeDensity
        val step = when {
            centerY < top + edge -> -(((top + edge - centerY) / edge).coerceIn(0f, 1f) * maxStep)
            centerY > bottom - edge -> ((centerY - (bottom - edge)) / edge).coerceIn(0f, 1f) * maxStep
            else -> 0f
        }
        if (step != 0f) sv.scrollBy(0, step.toInt())
    }

    override fun getMovementFlags(
        recyclerView: RecyclerView,
        viewHolder: RecyclerView.ViewHolder
    ): Int {
        if (viewHolder.itemViewType != 0) return 0
        val dragFlags = if (dragEnabled) ItemTouchHelper.UP or ItemTouchHelper.DOWN else 0
        return makeMovementFlags(dragFlags, ItemTouchHelper.RIGHT)
    }

    override fun isLongPressDragEnabled(): Boolean = dragEnabled

    override fun onMove(
        recyclerView: RecyclerView,
        viewHolder: RecyclerView.ViewHolder,
        target: RecyclerView.ViewHolder
    ): Boolean {
        val from = viewHolder.bindingAdapterPosition
        val to = target.bindingAdapterPosition
        if (from == RecyclerView.NO_POSITION || to == RecyclerView.NO_POSITION) return false
        PreferenceHelper.performHaptics(viewHolder.itemView, HapticFeedbackConstants.SEGMENT_TICK)
        didDrag = true
        return onMoveItem(from, to)
    }

    override fun onSelectedChanged(viewHolder: RecyclerView.ViewHolder?, actionState: Int) {
        super.onSelectedChanged(viewHolder, actionState)
        if (actionState == ItemTouchHelper.ACTION_STATE_DRAG && viewHolder != null) {
            PreferenceHelper.performSuccessHaptic(viewHolder.itemView)
            viewHolder.itemView.animate().scaleX(1.03f).scaleY(1.03f).setDuration(120).start()
        }
    }

    override fun clearView(recyclerView: RecyclerView, viewHolder: RecyclerView.ViewHolder) {
        super.clearView(recyclerView, viewHolder)
        viewHolder.itemView.animate().scaleX(1f).scaleY(1f).setDuration(120).start()
        if (didDrag) {
            didDrag = false
            onDragFinished()
        }
    }

    /** Reorder hook — adapter swaps + notifyItemMoved. Default no-op. */
    open fun onMoveItem(from: Int, to: Int): Boolean = false

    /** Called once a drag gesture settles, to persist the new order. Default no-op. */
    open fun onDragFinished() {}

    override fun onChildDraw(
        c: Canvas,
        recyclerView: RecyclerView,
        viewHolder: RecyclerView.ViewHolder,
        dX: Float,
        dY: Float,
        actionState: Int,
        isCurrentlyActive: Boolean
    ) {
        if (actionState == ItemTouchHelper.ACTION_STATE_DRAG && isCurrentlyActive) {
            autoScrollEdges(viewHolder)
        }
        val itemView = viewHolder.itemView
        val itemHeight = itemView.bottom - itemView.top
        val viewWidth = itemView.width.toFloat()
        val isCanceled = dX == 0f && !isCurrentlyActive

        if (isCanceled) {
            clearCanvas(c, itemView.right + dX, itemView.top.toFloat(), itemView.right.toFloat(), itemView.bottom.toFloat())
            super.onChildDraw(c, recyclerView, viewHolder, dX, dY, actionState, isCurrentlyActive)
            return
        }

        val id = viewHolder.itemId
        val state = hapticStateMap.getOrPut(id) { HapticState() }
        val rawProgress = abs(dX) / viewWidth

        if (dX == 0f) {
            state.hasTriggeredStart = false
            state.hasTriggeredRelease = false
            state.hasTriggeredDeep = false
        }

        val dampedDx = applyStickyDamping(dX, viewWidth)
        val radius = if (itemView is MaterialCardView) itemView.radius else 28f

        if (dampedDx > 0) {
            val nudgeThreshold = 0.05f
            if (rawProgress > nudgeThreshold && !state.hasTriggeredStart) {
                PreferenceHelper.performHaptics(itemView, HapticFeedbackConstants.SEGMENT_TICK)
                state.hasTriggeredStart = true
            }
            if (rawProgress > STICK_ZONE && !state.hasTriggeredRelease) {
                PreferenceHelper.performHaptics(itemView, HapticFeedbackConstants.GESTURE_START)
                state.hasTriggeredRelease = true
            }

            backgroundPaint.color = paidColor

            val background = RectF(
                itemView.left.toFloat(),
                itemView.top.toFloat(),
                itemView.left.toFloat() + dampedDx,
                itemView.bottom.toFloat()
            )
            c.drawRoundRect(background, radius, radius, backgroundPaint)

            val iconMargin = (itemHeight - intrinsicHeight) / 2
            val iconTop = itemView.top + (itemHeight - intrinsicHeight) / 2
            val iconBottom = iconTop + intrinsicHeight
            val iconLeft = itemView.left + iconMargin
            val iconRight = itemView.left + iconMargin + intrinsicWidth

            checkIcon?.setBounds(iconLeft, iconTop, iconRight, iconBottom)
            checkIcon?.setTint(ThemeHelper.getOnPrimaryColor(context))
            checkIcon?.draw(c)
        }

        super.onChildDraw(c, recyclerView, viewHolder, dampedDx, dY, actionState, isCurrentlyActive)
    }

    private fun clearCanvas(c: Canvas?, left: Float, top: Float, right: Float, bottom: Float) {
        c?.drawRect(left, top, right, bottom, clearPaint)
    }

    override fun getSwipeThreshold(viewHolder: RecyclerView.ViewHolder): Float = 0.4f

    abstract fun onSwipeRight(position: Int)

    override fun onSwiped(viewHolder: RecyclerView.ViewHolder, direction: Int) {
        val position = viewHolder.bindingAdapterPosition
        val id = viewHolder.itemId
        hapticStateMap.remove(id)
        if (direction == ItemTouchHelper.RIGHT) {
            onSwipeRight(position)
        }
    }
}
