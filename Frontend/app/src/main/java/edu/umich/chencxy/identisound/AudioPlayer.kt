package edu.umich.chencxy.identisound

import android.content.Context
import android.media.MediaPlayer
import android.media.MediaRecorder
import android.os.Handler
import android.util.Log
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.compositionLocalOf
import androidx.compose.runtime.setValue
import java.io.*
import java.util.*
import kotlin.concurrent.schedule
import kotlin.properties.Delegates


enum class StartMode {
    standby, record,
}
sealed class PlayerState {
    class start(val mode: StartMode): PlayerState()
    object recording: PlayerState()
//    class playing(val parent: StartMode): PlayerState()
//    class paused(val grand: StartMode): PlayerState()

    fun transition(event: TransEvent): PlayerState {
//        if (event == TransEvent.doneTapped) {
//            return start(StartMode.standby)
//        }
        return when (this) {
            is start -> when (mode) {
                StartMode.record -> if (event == TransEvent.recTapped) recording else this
//                StartMode.play -> if (event == TransEvent.playTapped) playing(StartMode.play) else this
                StartMode.standby -> when (event) {
                    TransEvent.recTapped -> recording
//                    TransEvent.playTapped -> playing(StartMode.standby)
                    else -> this
                }
            }
            recording -> when (event) {
//                TransEvent.recTapped -> start(StartMode.standby)
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
    var audio: ByteArray? by mutableStateOf(null)
    lateinit private var audioFilePath: String
    lateinit private var mediaRecorder: MediaRecorder
    private val mediaPlayer = MediaPlayer()

    constructor(context: Context, FilePath: String) : this() {
        audioFilePath = FilePath
        mediaRecorder = MediaRecorder(context)
    }

    var playerUIState = UIState()
    var playerState: PlayerState by Delegates.observable(PlayerState.start(StartMode.standby)) { _, _, playerState ->
        playerUIState.propagate(playerState)


        // change if statement to timer 10sec
        // set up the button and link to UIstate
        // check with uploading

    }

    fun recTapped() {
        if (playerState == PlayerState.recording) {
            finishRecording()
        } else {
            startRecording()
            Timer("stoprecording", false).schedule(10000){
                if(playerState == PlayerState.recording) {
                    recTapped()
                }
            }
        }
    }

     fun startRecording() {
        // reset player because we'll be re-using the output file that may have been primed at the player.
        mediaPlayer.reset()

        playerState = playerState.transition(TransEvent.recTapped)

        with (mediaRecorder) {
            setAudioSource(MediaRecorder.AudioSource.MIC)
            setOutputFormat(MediaRecorder.OutputFormat.MPEG_4)
            setAudioEncoder(MediaRecorder.AudioEncoder.AAC)
            setOutputFile(audioFilePath)
            try {
                prepare()
            } catch (e: IOException) {
                Log.e("startRecording: ", e.localizedMessage ?: "IOException")
                return
            }
            this.start()
        }
    }


    private fun finishRecording() {
        mediaRecorder.stop()
        mediaRecorder.reset()
        try {
            val fis = FileInputStream(audioFilePath)
            val bos = ByteArrayOutputStream()
            var read: Int
            val audioBlock = ByteArray(65536)
            while (fis.read(audioBlock, 0, audioBlock.size).also { read = it } != -1) {
                bos.write(audioBlock, 0, read)
            }
            audio = bos.toByteArray()
            bos.close()
            fis.close()
        } catch (e: IOException) {
            Log.e("finishRecording: ", e.localizedMessage ?: "IOException")
            playerState = playerState.transition(TransEvent.failed)
            return
        }
        playerState = playerState.transition(TransEvent.recTapped)
    }

    fun doneTapped() {
        if (playerState == PlayerState.recording) {
            finishRecording()
        } else {
            mediaRecorder.reset()
        }
        mediaPlayer.start() // so that playback works on revisit
//        TransEvent.stopTapped()
//        playerState = playerState.transition(TransEvent.doneTapped)
    }
}


