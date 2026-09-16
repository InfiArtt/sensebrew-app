import re

with open('lib/screens/settings_screen.dart', 'r', encoding='utf-8') as f:
    text = f.read()

# I will find the start of the first ListTile (tts_speed) and the end of the last ListTile (tts_voice)
start_marker = "          ListTile(\n            title: Text(AppStrings.str(lang, 'tts_speed')"
end_marker = "child: Text(settings.ttsVoiceName.isEmpty ? AppStrings.str(lang, 'default') : (settings.ttsVoiceName.length > 10 ? settings.ttsVoiceName.substring(0,10)+'...' : settings.ttsVoiceName)),\n              ),\n            ),"

if start_marker in text and end_marker in text:
    start_idx = text.find(start_marker)
    end_idx = text.find(end_marker) + len(end_marker)
    
    good_ui = """          if (settings.audioOutputMode == 'tts') ...[
            ListTile(
              title: Text(lang == 'en' ? 'Voice Volume' : 'Volume Suara (TTS)', style: const TextStyle(fontSize: 18)),
              subtitle: Slider(
                value: settings.ttsVolume,
                min: 0.0,
                max: 1.0,
                divisions: 10,
                label: "${(settings.ttsVolume * 100).toInt()}%",
                onChanged: (val) {
                  settings.setTtsVolume(val);
                },
                onChangeEnd: (val) {
                  _syncAudioSettings();
                  audio.speak(AppStrings.str(lang, 'tts_speed_changed', [(val * 100).toInt().toString()]));
                },
              ),
            ),
            ListTile(
              title: Text(AppStrings.str(lang, 'tts_speed'), style: const TextStyle(fontSize: 18)),
              subtitle: Slider(
                value: settings.ttsSpeed,
                min: 0.5,
                max: 2.0,
                divisions: 6,
                label: settings.ttsSpeed.toStringAsFixed(2),
                onChanged: (val) {
                  settings.setTtsSpeed(val);
                },
                onChangeEnd: (val) {
                  _syncAudioSettings();
                  audio.speak(AppStrings.str(lang, 'tts_speed_changed', [val.toStringAsFixed(2)]));
                },
              ),
            ),
            ListTile(
              title: Text(AppStrings.str(lang, 'tts_pitch'), style: const TextStyle(fontSize: 18)),
              subtitle: Slider(
                value: settings.ttsPitch,
                min: 0.5,
                max: 2.0,
                divisions: 15,
                label: settings.ttsPitch.toStringAsFixed(1),
                onChanged: (val) {
                  settings.setTtsPitch(val);
                },
                onChangeEnd: (val) {
                  _syncAudioSettings();
                  audio.speak(AppStrings.str(lang, 'tts_pitch_changed'));
                },
              ),
            ),
            ListTile(
              title: Text(AppStrings.str(lang, 'tts_voice'), style: const TextStyle(fontSize: 18)),
              subtitle: Text(AppStrings.str(lang, 'tts_voice_desc')),
              trailing: Row(
                mainAxisSize: MainAxisSize.min,
                children: [
                  IconButton(
                    icon: const Icon(Icons.play_circle_fill, color: Colors.blue, size: 36),
                    tooltip: lang == 'en' ? 'Preview Voice' : 'Coba Dengarkan Suara',
                    onPressed: () {
                      audio.previewVoice(lang == 'en' ? 'This is a sample of the current voice settings.' : 'Ini adalah contoh suara dari pengaturan saat ini.');
                    },
                  ),
                  ElevatedButton(
                    onPressed: () {
                      final options = audio.availableVoices
                          .where((v) => v['locale']?.startsWith(settings.appLanguage) ?? false)
                          .map((v) => {
                                'value': v['name'] ?? '',
                                'label': v['name'] ?? '',
                              })
                          .toList();
                      
                      _showSelectionBottomSheet(
                        title: AppStrings.str(lang, 'tts_voice'),
                        options: options,
                        currentValue: settings.ttsVoiceName,
                        onChanged: (val) {
                          final selectedVoice = audio.availableVoices.firstWhere((v) => v['name'] == val);
                          settings.setTtsVoice(val, selectedVoice['locale'] ?? '');
                          _syncAudioSettings();
                          audio.speak(AppStrings.str(lang, 'tts_voice_changed'));
                        },
                      );
                    },
                    child: Text(settings.ttsVoiceName.isEmpty ? AppStrings.str(lang, 'default') : (settings.ttsVoiceName.length > 10 ? settings.ttsVoiceName.substring(0,10)+'...' : settings.ttsVoiceName)),
                  ),
                ],
              ),
            ),
          ],"""
    
    new_text = text[:start_idx] + good_ui + text[end_idx:]
    with open('lib/screens/settings_screen.dart', 'w', encoding='utf-8') as f:
        f.write(new_text)
    print("Successfully replaced UI chunk via indices.")
else:
    print("Could not find start or end markers.")
