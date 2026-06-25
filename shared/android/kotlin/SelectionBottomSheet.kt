/*
 * Shared Hora-family component — canonical source lives in hora-core/shared/android.
 * It is GENERATED into each app by that app's tools/sync_shared_android.sh. Do NOT
 * hand-edit the copy inside an app; edit it here in hora-core and re-run the sync.
 * (A package placeholder in this file is rewritten to the app's base package on sync.)
 */
package __HORA_PKG__

import android.os.Bundle
import android.view.HapticFeedbackConstants
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import com.google.android.material.bottomsheet.BottomSheetBehavior
import com.google.android.material.bottomsheet.BottomSheetDialog
import com.google.android.material.bottomsheet.BottomSheetDialogFragment
import com.google.android.material.chip.Chip
import com.google.android.material.chip.ChipGroup

class SelectionBottomSheet(
    private val title: String,
    private val options: Array<String>,
    private val selectedOption: String?,
    private val onOptionSelected: (String) -> Unit
) : BottomSheetDialogFragment() {

    override fun onCreateDialog(savedInstanceState: Bundle?): android.app.Dialog {
        val dialog = super.onCreateDialog(savedInstanceState)
        dialog.window?.setSoftInputMode(android.view.WindowManager.LayoutParams.SOFT_INPUT_ADJUST_PAN)
        return dialog
    }

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        val view = inflater.inflate(R.layout.bottom_sheet_selection, container, false)

        val titleTextView = view.findViewById<TextView>(R.id.selection_title)
        val chipGroup = view.findViewById<ChipGroup>(R.id.selection_chip_group)
        val dragHandle = view.findViewById<View>(R.id.drag_handle)
        val scrollView = view.findViewById<androidx.core.widget.NestedScrollView>(R.id.selection_scroll_view)
        
        // M3E Mechanical Scroll Feel
        PreferenceHelper.attachNestedScrollHaptics(scrollView)

        dragHandle.setOnClickListener {
            PreferenceHelper.performHaptics(it, HapticFeedbackConstants.CLOCK_TICK)
        }

        titleTextView.text = title

        options.forEach { option ->
            val chip = Chip(requireContext())
            chip.text = option
            chip.isCheckable = true
            chip.isCheckedIconVisible = false
            chip.isChecked = option == selectedOption
            chip.setEnsureMinTouchTargetSize(false)
            updateChipStyle(chip)

            chip.setOnClickListener { v ->
                PreferenceHelper.performHaptics(v, HapticFeedbackConstants.VIRTUAL_KEY)
                onOptionSelected(option)
                dismiss()
            }
            chipGroup.addView(chip)
        }

        return view
    }

    private fun updateChipStyle(chip: Chip) {
        __HORA_PKG__.util.ChipHelper.styleChip(chip)
    }

    override fun onStart() {
        super.onStart()
        val bottomSheet = (dialog as? BottomSheetDialog)?.findViewById<View>(com.google.android.material.R.id.design_bottom_sheet)
        val behavior = (dialog as? BottomSheetDialog)?.behavior
        val dragHandle = view?.findViewById<View>(R.id.drag_handle)

        if (bottomSheet != null && behavior != null && dragHandle != null) {
            behavior.addBottomSheetCallback(object : BottomSheetBehavior.BottomSheetCallback() {
                override fun onStateChanged(bottomSheet: View, newState: Int) {
                    when (newState) {
                        BottomSheetBehavior.STATE_EXPANDED -> {
                            dragHandle.animate().scaleX(1.2f).scaleY(1.2f).setDuration(Constants.ANIM_DURATION_SHORT).setInterpolator(androidx.interpolator.view.animation.FastOutSlowInInterpolator())
                                .withEndAction { dragHandle.animate().scaleX(1f).scaleY(1f).setInterpolator(androidx.interpolator.view.animation.FastOutSlowInInterpolator()).start() }
                                .start()
                            PreferenceHelper.performHaptics(dragHandle, HapticFeedbackConstants.CONFIRM)
                        }
                        BottomSheetBehavior.STATE_DRAGGING -> {
                            dragHandle.animate().scaleX(0.9f).scaleY(0.9f).setDuration(Constants.ANIM_DURATION_SHORT).setInterpolator(androidx.interpolator.view.animation.FastOutSlowInInterpolator()).start()
                            PreferenceHelper.performHaptics(dragHandle, HapticFeedbackConstants.CLOCK_TICK)
                        }
                        BottomSheetBehavior.STATE_SETTLING, BottomSheetBehavior.STATE_COLLAPSED -> {
                            dragHandle.animate().scaleX(1f).scaleY(1f).setDuration(Constants.ANIM_DURATION_SHORT).setInterpolator(androidx.interpolator.view.animation.FastOutSlowInInterpolator()).start()
                        }
                    }
                }

                override fun onSlide(bottomSheet: View, slideOffset: Float) {}
            })
        }
    }
}
