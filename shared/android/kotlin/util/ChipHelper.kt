/*
 * Shared Hora-family component — canonical source lives in hora-core/shared/android.
 * It is GENERATED into each app by that app's tools/sync_shared_android.sh. Do NOT
 * hand-edit the copy inside an app; edit it here in hora-core and re-run the sync.
 * The "__HORA_PKG__" token is rewritten to the app's base package on sync.
 */
package __HORA_PKG__.util

import android.content.Context
import com.google.android.material.chip.Chip
import com.google.android.material.chip.ChipGroup
import com.google.android.material.shape.ShapeAppearanceModel

/**
 * Single source of truth for Chip styling and shape logic across the Hora family.
 */
object ChipHelper {

    /**
     * Applies standard Hora-family styling to a chip, including the dynamic shape
     * transition between selected and unselected states and high-contrast M3 colors.
     */
    fun styleChip(chip: Chip) {
        val context = chip.context
        val isChecked = chip.isChecked

        // Resolve shapes
        val r = context.resources.displayMetrics.density
        val selectedRadius = 20f * r

        val unselectedRadius = 100f * r

        chip.shapeAppearanceModel = chip.shapeAppearanceModel.toBuilder()
            .setAllCornerSizes(if (isChecked) selectedRadius else unselectedRadius)
            .build()

        // Apply colors programmatically to bypass XML selector resolution issues in dynamic contexts
        if (isChecked) {
            val bgColor = ThemeHelper.getPrimaryColor(context)
            val textColor = ThemeHelper.getOnPrimaryColor(context)

            chip.chipBackgroundColor = android.content.res.ColorStateList.valueOf(bgColor)
            chip.setTextColor(textColor)
            chip.chipIconTint = android.content.res.ColorStateList.valueOf(textColor)
            chip.checkedIconTint = android.content.res.ColorStateList.valueOf(textColor)

            // Solid background: no border needed
            chip.chipStrokeWidth = 0f
            chip.chipStrokeColor = android.content.res.ColorStateList.valueOf(android.graphics.Color.TRANSPARENT)
        } else {
            val bgColor = ThemeHelper.getSurfaceContainerHighColor(context)
            val textColor = ThemeHelper.getOnSurfaceColor(context)
            val strokeColor = ThemeHelper.getTertiaryColor(context)

            chip.chipBackgroundColor = android.content.res.ColorStateList.valueOf(bgColor)

            chip.setTextColor(textColor)
            chip.chipIconTint = android.content.res.ColorStateList.valueOf(textColor)

            // Subtle border for definition
            chip.chipStrokeWidth = 0.8f * r
            chip.chipStrokeColor = android.content.res.ColorStateList.valueOf(strokeColor)
        }
    }

    /**
     * Styles all chips within a ChipGroup.
     */
    fun styleChipGroup(group: ChipGroup) {
        for (i in 0 until group.childCount) {
            val chip = group.getChildAt(i) as? Chip
            chip?.let { styleChip(it) }
        }
    }
}
