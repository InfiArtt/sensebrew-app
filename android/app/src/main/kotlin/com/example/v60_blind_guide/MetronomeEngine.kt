package com.example.v60_blind_guide

import android.content.Context
import android.media.AudioAttributes
import android.media.AudioFormat
import android.media.AudioTimestamp
import android.media.AudioTrack
import android.os.Handler
import android.os.Looper
import io.flutter.FlutterInjector
import io.flutter.plugin.common.EventChannel
import java.io.InputStream
import java.nio.ByteBuffer
import java.nio.ByteOrder

class MetronomeEngine(private val context: Context, private val tickEventChannel: EventChannel) {
    private var audioTrack: AudioTrack? = null
    private var playThread: Thread? = null
    
    @Volatile private var isRunning = false
    @Volatile private var bpm = 60
    
    private var tickPcmData: ShortArray = ShortArray(0)
    private var silenceChunk: ShortArray = ShortArray(8000)
    private var eventSink: EventChannel.EventSink? = null
    private val mainHandler = Handler(Looper.getMainLooper())
    
    companion object {
        private const val SAMPLE_RATE = 44100
    }

    init {
        tickEventChannel.setStreamHandler(object : EventChannel.StreamHandler {
            override fun onListen(arguments: Any?, events: EventChannel.EventSink?) {
                eventSink = events
            }
            override fun onCancel(arguments: Any?) {
                eventSink = null
            }
        })
        loadTickSound()
    }
    
    private fun loadTickSound() {
        try {
            val loader = FlutterInjector.instance().flutterLoader()
            val assetPath = loader.getLookupKeyForAsset("assets/tick.wav")
            val inputStream = context.assets.open(assetPath)
            tickPcmData = readWavPcmData(inputStream)
            inputStream.close()
        } catch (e: Exception) {
            e.printStackTrace()
            // Fallback to empty if load fails
            tickPcmData = ShortArray(0)
        }
    }
    
    private fun readWavPcmData(inputStream: InputStream): ShortArray {
        val bytes = inputStream.readBytes()
        
        // Find "data" chunk
        val dataMarker = "data".toByteArray(Charsets.US_ASCII)
        var dataIndex = -1
        for (i in 0 until bytes.size - 4) {
            if (bytes[i] == dataMarker[0] && bytes[i+1] == dataMarker[1] && bytes[i+2] == dataMarker[2] && bytes[i+3] == dataMarker[3]) {
                dataIndex = i
                break
            }
        }
        
        val startOfData = if (dataIndex != -1) dataIndex + 8 else 44
        
        // Make sure we don't go out of bounds
        val actualStart = minOf(startOfData, bytes.size)
        val pcmBytes = bytes.copyOfRange(actualStart, bytes.size)
        
        val shorts = ShortArray(pcmBytes.size / 2)
        ByteBuffer.wrap(pcmBytes).order(ByteOrder.LITTLE_ENDIAN).asShortBuffer().get(shorts)
        return shorts
    }
    
    fun setBpm(newBpm: Int) {
        this.bpm = newBpm
    }
    
