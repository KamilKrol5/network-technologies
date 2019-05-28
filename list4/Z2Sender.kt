import java.net.*
import java.util.concurrent.ArrayBlockingQueue
import kotlin.concurrent.thread
import kotlin.math.min

internal class Z2Sender(myPort: Int, private val destinationPort: Int, private val silent: Boolean = false) {

    private val localHost: InetAddress = InetAddress.getByName(null)
    private val socket = DatagramSocket(myPort)
    private val sender = SenderThread()
    private val receiver = ReceiverThread()

    private val windowSize = 7
    private var lastNotConfirmed = 0
    private var next = 0

    private val confirmationsQueue = ArrayBlockingQueue<Z2Packet>(2 * windowSize)

    private var retransmissionDelay = 2000L
    private val maxRetransmissionDelay = 5000L
    private var retransmissionTimer: Long? = null
    private val retransmissionQueue = ArrayBlockingQueue<Z2Packet>(2 * windowSize)

    private var retransmissionCount = 0

    private fun packetToDatagram(packet: Z2Packet): DatagramPacket =
        DatagramPacket(packet.data, packet.data.size, localHost, destinationPort)

    private fun send(packet: Z2Packet, prefix: String) {
        if (!silent)
            println("${prefix}Sent(number=${packet.sequenceNumber}): ${packet.value.toChar()}")
        socket.send(packetToDatagram(packet))
    }

    internal inner class SenderThread : Thread() {
//        var x = true
        override fun run() {
            val inputQueue = ArrayBlockingQueue<Byte>(40)
            thread (start = true) {
                generateSequence {
                    System.`in`.read().let { if (it < 0) null else it }
                }.forEach {
                    if (it.toChar() != '\n')
                        inputQueue.put(it.toByte())
                }
            }

            while (!interrupted()) {
                generateSequence { confirmationsQueue.poll() }.forEach { confirmation ->
                    if (confirmation.sequenceNumber > lastNotConfirmed) {
                        lastNotConfirmed = confirmation.sequenceNumber
                        retransmissionTimer = retransmissionDelay
                    }
                }
                while (retransmissionQueue.peek()?.let { it.sequenceNumber < lastNotConfirmed } == true) {
                    retransmissionQueue.remove()
                }
                if (retransmissionQueue.isEmpty()) {
                    retransmissionTimer = null
//                    if (x) {
//                        println("(window size = $windowSize, retransmissions: $retransmissionCount)\n")
//                     x = false
//                    }
                }
                else {
                    retransmissionTimer = retransmissionTimer?.let { it - sleepTime }
                }

                if (retransmissionTimer?.let { it < 0 } == true) { // wait or not
                    for (i in 1..retransmissionQueue.size) {
                        val packet = retransmissionQueue.remove()
                        send(packet,"Re")
                        retransmissionCount++
                        retransmissionQueue.add(packet)
                    }
                    retransmissionDelay = min(2 * retransmissionDelay, maxRetransmissionDelay)
                    retransmissionTimer = retransmissionDelay
                }

                if (next < lastNotConfirmed + windowSize && !inputQueue.isEmpty()) {
                    val packet = Z2Packet(4 + 1)
                    packet.sequenceNumber = next
                    next++
                    packet.value = inputQueue.take()
                    send(packet,"")
                    if (retransmissionTimer == null)
                        retransmissionTimer = retransmissionDelay
                    retransmissionQueue.add(packet)
//                    x = true
                }

                sleep(sleepTime)
            }

        }
    }


    internal inner class ReceiverThread : Thread() {

        override fun run() {
            while (!interrupted()) {
                val data = ByteArray(datagramSize)
                val packet = DatagramPacket(data, datagramSize)
                socket.receive(packet)
                val p = Z2Packet(packet.data)
                if (!silent)
                    println("Confirmed(number=${p.sequenceNumber}): ${p.value.toChar()}")
                confirmationsQueue.put(p)
            }

        }

    }

    fun start() {
        sender.start()
        receiver.start()
    }

    fun join() {
        sender.join()
//        receiver.join()
    }

    companion object {
        private val datagramSize = 50
        private val sleepTime = 200L
        val maxPacket = 50

//        data class Data(val retransmissionCount: Int, val time: Long)
//        val data = TreeMap<Int, Data>()

        @JvmStatic
        fun main(args: Array<String>) {
            Z2Sender(Integer.parseInt(args[0]), Integer.parseInt(args[1])).apply {
                start()
                join()
            }
        }
    }



}
