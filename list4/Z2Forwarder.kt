import java.net.*
import java.util.*

internal class Z2Forwarder(myPort: Int, private val destinationPort: Int) {

    private val localHost: InetAddress = InetAddress.getByName(null)

    private val socket = DatagramSocket(myPort)

    data class Segment(var packet: DatagramPacket? = null, var delay: Long = 0L)

    private val buffer = List(capacity) { Segment() }

    private val receiver = Receiver()
    private val sender = Sender()

    private val random = Random()

    internal inner class Receiver : Thread() {

        fun addToBuffer(packet: DatagramPacket) {
            if (random.nextDouble() > reliability)
                return

            synchronized(buffer) {
                buffer.firstOrNull { it.packet == null }?.let { segment ->
                    segment.delay = minDelay + (random.nextDouble() * (maxDelay - minDelay)).toInt()
                    segment.packet = packet
                }
            }
        }


        override fun run() {
            while (true) {
                val packet = DatagramPacket(ByteArray(datagramSize), datagramSize)
                socket.receive(packet)
                addToBuffer(packet)
                while (random.nextDouble() < duplicateProbability)
                    addToBuffer(packet)
            }
        }

    }

    internal inner class Sender : Thread() {

        fun checkBuffer() {
            synchronized(buffer) {
                buffer.filter { it.packet != null }.forEach {
                    it.delay -= sleepTime
                    if (it.delay <= 0) {
                        it.packet!!.let { packet ->
                            packet.port = destinationPort
                            socket.send(packet)
                        }
                        it.packet = null
                    }
                }
            }
        }


        override fun run() {
            try {
                while (true) {
                    checkBuffer()
                    Thread.sleep(sleepTime)
                }
            } catch (e: Exception) {
                println("Forwader.Sender.run: $e")
            }

        }

    }

    fun start() {
        sender.start()
        receiver.start()
    }

    companion object {
        private val datagramSize = 50

        private val capacity = 1000
        private val minDelay = 2000L
        private val maxDelay = 10000L
        private val sleepTime = 40L

        private val reliability = 0.80
        private val duplicateProbability = 0.1


        @Throws(Exception::class)
        @JvmStatic
        fun main(args: Array<String>) {
            val forwarder = Z2Forwarder(Integer.parseInt(args[0]), Integer.parseInt(args[1])).apply {
                start()
            }
        }
    }


}

