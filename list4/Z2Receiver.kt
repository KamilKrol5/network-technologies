import java.net.*
import java.util.*

internal class Z2Receiver(myPort: Int, private val callbackPort: Int, private val silent: Boolean = false) {
    private val localHost: InetAddress = InetAddress.getByName(null)
    private val socket: DatagramSocket = DatagramSocket(myPort)

    private val receiver = ReceiverThread()

    private val windowSize = 10
    private var next = 0

    internal inner class ReceiverThread : Thread() {

        override fun run() {
            val buffer = arrayOfNulls<Z2Packet>(windowSize)
            while (true) {
                val data = ByteArray(datagramSize)
                val packet = DatagramPacket(data, datagramSize)
                socket.receive(packet)
                val p = Z2Packet(packet.data)
                if (p.sequenceNumber < next + windowSize && p.sequenceNumber >= next) {
                    buffer[(p.sequenceNumber) % windowSize] = Z2Packet(p.data.copyOf())
                    if (!silent)
                        System.err.println("Added to buffer(${p.sequenceNumber}): ${p.value.toChar()}")
                    while (buffer[next % windowSize] != null) {
                        val pp = buffer[next % windowSize]
                        if (!silent)
                            println("Received(number=${pp!!.sequenceNumber}): ${pp.value.toChar()}")
                        buffer[next % windowSize] = null
                        next++
                    }
                }
                    p.sequenceNumber = next
                    packet.address = localHost
                    packet.port = if (callbackPort != 0) callbackPort else packet.port
                    socket.send(packet)

            }

        }

    }

    fun start() {
        receiver.start()
    }

    companion object {
        private val datagramSize = 50

        @JvmStatic
        fun main(args: Array<String>) {
//            var basePort = 0
//            var callbackPort = 0
//            if (args.size == 0) {
//                Scanner(System.`in`).apply {
//                    basePort = nextInt()
//                    callbackPort = nextInt()
//                }
//            } else {
//                basePort = Integer.parseInt(args[0])
//                callbackPort = if (args.size > 1) Integer.parseInt(args[1]) else 0
//            }
//            val receiver = Z2Receiver(basePort, callbackPort).apply {
//                start()
//            }
            val receiver = Z2Receiver(Integer.parseInt(args[0]),
                Integer.parseInt(args[1])).apply { start() }
        }
    }


}
