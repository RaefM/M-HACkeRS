package edu.umich.chencxy.identisound

import android.content.Context
import androidx.compose.foundation.layout.size
import androidx.compose.material.Button
import androidx.compose.material.ButtonDefaults
import androidx.compose.material.Icon
import androidx.compose.material.MaterialTheme.colors
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.setValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.unit.dp
import androidx.navigation.NavController
import kotlinx.coroutines.runBlocking
import java.security.KeyStore.TrustedCertificateEntry

class UIState {

//    private var recVisible = true
    var recEnabled by mutableStateOf(true)
    var recIcon by mutableStateOf(R.drawable.ic_baseline_play_circle_24) // initial value
    var stopIcon by mutableStateOf(R.drawable.ic_baseline_stop_circle_24) // initial value

    private fun reset(){
        recEnabled = false
        recIcon = R.drawable.ic_baseline_play_circle_24
    }

    fun set_loading(){
        recIcon = R.drawable.ic_baseline_change_circle_24

    }

    fun reLoad(){
        recIcon = R.drawable.ic_baseline_play_circle_24
    }


    fun propagate(playerState: PlayerState) = when (playerState){
        is PlayerState.start -> {
            when (playerState.mode) {
                StartMode.standby -> {
                    recEnabled
//                    playEnabled(true)
//                    playCtlEnabled(false)
//                    doneEnabled(true)
                }
                StartMode.record -> {
                    // initial values already set up for record start mode.
                    reset()
                }
//                StartMode.play -> {
//                    recIcon = R.drawable.ic_baseline_play_circle_24
//                    recEnabled = true
//                }
            }
        }
        PlayerState.recording -> {
            recIcon = R.drawable.ic_baseline_stop_circle_24
            recEnabled = true
        }
    }
}

//@Composable
//fun recButton(context: Context){
//    val audioPlayer = LocalAudioPlayer.current
//    //runBlocking { audioPlayer.recTapped(context) }
//    Button(onClick = { runBlocking{audioPlayer.recTapped(context)} },
//        enabled = audioPlayer.playerUIState.recEnabled,
//        colors = ButtonDefaults.buttonColors(backgroundColor = Color.White,
//            disabledBackgroundColor = Color.White),
//        elevation = ButtonDefaults.elevation(0.dp)
//    ) {
//        Icon(painter = painterResource(audioPlayer.playerUIState.recIcon),
//            modifier= Modifier.size(100.dp),
//            contentDescription = stringResource(R.string.recButton),
////            tint = audioPlayer.playerUIState.recColor
//        )
//    }
//}