import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

import 'dart:ui' as ui;

class SettingsState extends ChangeNotifier {
  String _geminiApiKey = 'AIzaSyAfhSwpVzfD4DPQBGn2CkouqMCgLNhg7sI';
  String _appLanguage = 'id'; // UI and TTS language ('id' or 'en')
  double _ttsSpeed = 1.25;
  double _ttsPitch = 1.0;
  double _ttsVolume = 1.0;
  String? _ttsVoiceName;
  String? _ttsVoiceLocale;
  bool _isTtsEnabled = true;
  String _audioOutputMode = 'tts';
  bool _visualMetronome = true;
  bool _hapticMetronome = true;
  bool _audioMetronome = true;
  String _groqApiKey = '';
  String _aiProvider = 'gemini'; // 'gemini' or 'groq'
  double _calibrationOffset = 0.0;

  String get appLanguage => _appLanguage;
  String get geminiApiKey => _geminiApiKey;
  String get groqApiKey => _groqApiKey;
  String get aiProvider => _aiProvider;
  double get calibrationOffset => _calibrationOffset;
  double get ttsSpeed => _ttsSpeed;
  double get ttsPitch => _ttsPitch;
  double get ttsVolume => _ttsVolume;
  String? get ttsVoiceName => _ttsVoiceName;
  String? get ttsVoiceLocale => _ttsVoiceLocale;
  bool get isTtsEnabled => _isTtsEnabled;
  String get audioOutputMode => _audioOutputMode;
  bool get visualMetronome => _visualMetronome;
  bool get hapticMetronome => _hapticMetronome;
  bool get audioMetronome => _audioMetronome;

  SettingsState() {
    _loadSettings();
  }

  Future<void> _loadSettings() async {
    final prefs = await SharedPreferences.getInstance();
    
    // Auto-detect system language
    String systemLang = ui.PlatformDispatcher.instance.locale.toLanguageTag();
    if (!systemLang.contains('-')) {
      if (systemLang.startsWith('id')) systemLang = 'id-ID';
      if (systemLang.startsWith('en')) systemLang = 'en-US';
    }

    String savedKey = prefs.getString('gemini_api_key') ?? '';
    _geminiApiKey = savedKey.isEmpty ? 'AIzaSyAfhSwpVzfD4DPQBGn2CkouqMCgLNhg7sI' : savedKey;
    _groqApiKey = prefs.getString('groq_api_key') ?? '';
    _aiProvider = prefs.getString('ai_provider') ?? 'gemini';
    _appLanguage = prefs.getString('app_language') ?? (systemLang.startsWith('en') ? 'en' : 'id');
    _ttsSpeed = prefs.getDouble('tts_speed') ?? 1.25;
    _ttsPitch = prefs.getDouble('tts_pitch') ?? 1.0;
    _ttsVoiceName = prefs.getString('tts_voice_name');
    _ttsVoiceLocale = prefs.getString('tts_voice_locale');
    _isTtsEnabled = prefs.getBool('is_tts_enabled') ?? true;
    _audioOutputMode = prefs.getString('audio_output_mode') ?? 'tts';
    _visualMetronome = prefs.getBool('visual_metronome') ?? true;
    _hapticMetronome = prefs.getBool('haptic_metronome') ?? true;
    _audioMetronome = prefs.getBool('audio_metronome') ?? true;
    notifyListeners();
  }

  Future<void> setGroqApiKey(String key) async {
    _groqApiKey = key;
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('groq_api_key', key);
    notifyListeners();
  }

  Future<void> setAiProvider(String provider) async {
    _aiProvider = provider;
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('ai_provider', provider);
    notifyListeners();
  }

  Future<void> setGeminiApiKey(String key) async {
    _geminiApiKey = key;
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('gemini_api_key', key);
    notifyListeners();
  }

  Future<void> setAppLanguage(String lang) async {
    _appLanguage = lang;
    _ttsVoiceName = null;
    _ttsVoiceLocale = null;
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('app_language', lang);
    await prefs.remove('tts_voice_name');
    await prefs.remove('tts_voice_locale');
    notifyListeners();
  }

  Future<void> setTtsSpeed(double speed) async {
    _ttsSpeed = speed;
    final prefs = await SharedPreferences.getInstance();
    await prefs.setDouble('tts_speed', speed);
    notifyListeners();
  }

  
  Future<void> setTtsVolume(double vol) async {
    _ttsVolume = vol;
    final prefs = await SharedPreferences.getInstance();
    await prefs.setDouble('ttsVolume', vol);
    notifyListeners();
  }
  Future<void> setTtsPitch(double pitch) async {
    _ttsPitch = pitch;
    final prefs = await SharedPreferences.getInstance();
    await prefs.setDouble('tts_pitch', pitch);
    notifyListeners();
  }

  Future<void> setTtsVoice(String name, String locale) async {
    _ttsVoiceName = name;
    _ttsVoiceLocale = locale;
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('tts_voice_name', name);
    await prefs.setString('tts_voice_locale', locale);
    notifyListeners();
  }

  Future<void> setTtsEnabled(bool enabled) async {
    _isTtsEnabled = enabled;
    final prefs = await SharedPreferences.getInstance();
    await prefs.setBool('is_tts_enabled', enabled);
    notifyListeners();
  }

  Future<void> setAudioOutputMode(String mode) async {
    _audioOutputMode = mode;
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('audio_output_mode', mode);
    notifyListeners();
  }

  Future<void> setVisualMetronome(bool enabled) async {
    _visualMetronome = enabled;
    final prefs = await SharedPreferences.getInstance();
    await prefs.setBool('visual_metronome', enabled);
    notifyListeners();
  }

  Future<void> setHapticMetronome(bool enabled) async {
    _hapticMetronome = enabled;
    final prefs = await SharedPreferences.getInstance();
    await prefs.setBool('haptic_metronome', enabled);
    notifyListeners();
  }

  Future<void> setAudioMetronome(bool enabled) async {
    _audioMetronome = enabled;
    final prefs = await SharedPreferences.getInstance();
    await prefs.setBool('audio_metronome', enabled);
    notifyListeners();
  }
}
