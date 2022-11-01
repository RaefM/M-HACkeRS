package edu.umich.chencxy.identisound

import kotlin.properties.ReadWriteProperty
import kotlin.reflect.KProperty

class Song(var Songname: String? = null,
            audio: String? = null) {
    var audio: String? by SongPropDelegate(audio)}

class SongPropDelegate private constructor ():
    ReadWriteProperty<Any?, String?> {
    private var _value: String? = null
        set(newValue) {
            newValue ?: run {
                field = null
                return
            }
            field = if (newValue == "null" || newValue.isEmpty()) null else newValue
        }

    constructor(initialValue: String?): this() { _value = initialValue }

    override fun getValue(thisRef: Any?, property: KProperty<*>) = _value
    override fun setValue(thisRef: Any?, property: KProperty<*>, value: String?) {
        _value = value
    }
}