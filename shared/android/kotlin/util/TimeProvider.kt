/*
 * Shared Hora-family component — canonical source lives in hora-core/shared/android.
 * It is GENERATED into each app by that app's tools/sync_shared_android.sh. Do NOT
 * hand-edit the copy inside an app; edit it here in hora-core and re-run the sync.
 * (A package placeholder in this file is rewritten to the app's base package on sync.)
 */
package __HORA_PKG__.util

import java.util.Calendar
import java.util.Date

/**
 * Interface to provide the current time.
 * Allows switching between Real Time and Simulated (Sandbox) Time.
 */
interface TimeProvider {
    fun now(): Date
    fun calendar(): Calendar
}

/**
 * Standard implementation returning System time.
 */
class RealTimeProvider : TimeProvider {
    override fun now(): Date {
        return Date()
    }

    override fun calendar(): Calendar {
        return Calendar.getInstance()
    }
}

/**
 * Sandbox implementation allowing time travel.
 */
class SandboxTimeProvider : TimeProvider {
    private var simulatedTime: Long = System.currentTimeMillis()

    fun setTime(date: Date) {
        simulatedTime = date.time
    }
    
    fun setTime(timestamp: Long) {
        simulatedTime = timestamp
    }
    
    fun advanceTime(days: Int) {
        val cal = Calendar.getInstance()
        cal.timeInMillis = simulatedTime
        cal.add(Calendar.DAY_OF_YEAR, days)
        simulatedTime = cal.timeInMillis
    }

    override fun now(): Date {
        return Date(simulatedTime)
    }

    override fun calendar(): Calendar {
        val cal = Calendar.getInstance()
        cal.timeInMillis = simulatedTime
        return cal
    }
}
