package edu.umich.chencxy.identisound

import android.content.Context
import android.media.MediaPlayer
import android.media.MediaRecorder
import android.util.Base64
import android.util.Log
import androidx.compose.runtime.compositionLocalOf
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import java.io.*
import kotlin.properties.Delegates


enum class StartMode {
    standby, record, play
}
sealed class PlayerState {
    class start(val mode: StartMode): PlayerState()
    object recording: PlayerState()
    class playing(val parent: StartMode): PlayerState()
    class paused(val grand: StartMode): PlayerState()

    fun transition(event: TransEvent): PlayerState {
        if (event == TransEvent.doneTapped) {
            return start(StartMode.standby)
        }
        return when (this) {
            is start -> when (mode) {
                StartMode.record -> if (event == TransEvent.recTapped) recording else this
                StartMode.play -> if (event == TransEvent.playTapped) playing(StartMode.play) else this
                StartMode.standby -> when (event) {
                    TransEvent.recTapped -> recording
                    TransEvent.playTapped -> playing(StartMode.standby)
                    else -> this
                }
            }
            recording -> when (event) {
                TransEvent.recTapped, TransEvent.stopTapped -> start(StartMode.standby)
                TransEvent.failed -> start(StartMode.record)
                else -> this
            }
            is playing -> when (event) {
                TransEvent.playTapped -> paused(this.parent)
                TransEvent.stopTapped, TransEvent.failed -> start(this.parent)
                else -> this
            }
            is paused -> when (event) {
                TransEvent.recTapped -> recording
                TransEvent.playTapped -> playing(this.grand)
                TransEvent.stopTapped -> start(StartMode.standby)
                else -> this
            }
        }
    }
}


enum class TransEvent {
    recTapped, playTapped, stopTapped, doneTapped, failed
}

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
        UIState.propagate(playerState)


        // change ifstatement to timer 10sec
        // set up the button and link to UIstate
        // check with uploading

        fun recTapped() {
            if (playerState == PlayerState.recording) {
                finishRecording()
            } else {
                startRecording()
            }
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
        preparePlayer()
    }

    fun doneTapped() {
        if (playerState == PlayerState.recording) {
            finishRecording()
        } else {
            mediaRecorder.reset()
        }
        mediaPlayer.start() // so that playback works on revisit
        TransEvent.stopTapped()
        playerState = playerState.transition(TransEvent.doneTapped)
    }
}


