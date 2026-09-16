import re

# 1. Update SettingsState
with open('lib/core/settings_state.dart', 'r', encoding='utf-8') as f:
    s_text = f.read()

if "double _ttsVolume" not in s_text:
    s_text = s_text.replace("double _ttsPitch = 1.0;", "double _ttsPitch = 1.0;\n  double _ttsVolume = 1.0;")
    s_text = s_text.replace("double get ttsPitch => _ttsPitch;", "double get ttsPitch => _ttsPitch;\n  double get ttsVolume => _ttsVolume;")
    
    # In _loadSettings
    s_text = s_text.replace("_ttsPitch = prefs.getDouble('ttsPitch') ?? 1.0;", "_ttsPitch = prefs.getDouble('ttsPitch') ?? 1.0;\n    _ttsVolume = prefs.getDouble('ttsVolume') ?? 1.0;")
    
    # Add setTtsVolume
    set_vol = """
  Future<void> setTtsVolume(double vol) async {
    _ttsVolume = vol;
    final prefs = await SharedPreferences.getInstance();
    await prefs.setDouble('ttsVolume', vol);
    notifyListeners();
  }
"""
    s_text = s_text.replace("Future<void> setTtsPitch", set_vol + "  Future<void> setTtsPitch")

with open('lib/core/settings_state.dart', 'w', encoding='utf-8') as f:
    f.write(s_text)


# 2. Update TimerAudioState
with open('lib/core/timer_state.dart', 'r', encoding='utf-8') as f:
    t_text = f.read()

if "bool isEnabled, String outputMode, double pitch, String? voiceName, String? voiceLocale, bool hapticEnabled, bool audioMetronome)" in t_text:
    t_text = t_text.replace(
        "bool isEnabled, String outputMode, double pitch, String? voiceName, String? voiceLocale, bool hapticEnabled, bool audioMetronome)",
        "bool isEnabled, String outputMode, double pitch, double volume, String? voiceName, String? voiceLocale, bool hapticEnabled, bool audioMetronome)"
    )
    t_text = t_text.replace("_tts.setPitch(pitch);", "_tts.setPitch(pitch);\n    _tts.setVolume(volume);")

# Add previewVoice method if missing
if "previewVoice" not in t_text:
    preview = """
  Future<void> previewVoice(String text) async {
    if (_audioOutputMode == 'screen_reader') return;
    await _tts.speak(text);
  }
"""
    t_text = t_text.replace("Future<void> speak(String text)", preview + "  Future<void> speak(String text)")

with open('lib/core/timer_state.dart', 'w', encoding='utf-8') as f:
    f.write(t_text)

# 3. Update SettingsScreen to pass ttsVolume and hide TTS options if screen_reader
with open('lib/screens/settings_screen.dart', 'r', encoding='utf-8') as f:
    ui_text = f.read()

# First replace the applySettings call
ui_text = ui_text.replace(
    "settings.ttsPitch,\n        settings.ttsVoiceName,",
    "settings.ttsPitch,\n        settings.ttsVolume,\n        settings.ttsVoiceName,"
)

# Replace the TTS UI section
# Find the SwitchListTile for tts_enable and the RadioListTiles for output mode
old_tts_ui = """            const Divider(),
            SwitchListTile(
              title: const Text('Metronom Haptic (Getar)'),"""

# wait, I don't know exact structure. Let's just use Python script to read and replace exactly.
print("SettingsState and TimerAudioState updated.")
