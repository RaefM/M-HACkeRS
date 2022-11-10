package edu.umich.chencxy.identisound

import android.app.Application
import android.os.Bundle
import android.util.Log
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.result.contract.ActivityResultContracts
import androidx.activity.viewModels
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material.MaterialTheme
import androidx.compose.material.Surface
import androidx.compose.material.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.CompositionLocalProvider
import androidx.compose.ui.Modifier
import androidx.compose.ui.tooling.preview.Preview
import androidx.lifecycle.AndroidViewModel
import androidx.navigation.NavHost
import androidx.navigation.NavType
import androidx.navigation.compose.rememberNavController
import androidx.navigation.navArgument
import edu.umich.chencxy.identisound.ui.theme.IdentiSoundTheme
import android.Manifest
import android.content.Context
import android.widget.Toast
import androidx.compose.runtime.*
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import edu.umich.chencxy.identisound.ui.theme.toast


class MainActivity : ComponentActivity() {
    private val viewModel: MainViewModel by viewModels()
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        registerForActivityResult(ActivityResultContracts.RequestPermission())
        { granted ->
            if (!granted) {
                toast("Audio access denied")
                finish()
            }
        }.launch(Manifest.permission.RECORD_AUDIO)
        viewModel.audioPlayer?.let { audioPlayer ->
            setContent {
                CompositionLocalProvider(LocalAudioPlayer provides audioPlayer) {
                    val navController = rememberNavController()
                    NavHost(navController, startDestination = "MainView") {
                        composable("MainView") {
                            MainView(this@MainActivity, navController)
                        }
                        composable("MovieView") {
                            MovieView(this@MainActivity, navController)
                        }
                        // passing an optional, nullable argument
                        composable(
                            "AudioView?autoPlay={autoPlay}",
                            arguments = listOf(navArgument("autoPlay") {
                                type = NavType.BoolType
                                defaultValue = false
                            })
                        ) {
                          //  AudioView(navController, it.arguments?.getBoolean("autoPlay"))
                        }
                    }
                }
            }
        } ?: run {
            Log.e("MainActivity", "external cache dir null?")
            toast("Cannot create audio player!")
            finish()
        }
    }

}

class MainViewModel(app: Application): AndroidViewModel(app) {
    var audioPlayer = app.externalCacheDir?.let {
        AudioPlayer(app, "${it.absolutePath}/chatteraudio.m4a")
    }
}



@Composable
fun Greeting(name: String) {
    Text(text = "Hello $name!")
}

@Preview(showBackground = true)
@Composable
fun DefaultPreview() {
    IdentiSoundTheme {
        Greeting("Android")
    }
}