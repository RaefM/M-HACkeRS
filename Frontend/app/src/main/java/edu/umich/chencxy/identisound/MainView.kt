package edu.umich.chencxy.identisound

import android.content.Context
import android.util.Log
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.calculateEndPadding
import androidx.compose.foundation.layout.calculateStartPadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.material.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Add
import androidx.compose.runtime.*
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.unit.LayoutDirection
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.navigation.NavHostController
import com.google.accompanist.swiperefresh.SwipeRefresh
import com.google.accompanist.swiperefresh.rememberSwipeRefreshState
import edu.umich.chencxy.identisound.SongStore.songs
import edu.umich.chencxy.identisound.SongStore.getSongTitle
import androidx.activity.compose.BackHandler
import androidx.compose.foundation.layout.*
import androidx.compose.material.*
import androidx.compose.runtime.*
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.scale
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.unit.dp

val LocalPlayerUIState = compositionLocalOf { UIState() }

@Composable
fun MainView(context: Context, navController: NavHostController) {
    var isLaunching by rememberSaveable { mutableStateOf(true) }

    LaunchedEffect(Unit) {
        if (isLaunching) {
            isLaunching = false
            getSongTitle(context)
        }
    }
    Column(verticalArrangement = Arrangement.SpaceAround,
        horizontalAlignment = Alignment.CenterHorizontally,
        modifier=Modifier.fillMaxHeight(1f)) {
        Spacer(modifier = Modifier.fillMaxHeight(.05f))
        RecButton()
        Log.d("abc","we are here")
    }
}

@Composable
fun RecButton() {
    val audioPlayer = LocalAudioPlayer.current
    val playerUIState = LocalPlayerUIState.current

    Button(onClick = { audioPlayer.startRecording() },
        enabled = playerUIState.recEnabled,
        colors = ButtonDefaults.buttonColors(backgroundColor = Color.White,
            disabledBackgroundColor = Color.White),
        elevation = ButtonDefaults.elevation(0.dp)
    ) {
        Icon(painter = painterResource(playerUIState.recIcon),
            modifier= Modifier.size(100.dp),
            contentDescription = stringResource(R.string.recButton),
            tint = Color.Black
        )
    }
}