import re

with open('lib/core/timer_state.dart', 'r', encoding='utf-8') as f:
    timer_code = f.read()

# 1. Add keepAlivePlayer and tickPool
timer_code = timer_code.replace("late AudioPlayer _audioPlayer;", """static const int _poolSize = 2;
  final List<AudioPlayer> _tickPool = [];
  int _tickIndex = 0;
  AudioPlayer? _keepAlivePlayer;""")

# 2. Update initTts (audio focus and player init)
old_init = """    final audioContext = AudioContext(
      android: const AudioContextAndroid(
        isSpeakerphoneOn: false,
        stayAwake: true,
        contentType: AndroidContentType.speech,
        usageType: AndroidUsageType.assistanceAccessibility,
        audioFocus: AndroidAudioFocus.gainTransientMayDuck,
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
    _audioPlayer = AudioPlayer();
    _audioPlayer.setAudioContext(audioContext);

    _tts.setLanguage("id-ID"); _tts.awaitSpeakCompletion(true);
    _tts.setSpeechRate(1.25);
    _audioPlayer.setReleaseMode(ReleaseMode.stop);
    await _audioPlayer.setSourceAsset('tick.wav');"""

new_init = """    final audioContext = AudioContext(
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

    _tts.setLanguage("id-ID"); _tts.awaitSpeakCompletion(true);
    _tts.setSpeechRate(1.25);

    // Pre-load tick players
    for (int i = 0; i < _poolSize; i++) {
      final player = AudioPlayer();
      player.setReleaseMode(ReleaseMode.stop);
      await player.setSourceAsset('tick.wav');
      _tickPool.add(player);
    }"""
timer_code = timer_code.replace(old_init, new_init)

# 3. Add _startKeepAlive, _stopKeepAlive, _playTick methods
keep_alive_code = """  Future<void> _startKeepAlive() async {
    _keepAlivePlayer?.dispose();
    _keepAlivePlayer = AudioPlayer();
    _keepAlivePlayer!.setReleaseMode(ReleaseMode.loop);
    final header = Uint8List.fromList([
      0x52, 0x49, 0x46, 0x46, 0x74, 0x22, 0x00, 0x00,
      0x57, 0x41, 0x56, 0x45, 0x66, 0x6D, 0x74, 0x20,
      0x10, 0x00, 0x00, 0x00, 0x01, 0x00, 0x01, 0x00,
      0x44, 0xAC, 0x00, 0x00, 0x88, 0x58, 0x01, 0x00,
      0x02, 0x00, 0x10, 0x00, 0x64, 0x61, 0x74, 0x61,
      0x58, 0x22, 0x00, 0x00,
    ]);
    final silenceData = Uint8List(8792);
    final wavBytes = Uint8List(header.length + silenceData.length);
    wavBytes.setRange(0, header.length, header);
    wavBytes.setRange(header.length, wavBytes.length, silenceData);
    
    await _keepAlivePlayer!.setVolume(0.01);
    await _keepAlivePlayer!.setSourceBytes(wavBytes);
    await _keepAlivePlayer!.resume();
  }

  void _stopKeepAlive() {
    _keepAlivePlayer?.stop();
    _keepAlivePlayer?.dispose();
    _keepAlivePlayer = null;
  }

  void _playTick() async {
    final player = _tickPool[_tickIndex];
    _tickIndex = (_tickIndex + 1) % _poolSize;
    await player.seek(Duration.zero);
    player.resume();
  }

  void applySettings"""
timer_code = timer_code.replace("  void applySettings", keep_alive_code)

# 4. Fix startMetronome
old_start = """    int millis = (tickIntervalSeconds * 1000).round();

    _timer = Timer.periodic(Duration(milliseconds: millis), (timer) {"""
new_start = """    if (_audioMetronome) {
      _startKeepAlive();
    }

    int millis = (tickIntervalSeconds * 1000).round();

    _timer = Timer.periodic(Duration(milliseconds: millis), (timer) {"""
timer_code = timer_code.replace(old_start, new_start)

timer_code = timer_code.replace("""      if (_audioMetronome) {
        _audioPlayer.seek(Duration.zero);
        _audioPlayer.resume();
      }""", """      if (_audioMetronome) {
        _playTick();
      }""")

# 5. Fix stopMetronome
timer_code = timer_code.replace("""  void stopMetronome() {
    _timer?.cancel();
    _isRunning = false;
    notifyListeners();
  }""", """  void stopMetronome() {
    _timer?.cancel();
    _isRunning = false;
    _stopKeepAlive();
    for (final player in _tickPool) {
      player.stop();
    }
    notifyListeners();
  }""")

# 6. Fix playBell audio context focus
old_bell = """        audioFocus: AndroidAudioFocus.gainTransientMayDuck,"""
new_bell = """        audioFocus: AndroidAudioFocus.none,"""
timer_code = timer_code.replace(old_bell, new_bell)

# 7. Fix dispose
timer_code = timer_code.replace("""  void dispose() {
    _timer?.cancel();
    _audioPlayer.dispose();
    _tts.stop();
    super.dispose();
  }""", """  void dispose() {
    _timer?.cancel();
    _stopKeepAlive();
    for (final player in _tickPool) {
      player.dispose();
    }
    _tts.stop();
    super.dispose();
  }""")

# Add dart:typed_data if missing
if "import 'dart:typed_data';" not in timer_code:
    timer_code = timer_code.replace("import 'dart:async';", "import 'dart:async';\nimport 'dart:typed_data';")


with open('lib/core/timer_state.dart', 'w', encoding='utf-8') as f:
    f.write(timer_code)

print("Restored tick pool and low latency keep-alive!")
