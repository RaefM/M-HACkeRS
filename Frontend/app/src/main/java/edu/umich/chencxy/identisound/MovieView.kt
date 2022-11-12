package edu.umich.chencxy.identisound

import android.content.Context
import android.util.Base64
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
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.LayoutDirection
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.navigation.NavHostController
import edu.umich.chencxy.identisound.SongStore.movies
import edu.umich.chencxy.identisound.SongStore.songs

/*
    TO DO:
    1) Get MovieView working with dummy constants *DONE*
    2) Query backend with dummy song name and use results to populate the movie view
        - the movie list is currently stored in SongStore.kt's _movies *DONE*
    3) Get ShazamKit working and integrate the song name it returns instead of the dummy song name
 */

@Composable
fun MovieView(context: Context, navController: NavHostController) {
    val songname = songs[songs.size-1].Songname.toString()
    val songmovie = movies[movies.size-1].Movie_name.toString()
//    val songmovie by rememberSaveable { mutableStateOf(context.getString(R.string.movie)) }
//    var enableSend by rememberSaveable { mutableStateOf(true) }

    Scaffold(
        // put the topBar here
    ) {
        Column(
            verticalArrangement = Arrangement.SpaceAround,
            modifier = Modifier.padding(it.calculateStartPadding(LayoutDirection.Ltr)+8.dp,
                it.calculateTopPadding(),
                it.calculateEndPadding(LayoutDirection.Ltr)+8.dp,
                it.calculateBottomPadding())
        ) {
            Text(songname, Modifier.padding(0.dp, 30.dp, 0.dp, 0.dp)
                .fillMaxWidth(1f), textAlign=TextAlign.Center, fontSize = 20.sp)
            Text(songmovie, Modifier.padding(0.dp, 60.dp, 0.dp, 0.dp)
                .fillMaxWidth(1f), textAlign=TextAlign.Center, fontSize = 20.sp)
//            TextField(
//                value = songmovie,
//                modifier = Modifier.padding(8.dp, 20.dp, 8.dp, 0.dp).fillMaxWidth(1f),
//                textStyle = TextStyle(fontSize = 17.sp),
//                colors = TextFieldDefaults.textFieldColors(backgroundColor=Color(0xffffffff))
//            )
        }
    }
}