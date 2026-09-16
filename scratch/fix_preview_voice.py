import re

with open('lib/core/timer_state.dart', 'r', encoding='utf-8') as f:
    text = f.read()

bad_preview = """  Future<void> previewVoice(String text) async {
    if (_audioOutputMode == 'screen_reader') return;
    await _tts.speak(text);
  }"""
good_preview = """  Future<void> previewVoice(String text, {String? tempVoiceName, String? tempVoiceLocale}) async {
    if (_audioOutputMode == 'screen_reader') return;
    if (tempVoiceName != null && tempVoiceLocale != null) {
      await _tts.setVoice({"name": tempVoiceName, "locale": tempVoiceLocale});
    }
    await _tts.speak(text);
  }"""

if bad_preview in text:
    text = text.replace(bad_preview, good_preview)
    with open('lib/core/timer_state.dart', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Updated previewVoice in timer_state.dart")
else:
    print("Could not find previewVoice in timer_state.dart")
