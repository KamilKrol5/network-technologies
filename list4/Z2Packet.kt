import java.io.ByteArrayInputStream

internal class Z2Packet {
    // PAKIET PRZESYLANY W DATAGRAMIE
    val data: ByteArray

    constructor(size: Int)
    // TWORZY PUSTY PAKIET
    {
        data = ByteArray(size)
    }

    constructor(b: ByteArray)
    // TWORZY PAKIET ZAWIERAJACY CIAG BAJTOW b
    {
        data = b
    }

    fun setIntAt(value: Int, idx: Int)
    // ZAPISUJE LICZBE CALKOWITA value JAKO 4 BAJTY OD POZYCJI idx
    {
        data[idx] = (value shr 24 and 0xFF).toByte()
        data[idx + 1] = (value shr 16 and 0xFF).toByte()
        data[idx + 2] = (value shr 8 and 0xFF).toByte()
        data[idx + 3] = (value and 0xFF).toByte()
    }

    fun getIntAt(idx: Int): Int
    // ODCZYTUJE LICZBE CALKOWITA NA 4 BAJTACH OD POZYCJI idx
    {
        var x: Int
        x = data[idx].toInt() and 0xFF shl 24
        x = x or (data[idx + 1].toInt() and 0xFF shl 16)
        x = x or (data[idx + 2].toInt() and 0xFF shl 8)
        x = x or (data[idx + 3].toInt() and 0xFF)
        return x
    }

    var sequenceNumber
        get() = getIntAt(0)
        set(value) = setIntAt(value, 0)

    var value
        get() = data[4]
        set(value) { data[4] = value }

}
