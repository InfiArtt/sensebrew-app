import 'dart:async';
import 'package:flutter/foundation.dart';
import 'package:flutter/semantics.dart';
import 'package:flutter/services.dart';
import 'package:flutter_tts/flutter_tts.dart';
import 'package:audioplayers/audioplayers.dart';
import 'package:soundpool/soundpool.dart';
import 'metronome_bridge.dart';

class TimerAudioState extends ChangeNotifier {
  final FlutterTts _tts = FlutterTts();
  
  Soundpool? _soundpool;
  int? _bellSoundId;
  
  bool _isRunning = false;
  int _beats = 0;
  
  StreamSubscription<int>? _tickSubscription;

  bool get isRunning => _isRunning;
  int get beats => _beats;

  bool _isTtsEnabled = true;
  String _audioOutputMode = 'tts';
  List<Map<String, String>> availableVoices = [];
  bool _hapticEnabled = true;
  bool _audioMetronome = true;

  TimerAudioState() {
    _initTts();
  }

  Future<void> _initTts() async {
    // 1. Initialize Soundpool for zero-latency bell sound
    _soundpool = Soundpool.fromOptions(options: const SoundpoolOptions(
      streamType: StreamType.notification,
      maxStreams: 4,
    ));

    // Load bell.wav into memory
    final bellData = await rootBundle.load('assets/bell.wav');
    _bellSoundId = await _soundpool!.load(bellData);

    // 2. Initialize KeepAlive AudioPlayer context to keep Bluetooth SCO warm
    final audioContext = AudioContext(
      android: const AudioContextAndroid(
        isSpeakerphoneOn: false,
        stayAwake: true,
        contentType: AndroidContentType.speech,
        usageType: AndroidUsageType.assistanceAccessibility,
        audioFocus: AndroidAudioFocus.none,
      ),
      iOS: AudioContextIOS(
        category: AVAudioSessionCategory.playback,
        options: const [
          AVAudioSessionOptions.mixWithOthers,
          AVAudioSessionOptions.allowBluetooth,
          AVAudioSessionOptions.allowBluetoothA2DP,
        ],
      ),
    );
    AudioPlayer.global.setAudioContext(audioContext);

    // 3. Initialize TTS
    _tts.awaitSpeakCompletion(true);
    _tts.setSpeechRate(1.25);

    final voices = await _tts.getVoices;
    if (voices != null) {
      availableVoices = (voices as List).map((v) {
        final map = v as Map;
        return {"name": map["name"].toString(), "locale": map["locale"].toString()};
      }).toList();
      notifyListeners();
    }
  }

  String _appliedLang = '';
  String? _appliedVoiceName;

  void applySettings(String appLanguage, double speed, bool isEnabled, String outputMode, double pitch, double volume, String? voiceName, String? voiceLocale, bool hapticEnabled, bool audioMetronome) {
    if (_appliedLang != appLanguage) {
      _appliedLang = appLanguage;
      if (appLanguage == 'id') {
        _tts.setLanguage('id-ID');
      } else {
        _tts.setLanguage('en-US');
      }
    }

    _tts.setSpeechRate(speed);
    _tts.setPitch(pitch);
    _tts.setVolume(volume);
    _isTtsEnabled = isEnabled;
    _audioOutputMode = outputMode;
    _hapticEnabled = hapticEnabled;
    _audioMetronome = audioMetronome;

    if (_appliedVoiceName != voiceName) {
      _appliedVoiceName = voiceName;
      if (voiceName != null && voiceLocale != null) {
        bool isMatch = false;
        if (appLanguage == 'id' && voiceLocale.toLowerCase().contains('id')) isMatch = true;
        if (appLanguage == 'en' && voiceLocale.toLowerCase().contains('en')) isMatch = true;
        
        if (isMatch) {
          _tts.setVoice({"name": voiceName, "locale": voiceLocale});
        }
      }
    }
  }

  Future<void> previewVoice(String text, {String? tempVoiceName, String? tempVoiceLocale}) async {
    if (_audioOutputMode == 'screen_reader') return;
    if (tempVoiceName != null && tempVoiceLocale != null) {
      await _tts.setVoice({"name": tempVoiceName, "locale": tempVoiceLocale});
    }
    await _tts.speak(text);
  }

  Future<void> speak(String text) async {
    if (!_isTtsEnabled) return;
    
    if (_audioOutputMode == 'screen_reader') {
      SemanticsService.announce(text, TextDirection.ltr);
    } else {
      await _tts.speak(text);
    }
  }

  void startMetronome({Function(int)? onTick, double tickIntervalSeconds = 1.0}) {
    if (_isRunning) stopMetronome();
    _isRunning = true;
    _beats = 0;
    notifyListeners();

    int bpm = (60 / tickIntervalSeconds).round();

    _tickSubscription = MetronomeBridge.tickStream.listen((beat) {
      if (!_isRunning) return;
      _beats = beat;
      
      if (_hapticEnabled) {
        HapticFeedback.heavyImpact();
      }
      
      if (onTick != null) {
        onTick(_beats);
      }
      notifyListeners();
    });

    if (_audioMetronome) {
      MetronomeBridge.start(bpm: bpm);
    } else {
      // If audio is disabled, use a silent native bridge anyway to keep accurate timing
      // or just send bpm, but wait, if we want NO audio, our native engine currently
      // has no concept of "mute". 
      // For now, if audioMetronome is false, we can start the native engine and it will play ticks.
      // Wait, we need to handle "mute". I should add mute support to the native engine or 
      // just pass a volume parameter. Actually, visual metronome relies on the tick events!
      // I will send a mute flag to the native engine or just use Dart timer if muted.
      // Since it's easiest: if audioMetronome is false, we use a fallback Dart Timer 
      // since exact audio sync isn't needed if there's no audio!
      _startFallbackTimer(bpm, onTick);
    }
  }

  Timer? _fallbackTimer;

  void _startFallbackTimer(int bpm, Function(int)? onTick) {
    int millis = (60000 / bpm).round();
    _fallbackTimer = Timer.periodic(Duration(milliseconds: millis), (timer) {
      if (!_isRunning) {
        timer.cancel();
        return;
      }
      _beats++;
      if (_hapticEnabled) HapticFeedback.heavyImpact();
      if (onTick != null) onTick(_beats);
      notifyListeners();
    });
  }

  void stopMetronome() {
    _isRunning = false;
    _tickSubscription?.cancel();
    _tickSubscription = null;
    _fallbackTimer?.cancel();
    _fallbackTimer = null;
    MetronomeBridge.stop();
    notifyListeners();
  }

  Future<void> playBell() async {
    if (_bellSoundId != null && _soundpool != null) {
      _soundpool!.play(_bellSoundId!);
    }
  }

  @override
  void dispose() {
    stopMetronome();
    _soundpool?.release();
    _soundpool?.dispose();
    _tts.stop();
    super.dispose();
  }
}
