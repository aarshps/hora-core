/*
 * Shared Hora-family component — canonical source lives in hora-core/shared/android.
 * It is GENERATED into each app by that app's tools/sync_shared_android.sh. Do NOT
 * hand-edit the copy inside an app; edit it here in hora-core and re-run the sync.
 * (A package placeholder in this file is rewritten to the app's base package on sync.)
 */
package __HORA_PKG__

import android.content.Context
import android.graphics.Typeface
import android.os.Bundle
import android.util.AttributeSet
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import androidx.activity.enableEdgeToEdge
import com.google.android.material.appbar.CollapsingToolbarLayout
import com.google.android.material.color.DynamicColors

open class BaseActivity : AppCompatActivity() {

    private var currentFontEnabled: Boolean = true

    override fun onCreate(savedInstanceState: Bundle?) {
        enableEdgeToEdge()

        // Cache the current preference value used to create this activity
        currentFontEnabled = PreferenceHelper.isGoogleFontEnabled(this)

        // 1. Apply the Base Theme (decides the font).
        // NOTE: style resource names keep their dots at runtime — aapt2 only replaces
        // dots with underscores in the generated Java `R` field name (R.style.Theme_App),
        // not in the resource table entry itself, which Resources.getIdentifier() matches
        // against literally. Verified with `aapt2 dump resources` against a built APK:
        // the compiled entry is "style/Theme.Muthal.SystemFont", never
        // "style/Theme_Muthal.SystemFont". An earlier "Theme_" (underscore) prefix here
        // never matched anything, so setTheme() silently no-op'd (styleRes == 0) and the
        // System-font option appeared to do nothing — the toggle persisted the
        // preference correctly, but the visual theme swap never actually happened.
        val styleRes = if (!currentFontEnabled) {
            resources.getIdentifier("Theme.${resources.getString(R.string.app_name)}.SystemFont", "style", packageName)
        } else {
            resources.getIdentifier("Theme.${resources.getString(R.string.app_name)}", "style", packageName)
        }
        if (styleRes != 0) {
            setTheme(styleRes)
        }

        // VITAL: Re-apply Dynamic Colors because the manual setTheme() above overrides
        // the global Application callback (which happens in onActivityPreCreated).
        DynamicColors.applyToActivityIfAvailable(this)

        super.onCreate(savedInstanceState)
    }

    override fun onResume() {
        super.onResume()
        // Check if the preference has changed since this activity was created/last resumed.
        // If it has changed (e.g., changed in SettingsActivity and we are now returning to MainActivity),
        // we recreate this activity to apply the new theme.
        if (currentFontEnabled != PreferenceHelper.isGoogleFontEnabled(this)) {
            recreate()
        }
    }

    // 2. Belt-and-braces font override. The theme swap above (step 1) is correct and
    // does reach most TextViews, but repeated real-world testing found individual
    // TextAppearance/widget-style declarations that hardcode the brand font by literal
    // reference (not through a themed attr) keep resurfacing — a shared type style, a
    // widget default style, a one-off layout override — each is a different bug, but
    // they all have the same symptom (a title/subtitle stuck in the brand font under
    // "System font"). Rather than keep chasing individual declarations, force every
    // TextView (and its subclasses: Button, MaterialButton, EditText, Chip, etc.) to
    // the platform default typeface when the toggle is off, regardless of how its font
    // was declared upstream. AppCompatActivity.onCreateView is the documented hook for
    // post-processing inflated views — including views inflated by Fragments and
    // BottomSheetDialogFragments hosted in this Activity, since their inflaters clone
    // this Activity's factory chain. But it only intercepts framework-named tags
    // ("TextView", "Button", ...): for fully-qualified tags (Material components like
    // <com.google.android.material.chip.Chip>) AppCompat's factory returns null and the
    // inflater instantiates them reflectively, bypassing this hook entirely.
    override fun onCreateView(parent: View?, name: String, context: Context, attrs: AttributeSet): View? {
        val view = super.onCreateView(parent, name, context, attrs)
        if (!currentFontEnabled && view is TextView) applySystemTypeface(view)
        return view
    }

    // ...so onContentChanged() (fired when setContentView completes) walks the whole
    // Activity view tree and catches everything the factory hook missed: Material
    // components declared with fully-qualified tags, and CollapsingToolbarLayout —
    // whose large/collapsed titles are drawn internally by CollapsingTextHelper (not a
    // TextView child), so they can only be reached via its explicit typeface setters.
    // Dialog/bottom-sheet windows have their own content views and are not walked here,
    // but their text views are framework-named tags covered by the factory hook above.
    override fun onContentChanged() {
        super.onContentChanged()
        if (!currentFontEnabled) applySystemFontTree(window.decorView)
    }

    private fun applySystemTypeface(view: TextView) {
        val style = view.typeface?.style ?: Typeface.NORMAL
        view.typeface = Typeface.create(Typeface.DEFAULT, style)
    }

    private fun applySystemFontTree(view: View) {
        when (view) {
            is TextView -> applySystemTypeface(view)
            is CollapsingToolbarLayout -> {
                view.setExpandedTitleTypeface(Typeface.DEFAULT)
                view.setCollapsedTitleTypeface(Typeface.DEFAULT)
            }
        }
        if (view is ViewGroup) {
            for (i in 0 until view.childCount) applySystemFontTree(view.getChildAt(i))
        }
    }
}
