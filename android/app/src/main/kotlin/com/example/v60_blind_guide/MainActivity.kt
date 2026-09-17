package com.example.v60_blind_guide

import io.flutter.embedding.android.FlutterActivity
import io.flutter.embedding.engine.FlutterEngine
import io.flutter.plugin.common.EventChannel
import io.flutter.plugin.common.MethodChannel

class MainActivity: FlutterActivity() {
    private val METHOD_CHANNEL = "com.sensebrew/metronome"
    private val EVENT_CHANNEL = "com.sensebrew/metronome_tick"
    
    private var metronomeEngine: MetronomeEngine? = null

    override fun configureFlutterEngine(flutterEngine: FlutterEngine) {
        super.configureFlutterEngine(flutterEngine)

        // Register native EditText PlatformView
        flutterEngine.platformViewsController.registry
            .registerViewFactory(
                "sensebrew/native_textfield",
                NativeTextFieldFactory(flutterEngine.dartExecutor.binaryMessenger)
            )

        val eventChannel = EventChannel(flutterEngine.dartExecutor.binaryMessenger, EVENT_CHANNEL)
        metronomeEngine = MetronomeEngine(context, eventChannel)
        
        MethodChannel(flutterEngine.dartExecutor.binaryMessenger, METHOD_CHANNEL).setMethodCallHandler { call, result ->
            when (call.method) {
                "start" -> {
                    val bpm = call.argument<Int>("bpm") ?: 60
                    metronomeEngine?.start(bpm)
                    result.success(null)
                }
                "stop" -> {
                    metronomeEngine?.stop()
                    result.success(null)
                }
                "setBpm" -> {
                    val bpm = call.argument<Int>("bpm") ?: 60
                    metronomeEngine?.setBpm(bpm)
                    result.success(null)
                }
                else -> result.notImplemented()
            }
        }
    }
    
    override fun onDestroy() {
        metronomeEngine?.stop()
        super.onDestroy()
    }
}


