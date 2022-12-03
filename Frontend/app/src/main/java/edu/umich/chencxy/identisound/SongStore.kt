package edu.umich.chencxy.identisound

import android.content.Context
import android.os.Build
import android.util.Log
import androidx.compose.runtime.*
import androidx.navigation.NavHostController
import com.android.volley.Request
import com.android.volley.RequestQueue
import com.android.volley.toolbox.JsonObjectRequest
import com.android.volley.toolbox.Volley.newRequestQueue
import com.shazam.shazamkit.*
import org.json.JSONArray
import org.json.JSONException
import org.json.JSONObject
import java.util.*
import kotlin.reflect.full.declaredMemberProperties

object SongStore {
    private val _songs = mutableStateListOf<Song>()
    private val _movies = mutableStateListOf<Movie>()
    val songs: List<Song> = _songs
    val movies: List<Movie> = _movies

    private lateinit var queue: RequestQueue
    private const val serverUrl = "https://54.226.221.81/"

//    suspend fun getSongTitle(context: Context, audio: ByteArray?): String? {
//        //DEBUG = true turns off Shazam function... For testing front end quickly.
//        val DEBUG = true
//        if (DEBUG){return "Singin' in the Rain"} //If I Didn't Care
//        val signatureGenerator = (ShazamKit.createSignatureGenerator(AudioSampleRateInHz.SAMPLE_RATE_48000) as ShazamKitResult.Success).data
//
//        audio?.let {
//            signatureGenerator.append(
//                it,
//                audio.size,
//                System.currentTimeMillis()
//            )
//        }
//        val signature = signatureGenerator.generateSignature()
//
//        val catalog = ShazamKit.createShazamCatalog(DevTokenProvider(context), null)
//        val session = (ShazamKit.createSession(catalog) as ShazamKitResult.Success).data
//
//        val songName: String? =
//            when (val match = session.match(signature)) {
//                 is MatchResult.Match -> {
//                    Log.d("shazam success", match.matchedMediaItems.toString())
//                    match.matchedMediaItems[0].title
//                }
//                is MatchResult.Error -> {
//                    Log.d("shazam error", match.exception.toString())
//                    "No Song Found"
//                }
//                is MatchResult.NoMatch -> {
//                    Log.d("shazam none", match.querySignature.toString())
//                    "No Song Found"
//                }
//            }
//
//        return songName
//    }

    fun getSongTitle(context: Context, audio: ByteArray?, navController: NavHostController) {
        Log.d("ML", "getSongTitleML called")
        if (audio == null) {
            Log.d("ML", "getSongTitleML with null audio")
            return
        }

        val b64AudioString = String(Base64.getEncoder().encode(audio))
        val fileName = "testAudio.pcm"

        val jsonObj = mapOf(
            "fileName" to fileName,
            "file" to b64AudioString,
        )

        Log.d("ML", jsonObj.toString())
        Log.d("ML sending", b64AudioString)

        val postRequest = JsonObjectRequest(Request.Method.POST,
            serverUrl+"postAudio/", JSONObject(jsonObj),
            {
                    response ->
                Log.d("ML postAudio response", response.toString())
                val songName = try {response.getString("songName")
                } catch (e: JSONException) { null }

                getMovie(context, Song(songName), navController)
            },
            { error -> Log.e("ML Audio", error.localizedMessage ?: "JsonObjectRequest error") }
        )

        if (!this::queue.isInitialized) {
            queue = newRequestQueue(context)
        }
        queue.add(postRequest)
    }

    fun getMovie(context: Context, song: Song, navController: NavHostController){
        Log.d("pikapika","getMovie")
        val jsonObj = mapOf(
            "songName" to song.Songname,
        )
        val postRequest = JsonObjectRequest(Request.Method.POST,
            serverUrl+"getsongs/", JSONObject(jsonObj),
            {
                response ->
                val MovieReceived = try {response.getJSONArray("movies")
                } catch (e: JSONException) { JSONArray() }

                _movies.clear()

                for (i in 0 until MovieReceived.length()) {
                    Log.d("pikapika","Inside Line 86")
                    // Movie Title
                    // Movie Year
                    // Movie Director
                    // Movie Media Poster Link
                    val movie = MovieReceived[i] as JSONArray
                    _movies.add(Movie(movie[0].toString(),movie[1].toString(),movie[2].toString(),movie[3].toString())) //get the name of the movie
                }
                _songs.add(song)
                navController.navigate("MovieView")
            },
            { error -> Log.e("postSong", error.localizedMessage ?: "JsonObjectRequest error") }
        )

        if (!this::queue.isInitialized) {
            queue = newRequestQueue(context)
        }
        queue.add(postRequest)
    }
}