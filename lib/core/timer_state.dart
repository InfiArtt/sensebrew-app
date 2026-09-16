import 'dart:async';
import 'dart:typed_data';
import 'package:flutter/foundation.dart';
import 'package:flutter/semantics.dart';
import 'package:flutter/services.dart';
import 'package:flutter_tts/flutter_tts.dart';
import 'package:audioplayers/audioplayers.dart';
import 'package:soundpool/soundpool.dart';

class TimerAudioState extends ChangeNotifier {
  final FlutterTts _tts = FlutterTts();
  
  Soundpool? _soundpool;
  int? _tickSoundId;
  int? _bellSoundId;

  AudioPlayer? _keepAlivePlayer;
  
  bool _isRunning = false;
  int _beats = 0;
  Timer? _timer;

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
    // 1. Initialize Soundpool for zero-latency tick and bell sounds
    // Use StreamType.notification to attempt piercing the Bluetooth SCO call channel
    _soundpool = Soundpool.fromOptions(options: const SoundpoolOptions(
      streamType: StreamType.notification,
      maxStreams: 4,
    ));

    // Load tick.wav into memory
    final tickData = await rootBundle.load('assets/tick.wav');
    _tickSoundId = await _soundpool!.load(tickData);

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

  Uint8List _createSilenceWav(int seconds) {
    int sampleRate = 44100;
    int channels = 1;
    int byteRate = sampleRate * channels * 2;
    int dataSize = seconds * byteRate;
    int fileSize = 36 + dataSize;

    var header = ByteData(44);
    header.setUint8(0, 0x52); header.setUint8(1, 0x49); header.setUint8(2, 0x46); header.setUint8(3, 0x46); // RIFF
    header.setUint32(4, fileSize, Endian.little);
    header.setUint8(8, 0x57); header.setUint8(9, 0x41); header.setUint8(10, 0x56); header.setUint8(11, 0x45); // WAVE
    header.setUint8(12, 0x66); header.setUint8(13, 0x6D); header.setUint8(14, 0x74); header.setUint8(15, 0x20); // fmt 
    header.setUint32(16, 16, Endian.little);
    header.setUint16(20, 1, Endian.little);
    header.setUint16(22, channels, Endian.little);
    header.setUint32(24, sampleRate, Endian.little);
    header.setUint32(28, byteRate, Endian.little);
    header.setUint16(32, channels * 2, Endian.little);
    header.setUint16(34, 16, Endian.little);
    header.setUint8(36, 0x64); header.setUint8(37, 0x61); header.setUint8(38, 0x74); header.setUint8(39, 0x61); // data
    header.setUint32(40, dataSize, Endian.little);

    final wavBytes = Uint8List(44 + dataSize);
    wavBytes.setRange(0, 44, header.buffer.asUint8List());
    return wavBytes;
  }

  Future<void> _startKeepAlive() async {
    _keepAlivePlayer?.dispose();
    _keepAlivePlayer = AudioPlayer();
    _keepAlivePlayer!.setReleaseMode(ReleaseMode.loop);
    
    // Create 10 seconds of silence to prevent platform channel event flooding
    final wavBytes = _createSilenceWav(10);
    
    await _keepAlivePlayer!.setVolume(0.01);
    await _keepAlivePlayer!.setSourceBytes(wavBytes);
    await _keepAlivePlayer!.resume();
  }

  void _stopKeepAlive() {
    _keepAlivePlayer?.stop();
    _keepAlivePlayer?.dispose();
    _keepAlivePlayer = null;
  }

  void _playTick() {
    if (_tickSoundId != null && _soundpool != null) {
      _soundpool!.play(_tickSoundId!);
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

    if (_audioMetronome) {
      _startKeepAlive();
    }

    int millis = (tickIntervalSeconds * 1000).round();

    _timer = Timer.periodic(Duration(milliseconds: millis), (timer) {
      if (!_isRunning) {
        timer.cancel();
        return;
      }
      _beats++;
      
      if (_audioMetronome) {
        _playTick();
      }
      
      if (_hapticEnabled) {
        HapticFeedback.heavyImpact();
      }
      
      if (onTick != null) {
        onTick(_beats);
      }
      notifyListeners();
    });
  }

  void stopMetronome() {
    _timer?.cancel();
    _isRunning = false;
    _stopKeepAlive();
    notifyListeners();
  }

  Future<void> playBell() async {
    if (_bellSoundId != null && _soundpool != null) {
      _soundpool!.play(_bellSoundId!);
    }
  }

  @override
  void dispose() {
    _timer?.cancel();
    _stopKeepAlive();
    _soundpool?.release();
    _soundpool?.dispose();
    _tts.stop();
    super.dispose();
  }
}
