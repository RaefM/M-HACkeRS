package edu.umich.chencxy.identisound

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.material.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

@Composable
fun MovieListRow(index: Int, movie: Movie) {
    Column(
        modifier = Modifier.padding(8.dp, 0.dp, 8.dp, 0.dp)
            .background(color = Color(if (index % 2 == 0) 0xFFE0E0E0 else 0xFFEEEEEE))
    ) {
        Row(
            horizontalArrangement = Arrangement.SpaceBetween,
            modifier = Modifier.fillMaxWidth(1f)
        ) {
            movie.Movie_name?.let {
                Text(
                    it,
                    fontSize = 14.sp,
                    textAlign = TextAlign.End,
                    modifier = Modifier.padding(4.dp, 8.dp, 4.dp, 0.dp)
                )
            }
            movie.Director?.let {
                Text(
                    it,
                    fontSize = 17.sp,
                    modifier = Modifier.padding(4.dp, 8.dp, 4.dp, 0.dp)
                )
            }

            movie.Year?.let {
                Text(
                    it,
                    fontSize = 14.sp,
                    textAlign = TextAlign.End,
                    modifier = Modifier.padding(4.dp, 8.dp, 4.dp, 0.dp)
                )
            }

            //chatt.message?.let { Text(it, fontSize = 17.sp, modifier = Modifier.padding(4.dp, 10.dp, 4.dp, 10.dp)) }
        }
    }
}

//class Movie(var Movie_name: String? = null,
//            Director: String? = null,
//            Year: Int? = null,
//            Timestamp: String? = null
//)