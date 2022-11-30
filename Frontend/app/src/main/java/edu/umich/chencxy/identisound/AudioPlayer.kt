package edu.umich.chencxy.identisound

import android.Manifest
import android.content.Context
import android.content.pm.PackageManager
import android.media.AudioFormat
import android.media.AudioRecord
import android.media.MediaPlayer
import android.media.MediaRecorder
import android.os.Process.THREAD_PRIORITY_URGENT_AUDIO
import android.os.Process.setThreadPriority
import android.util.Log
import androidx.activity.result.contract.ActivityResultContracts
import androidx.annotation.RequiresPermission
import androidx.annotation.WorkerThread
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.compositionLocalOf
import androidx.compose.runtime.setValue
import androidx.core.app.ActivityCompat
import androidx.navigation.NavHostController
import com.shazam.shazamkit.Catalog
import edu.umich.chencxy.identisound.SongStore.getMovie
import edu.umich.chencxy.identisound.SongStore.getSongTitle
import java.io.*
import java.nio.ByteBuffer
import java.util.*
import kotlin.properties.Delegates

enum class StartMode {
    standby, record,
}
sealed class PlayerState {
    class start(val mode: StartMode): PlayerState()
    object recording: PlayerState()

    fun transition(event: TransEvent): PlayerState {

        return when (this) {
            is start -> when (mode) {
                StartMode.record -> if (event == TransEvent.recTapped) recording else this
                StartMode.standby -> when (event) {
                    TransEvent.recTapped -> recording
                    else -> this
                }
            }
            recording -> when (event) {
                TransEvent.failed -> start(StartMode.record)
                else -> this
            }
        }
    }
}


enum class TransEvent {
    recTapped, failed
}

val LocalAudioPlayer = compositionLocalOf { AudioPlayer() }
class AudioPlayer() {
    lateinit private var audioFilePath: String
    lateinit private var audioRecorder: AudioRecord
    private val mediaPlayer = MediaPlayer()
    lateinit private var audioFormat: AudioFormat

    @RequiresPermission(Manifest.permission.RECORD_AUDIO)
    constructor(context: Context, FilePath: String) : this() {
        audioFilePath = FilePath
        val audioSource = MediaRecorder.AudioSource.UNPROCESSED

        audioFormat = AudioFormat.Builder()
            .setChannelMask(AudioFormat.CHANNEL_IN_MONO)
            .setEncoding(AudioFormat.ENCODING_PCM_16BIT)
            .setSampleRate(48_000)
            .build()

        audioRecorder = AudioRecord.Builder()
            .setAudioSource(audioSource)
            .setAudioFormat(audioFormat)
            .build()
    }

    var playerUIState = UIState()
    var playerState: PlayerState by Delegates.observable(PlayerState.start(StartMode.standby)) { _, _, playerState ->
        playerUIState.propagate(playerState)
    }

    suspend fun recTapped(context: Context, navController: NavHostController) { // attempting
        val recordedBytes = startRecording()
        finishRecording(context, navController, recordedBytes)
    }

     private fun startRecording(): ByteArray {
        // reset player because we'll be re-using the output file that may have been primed at the player.
        mediaPlayer.reset()

        playerState = playerState.transition(TransEvent.recTapped)

        val seconds = 10

         // Final desired buffer size to allocate 12 seconds of audio
         val size = audioFormat.sampleRate * audioFormat.encoding.toByteAllocation() * seconds
         val destination = ByteBuffer.allocate(size)

         // Small buffer to retrieve chunks of audio
         val bufferSize = AudioRecord.getMinBufferSize(
             48_000,
             AudioFormat.CHANNEL_IN_MONO,
             AudioFormat.ENCODING_PCM_16BIT
         )

         audioRecorder.startRecording()
         val readBuffer = ByteArray(bufferSize)
         while (destination.remaining()>0) {
             val actualRead = audioRecorder.read(readBuffer, 0, bufferSize)
             val byteArray = readBuffer.sliceArray(0 until actualRead)
             destination.putTrimming(byteArray)
         }
         audioRecorder.release()
         return destination.array()
    }

    private fun Int.toByteAllocation(): Int {
        return when (this) {
            AudioFormat.ENCODING_PCM_16BIT -> 2
            else -> throw IllegalArgumentException("Unsupported encoding")
        }
    }

    private fun ByteBuffer.putTrimming(byteArray: ByteArray) {
        if (byteArray.size <= this.capacity() - this.position()) {
            this.put(byteArray)
        } else {
            this.put(byteArray, 0, this.capacity() - this.position())
        }
    }

    private suspend fun finishRecording(context: Context, navController: NavHostController, audio: ByteArray) {
        Log.d("pika-pika","called finish recording")
        val songName = getSongTitle(context, audio)

        if (songName == null) {
            // if failed to identify, restart recording
            Log.d("finishRecording", "song was null")
            //getMovie(context, Song("If I Didn't Care"), navController)
            //recTapped(context,navController)
        } else {
            getMovie(context, Song(songName), navController)

        }

        playerState = playerState.transition(TransEvent.recTapped)

    }
}


