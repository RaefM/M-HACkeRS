package edu.umich.chencxy.identisound

import android.annotation.SuppressLint
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
import androidx.compose.material.MaterialTheme.colors
import androidx.compose.runtime.*
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.scale
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import kotlinx.coroutines.GlobalScope
import kotlinx.coroutines.async
import kotlinx.coroutines.launch
import kotlinx.coroutines.runBlocking

val LocalPlayerUIState = compositionLocalOf { UIState() }

@SuppressLint("UnusedMaterialScaffoldPaddingParameter")
@Composable
fun MainView(context: Context, navController: NavHostController) {
    var isLaunching by rememberSaveable { mutableStateOf(true) }

    LaunchedEffect(Unit) {
        if (isLaunching) {
            isLaunching = false
            //getSongTitle(context)
        }
    }
    Scaffold() {

        Column(
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.Center,
            modifier = Modifier.fillMaxWidth().fillMaxHeight().background(color = Color(0xAFBBF2)),

        ) {
            Text(
                "Press To Crash the phone🥰🥰",
                fontSize = 22.sp,
                textAlign = TextAlign.End,
                modifier = Modifier.padding(4.dp, 8.dp, 4.dp, 0.dp)
            )
            RecButton(context, navController)
            Log.d("abc", "we are here")

        }
    }
}

@Composable
fun RecButton(context: Context, navController: NavHostController) {
    val audioPlayer = LocalAudioPlayer.current
    val playerUIState = LocalPlayerUIState.current
    playerUIState.reLoad()
    Button(onClick = {
        playerUIState.set_loading()
        GlobalScope.async { audioPlayer.recTapped(context,navController) }
        //Thread.sleep(11000)
        //playerUIState.set_loading()
        },
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