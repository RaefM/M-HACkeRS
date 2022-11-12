package edu.umich.chencxy.identisound

import android.content.Context
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
import kotlin.reflect.full.declaredMemberProperties

object SongStore {
    private val _songs = mutableStateListOf<Song>()
    private val _movies = mutableStateListOf<Movie>()
    val songs: List<Song> = _songs
    val movies: List<Movie> = _movies
    private val nFields = Song::class.declaredMemberProperties.size

    private lateinit var queue: RequestQueue
    private const val serverUrl = "https://54.226.221.81/"
    var song_name = "We'll live through the long long days, and through the long nights "
    var movie_name = "Drive my car"
//    fun postSong(context: Context, song: Song) {
//        val jsonObj = mapOf(
//            "songName" to song.Songname,
//        )
//        val postRequest = JsonObjectRequest(Request.Method.POST,
//            serverUrl+"getsongs/", JSONObject(jsonObj),
//            {
//                Log.d("postSong", "Song posted!")
////                getSongTitle(song)
//            },
//            { error -> Log.e("postSong", error.localizedMessage ?: "JsonObjectRequest error") }
//        )
//
//        if (!this::queue.isInitialized) {
//            queue = newRequestQueue(context)
//        }
//        queue.add(postRequest)
//    }

    suspend fun getSongTitle(context: Context, audio: ByteArray?): String? {
        /*
        val signatureGenerator = (ShazamKit.createSignatureGenerator(AudioSampleRateInHz.SAMPLE_RATE_48000) as ShazamKitResult.Success).data

        audio?.let {
            signatureGenerator.append(
                it,
                audio.size,
                System.currentTimeMillis()
            )
        }
        val signature = signatureGenerator.generateSignature()

        val catalog = ShazamKit.createShazamCatalog(DevTokenProvider(context), null)
        val session = (ShazamKit.createSession(catalog) as ShazamKitResult.Success).data

        val songName: String? =
            when (val match = session.match(signature)) {
                is MatchResult.Match -> match.matchedMediaItems[0].title
                is MatchResult.NoMatch -> null
                is MatchResult.Error -> null
            }

        return songName*/
        val songName = "If I Didn't Care"
        return songName
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
                for (i in 0 until MovieReceived.length()) {
                    Log.d("pikapika","Inside Line 86")
                    val movie = MovieReceived[i] as JSONArray
                    _movies.add(Movie(movie[0].toString())) //get the name of the movie


                //    val movie = MovieReceived.getJSONObject(i)
                //    _movies.add(Movie(movie.getString("name")))
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

//    fun getSongTitle(context: Context) {
//        val getRequest = JsonObjectRequest(serverUrl+"/"+R.string.songaudio,
//            { response ->
//                val chattsReceived = try { response.getJSONArray("Song_Name") } catch (e: JSONException) { JSONArray() }
////                for (i in 0 until chattsReceived.length()) {
////                    val chattEntry = chattsReceived[i] as JSONArray
////                    if (chattEntry.length() == nFields) {
////                        _chatts.add(Song(Songname = chattEntry[0].toString(),
////                            audio = chattEntry[3].toString()
////                        ))
////                    } else {
////                        Log.e("getaudio",
////                            "Received unexpected number of fields: " + chattEntry.length()
////                                .toString() + " instead of " + nFields.toString()
////                        )
////                    }
////                }
//            }, {}
//        )
//
//        if (!this::queue.isInitialized) {
//            queue = newRequestQueue(context)
//        }
//        queue.add(getRequest)
//    }
}