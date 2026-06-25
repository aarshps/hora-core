/*
 * Shared Hora-family component — canonical source lives in hora-core/shared/android.
 * It is GENERATED into each app by that app's tools/sync_shared_android.sh. Do NOT
 * hand-edit the copy inside an app; edit it here in hora-core and re-run the sync.
 * (A package placeholder in this file is rewritten to the app's base package on sync.)
 */
package __HORA_PKG__.util

import android.content.Context
import android.view.HapticFeedbackConstants
import androidx.recyclerview.widget.ItemTouchHelper
import androidx.recyclerview.widget.RecyclerView
import __HORA_PKG__.PreferenceHelper

/**
 * Long-press drag-to-reorder for the habit list. There is **no row-swipe action** —
 * Pathivu marks a habit done via the row's check button (swipe-to-mark-done was
 * removed). This callback only handles vertical drag reordering.
 */
abstract class DragReorderCallback(private val context: Context) :
    ItemTouchHelper.SimpleCallback(ItemTouchHelper.UP or ItemTouchHelper.DOWN, 0) {

    // Reorder via long-press drag — disabled by default; the home list opts in by
    // flipping this so screens that attach the callback without reorder are unaffected.
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
        return makeMovementFlags(dragFlags, 0)
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

    override fun onChildDraw(
        c: android.graphics.Canvas,
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
        super.onChildDraw(c, recyclerView, viewHolder, dX, dY, actionState, isCurrentlyActive)
    }

    /** Reorder hook — adapter swaps + notifyItemMoved. Default no-op. */
    open fun onMoveItem(from: Int, to: Int): Boolean = false

    /** Called once a drag gesture settles, to persist the new order. Default no-op. */
    open fun onDragFinished() {}

    // Swipe is intentionally disabled (swipeDirs = 0); onSwiped never fires.
    override fun onSwiped(viewHolder: RecyclerView.ViewHolder, direction: Int) {}
}
