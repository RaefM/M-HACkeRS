package edu.umich.chencxy.identisound

import android.content.Context
import com.shazam.shazamkit.DeveloperToken
import com.shazam.shazamkit.DeveloperTokenProvider

class DevTokenProvider(private val context: Context) : DeveloperTokenProvider {
    override fun provideDeveloperToken(): DeveloperToken {
        return DeveloperToken(context.getString(R.string.devToken))
    }
}