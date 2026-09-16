import 'package:flutter/services.dart';

class MetronomeBridge {
  static const MethodChannel _channel = MethodChannel('com.sensebrew/metronome');
  static const EventChannel _tickChannel = EventChannel('com.sensebrew/metronome_tick');
  
  static Stream<int>? _tickStream;

  static Future<void> start({int bpm = 60}) async {
    try {
      await _channel.invokeMethod('start', {'bpm': bpm});
    } on PlatformException catch (e) {
      print("Failed to start metronome: '${e.message}'.");
    }
  }

  static Future<void> stop() async {
    try {
      await _channel.invokeMethod('stop');
    } on PlatformException catch (e) {
      print("Failed to stop metronome: '${e.message}'.");
    }
  }

  static Future<void> setBpm(int bpm) async {
    try {
      await _channel.invokeMethod('setBpm', {'bpm': bpm});
    } on PlatformException catch (e) {
      print("Failed to set bpm: '${e.message}'.");
    }
  }

  static Stream<int> get tickStream {
    _tickStream ??= _tickChannel.receiveBroadcastStream().map((dynamic event) => event as int);
    return _tickStream!;
  }
}