    fun start(startBpm: Int) {
        if (isRunning) return
        this.bpm = startBpm
        isRunning = true
        
        val minBufferSize = AudioTrack.getMinBufferSize(
            SAMPLE_RATE,
            AudioFormat.CHANNEL_OUT_MONO,
            AudioFormat.ENCODING_PCM_16BIT
        )
        
        audioTrack = AudioTrack.Builder()
            .setAudioAttributes(AudioAttributes.Builder()
                .setUsage(AudioAttributes.USAGE_MEDIA)
                .setContentType(AudioAttributes.CONTENT_TYPE_MUSIC)
                .build())
            .setAudioFormat(AudioFormat.Builder()
                .setEncoding(AudioFormat.ENCODING_PCM_16BIT)
                .setSampleRate(SAMPLE_RATE)
                .setChannelMask(AudioFormat.CHANNEL_OUT_MONO)
                .build())
            .setBufferSizeInBytes(minBufferSize * 4) // Ensure enough buffer
            .setTransferMode(AudioTrack.MODE_STREAM)
            .build()
            
        audioTrack?.play()
        
        playThread = Thread {
            var tickCount = 0
            var totalFramesWritten = 0L
            
            // Dart's Timer.periodic fires its first tick AFTER the interval has elapsed.
            // To perfectly mimic this, we write one full period of silence before the main loop.
            val initialPeriodSize = (SAMPLE_RATE * 60) / bpm
            var initialSilenceWritten = 0
            while (initialSilenceWritten < initialPeriodSize && isRunning) {
                val remaining = initialPeriodSize - initialSilenceWritten
                val silenceToWrite = minOf(silenceChunk.size, remaining)
                val written = writeAudio(silenceChunk, silenceToWrite)
                initialSilenceWritten += written
            }
            totalFramesWritten += initialSilenceWritten
            
            while (isRunning) {
                // Calculate current period size based on BPM
                val currentBpm = bpm
                val periodSize = (SAMPLE_RATE * 60) / currentBpm
                
                var framesWrittenInPeriod = 0
                
                // 1. Write the tick sound
                val tickFramesToWrite = minOf(tickPcmData.size, periodSize)
                if (tickFramesToWrite > 0) {
                    val written = writeAudio(tickPcmData, tickFramesToWrite)
                    framesWrittenInPeriod += written
                }
                
                // Schedule the UI notification for exact presentation time
                scheduleTickNotification(tickCount + 1, totalFramesWritten)
                
                // 2. Fill the rest of the period with silence in chunks
                // This allows us to re-evaluate BPM if it changes mid-beat,
                // but for V60 app, it's usually always 60 BPM anyway.
                while (framesWrittenInPeriod < periodSize && isRunning) {
                    val remaining = periodSize - framesWrittenInPeriod
                    val silenceToWrite = minOf(silenceChunk.size, remaining)
                    val written = writeAudio(silenceChunk, silenceToWrite)
                    framesWrittenInPeriod += written
                }
                
                totalFramesWritten += framesWrittenInPeriod
                tickCount++
            }
            
            audioTrack?.stop()
            audioTrack?.release()
            audioTrack = null
        }
        playThread?.priority = Thread.MAX_PRIORITY
        playThread?.start()
    }
    
    fun stop() {
        isRunning = false
        playThread?.interrupt()
        playThread?.join(500)
        playThread = null
    }
    
    private fun writeAudio(data: ShortArray, size: Int): Int {
        if (!isRunning) return 0
        val result = audioTrack?.write(data, 0, size, AudioTrack.WRITE_BLOCKING) ?: 0
        return if (result < 0) 0 else result
    }
    
    private fun scheduleTickNotification(tick: Int, totalFramesWritten: Long) {
        val track = audioTrack ?: return
        val audioTimestamp = AudioTimestamp()
        var delayMillis = 0L
        
        if (track.getTimestamp(audioTimestamp)) {
            val nanosPerFrame = 1_000_000_000L / SAMPLE_RATE
            val timestampAgeNanos = System.nanoTime() - audioTimestamp.nanoTime
            val framesAheadOfTimestamp = totalFramesWritten - audioTimestamp.framePosition
            val delayNanos = (framesAheadOfTimestamp * nanosPerFrame) - timestampAgeNanos
            if (delayNanos > 0) {
                delayMillis = delayNanos / 1_000_000L
            }
        }
        
        if (delayMillis > 150L) {
            delayMillis -= 150L // Offset by 150ms to compensate for TTS synthesis latency!
        } else {
            delayMillis = 0L
        }
        
        if (delayMillis <= 0) {
            mainHandler.post { eventSink?.success(tick) }
        } else {
            mainHandler.postDelayed({ eventSink?.success(tick) }, delayMillis)
        }
    }
}
