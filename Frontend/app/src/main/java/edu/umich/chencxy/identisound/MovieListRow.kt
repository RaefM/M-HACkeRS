package edu.umich.chencxy.identisound

import android.view.View
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.material.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import coil.compose.rememberImagePainter


@Composable
fun MovieListRow(index: Int, movie: Movie) {
    Column(
        modifier = Modifier.padding(8.dp, 0.dp, 8.dp, 0.dp),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Column(
            //horizontalArrangement = Arrangement.SpaceBetween,
            modifier = Modifier.fillMaxWidth(),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {

            Image(
                painter = rememberImagePainter(movie.Media_link),
                contentDescription = "My content description",
                modifier = Modifier.size(400.dp),
            )


            movie.Movie_name?.let {
                Text(
                    it+"  ("+movie.Year+')',
                    fontSize = 22.sp,
                    textAlign = TextAlign.End,
                    modifier = Modifier.padding(4.dp, 8.dp, 4.dp, 0.dp)
                )
            }


            movie.Director?.let {
                Text(
                    "          "+it,
                    fontSize = 18.sp,
                    modifier = Modifier.padding(4.dp, 8.dp, 4.dp, 0.dp).align(alignment = Alignment.End),
                    //horizontalAlignment = Alignment.End
                )
            }

            Spacer(modifier = Modifier.height(90.dp))



            //chatt.message?.let { Text(it, fontSize = 17.sp, modifier = Modifier.padding(4.dp, 10.dp, 4.dp, 10.dp)) }
        }
    }
}

//class Movie(var Movie_name: String? = null,
//            Director: String? = null,
//            Year: Int? = null,
//            Timestamp: String? = null
//)