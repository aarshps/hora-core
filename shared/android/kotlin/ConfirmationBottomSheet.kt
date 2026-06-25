/*
 * Shared Hora-family component — canonical source lives in hora-core/shared/android.
 * It is GENERATED into each app by that app's tools/sync_shared_android.sh. Do NOT
 * hand-edit the copy inside an app; edit it here in hora-core and re-run the sync.
 * (A package placeholder in this file is rewritten to the app's base package on sync.)
 */
package __HORA_PKG__

import android.content.DialogInterface
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import android.widget.TextView
import com.google.android.material.bottomsheet.BottomSheetDialogFragment
import __HORA_PKG__.util.ThemeHelper

class ConfirmationBottomSheet(
    private val title: String,
    private val message: String,
    private val positiveButtonText: String,
    private val negativeButtonText: String = "Cancel",
    private val isDestructive: Boolean = false,
    private val onConfirm: () -> Unit,
    private val onCancel: () -> Unit = {}
) : BottomSheetDialogFragment() {

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        val view = inflater.inflate(R.layout.bottom_sheet_confirmation, container, false)
        
        val textTitle = view.findViewById<TextView>(R.id.text_title)
        val textMessage = view.findViewById<TextView>(R.id.text_message)
        val btnConfirm = view.findViewById<Button>(R.id.btn_confirm)
        val btnCancel = view.findViewById<Button>(R.id.btn_cancel)
        
        textTitle.text = title
        textMessage.text = message
        btnConfirm.text = positiveButtonText
        btnCancel.text = negativeButtonText
        
        if (isDestructive) {
            btnConfirm.setBackgroundColor(ThemeHelper.getErrorColor(requireContext()))
            btnConfirm.setTextColor(ThemeHelper.getOnErrorColor(requireContext()))
        } else {
            // Default Primary
            btnConfirm.setBackgroundColor(ThemeHelper.getPrimaryColor(requireContext()))
            btnConfirm.setTextColor(ThemeHelper.getOnPrimaryColor(requireContext()))
        }
        
        btnConfirm.setOnClickListener {
            PreferenceHelper.performSuccessHaptic(it)
            onConfirm()
            dismiss()
        }
        
        btnCancel.setOnClickListener {
            PreferenceHelper.performClickHaptic(it)
            onCancel()
            dismiss()
        }
        
        // Drag handle animation
        val dragHandle = view.findViewById<View>(R.id.drag_handle)
        dragHandle.setOnClickListener {
            PreferenceHelper.performClickHaptic(it)
        }

        return view
    }
    
    override fun onCancel(dialog: DialogInterface) {
        super.onCancel(dialog)
        onCancel()
    }
}
