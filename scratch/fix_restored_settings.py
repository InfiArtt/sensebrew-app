import re

with open('lib/screens/settings_screen.dart', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Remove url_launcher
text = text.replace("import 'package:url_launcher/url_launcher.dart';", "")

# 2. Fix applySettings
bad_sync = """  void _syncAudioSettings() {
    final settings = Provider.of<SettingsState>(context, listen: false);
    final audio = Provider.of<TimerAudioState>(context, listen: false);
    audio.applySettings(
      settings.audioMetronome,
      settings.isTtsEnabled,
      settings.audioOutputMode,
      settings.ttsPitch,
      settings.ttsVolume,
      settings.ttsVoiceName,
      settings.ttsVoiceLocale,
      settings.hapticMetronome,
    );
  }"""
good_sync = """  void _syncAudioSettings() {
    final settings = Provider.of<SettingsState>(context, listen: false);
    final audio = Provider.of<TimerAudioState>(context, listen: false);
    audio.applySettings(
      settings.appLanguage,
      settings.ttsSpeed,
      settings.isTtsEnabled,
      settings.audioOutputMode,
      settings.ttsPitch,
      settings.ttsVolume,
      settings.ttsVoiceName,
      settings.ttsVoiceLocale,
      settings.hapticMetronome,
      settings.audioMetronome,
    );
  }"""
text = text.replace(bad_sync, good_sync)

# 3. Fix setIsTtsEnabled
text = text.replace("settings.setIsTtsEnabled(val);", "settings.setTtsEnabled(val);")

# 4. Fix ttsVoiceName.isEmpty (it is nullable, so use ?? '')
text = text.replace("settings.ttsVoiceName.isEmpty", "(settings.ttsVoiceName ?? '').isEmpty")
text = text.replace("settings.ttsVoiceName.length > 10", "(settings.ttsVoiceName ?? '').length > 10")
text = text.replace("settings.ttsVoiceName.substring", "(settings.ttsVoiceName ?? '').substring")
text = text.replace("settings.ttsVoiceName,", "(settings.ttsVoiceName ?? ''),")

with open('lib/screens/settings_screen.dart', 'w', encoding='utf-8') as f:
    f.write(text)
print("Applied fixes to settings_screen.dart!")
