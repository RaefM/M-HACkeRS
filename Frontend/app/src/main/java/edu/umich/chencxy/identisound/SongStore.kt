package edu.umich.chencxy.identisound

import android.content.Context
import android.util.Log
import androidx.compose.runtime.*
import com.android.volley.Request
import com.android.volley.RequestQueue
import com.android.volley.toolbox.JsonObjectRequest
import com.android.volley.toolbox.Volley.newRequestQueue
import org.json.JSONArray
import org.json.JSONException
import org.json.JSONObject
import kotlin.reflect.full.declaredMemberProperties

object SongStore {
    private val _chatts = mutableStateListOf<Song>()
    val chatts: List<Song> = _chatts
    private val nFields = Song::class.declaredMemberProperties.size

    private lateinit var queue: RequestQueue
    private const val serverUrl = "https://54.226.221.81/"
    fun postSong(context: Context, song: Song) {
        val jsonObj = mapOf(
            "uri" to Song.audio
        )
        val postRequest = JsonObjectRequest(Request.Method.POST,
            serverUrl+"postaudio/", JSONObject(jsonObj),
            {
                Log.d("postSong", "Song posted!")
                getSong(context)
            },
            { error -> Log.e("postSong", error.localizedMessage ?: "JsonObjectRequest error") }
        )

        if (!this::queue.isInitialized) {
            queue = newRequestQueue(context)
        }
        queue.add(postRequest)
    }

    fun getSongTitle(context: Context) {
        val getRequest = JsonObjectRequest(serverUrl+"/"+R.string.songaudio,
            { response ->
                val chattsReceived = try { response.getJSONArray("Song_Name") } catch (e: JSONException) { JSONArray() }
//                for (i in 0 until chattsReceived.length()) {
//                    val chattEntry = chattsReceived[i] as JSONArray
//                    if (chattEntry.length() == nFields) {
//                        _chatts.add(Song(Songname = chattEntry[0].toString(),
//                            audio = chattEntry[3].toString()
//                        ))
//                    } else {
//                        Log.e("getaudio",
//                            "Received unexpected number of fields: " + chattEntry.length()
//                                .toString() + " instead of " + nFields.toString()
//                        )
//                    }
//                }
            }, {}
        )

        if (!this::queue.isInitialized) {
            queue = newRequestQueue(context)
        }
        queue.add(getRequest)
    }
}