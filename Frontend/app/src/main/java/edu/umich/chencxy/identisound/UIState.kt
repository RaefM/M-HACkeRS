package edu.umich.chencxy.identisound

class UIState {

    private var recVisible = true
    var recEnabled by mutableStateOf(true)
    var recColor by mutableStateOf(Color.Black)
    var recIcon by mutableStateOf(R.drawable.ic_baseline_play_circle_24_24) // initial value

    var stopEnabled by mutableStateOf(true)
    var stopColor by mutableStateOf(Color.DarkGray)
    var stopIcon by mutableStateOf(R.drawable.ic_stop_circle_24) // initial value

//    private fun reset() {
//
//        stopEnabled = false
//        stopColor = Color.Black
//        stopIcon = R.drawable.ic_baseline_play_circle_24 // initial value
//    }


}