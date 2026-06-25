/*
 * Shared Hora-family component — canonical source lives in hora-core/shared/android.
 * It is GENERATED into each app by that app's tools/sync_shared_android.sh. Do NOT
 * hand-edit the copy inside an app; edit it here in hora-core and re-run the sync.
 * (A package placeholder in this file is rewritten to the app's base package on sync.)
 */
package __HORA_PKG__

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import androidx.activity.enableEdgeToEdge
import com.google.android.material.color.DynamicColors

open class BaseActivity : AppCompatActivity() {
    
    private var currentFontEnabled: Boolean = true

    override fun onCreate(savedInstanceState: Bundle?) {
        enableEdgeToEdge()
        
        // Cache the current preference value used to create this activity
        currentFontEnabled = PreferenceHelper.isGoogleFontEnabled(this)
        
        // 1. Apply the Base Theme (decides the font)
        val styleRes = if (!currentFontEnabled) {
            resources.getIdentifier("Theme_${resources.getString(R.string.app_name)}.SystemFont", "style", packageName)
        } else {
            resources.getIdentifier("Theme_${resources.getString(R.string.app_name)}", "style", packageName)
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
}
