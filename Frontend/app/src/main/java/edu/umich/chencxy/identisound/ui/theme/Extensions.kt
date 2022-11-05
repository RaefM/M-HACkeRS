package edu.umich.chencxy.identisound.ui.theme

import android.content.Context
import android.widget.Toast

fun Context.toast(message: String, short: Boolean = true) {
    Toast.makeText(this, message, if (short) Toast.LENGTH_SHORT else Toast.LENGTH_LONG).show()
}