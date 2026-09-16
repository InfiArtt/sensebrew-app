import re

with open('lib/screens/settings_screen.dart', 'r', encoding='utf-8') as f:
    text = f.read()

bad_ui = """          ListTile(
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
          if (settings.audioOutputMode == 'tts')
            ListTile(
              title: Text(AppStrings.str(lang, 'tts_voice'), style: const TextStyle(fontSize: 18)),
              subtitle: Text(AppStrings.str(lang, 'tts_voice_desc')),
              trailing: ElevatedButton(
                onPressed: () {
                  final options = audio.availableVoices
                      .where((v) => v['locale']?.startsWith(settings.appLanguage) ?? false)
                      .map((v) => {
                            'value': v['name'] ?? '',
                            'label': v['name'] ?? '',
                          })
                      .toList();
                  
                  if (options.isEmpty) {
                    ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(lang == 'en' ? 'No voice available for this language' : 'Tidak ada suara untuk bahasa ini')));
                    return;
                  }

                  _showSelectionBottomSheet(
                    title: AppStrings.str(lang, 'tts_voice'),
                    options: options,
                    currentValue: settings.ttsVoiceName,
                    onSelected: (val) {
                      final selectedVoice = audio.availableVoices.firstWhere((v) => v['name'] == val);
                      settings.setTtsVoice(val, selectedVoice['locale'] ?? '');
                      _syncAudioSettings();
                      audio.speak(AppStrings.str(lang, 'tts_voice_changed'));
                    },
                  );
                },
                child: Text(settings.ttsVoiceName.isEmpty ? AppStrings.str(lang, 'default') : (settings.ttsVoiceName.length > 10 ? settings.ttsVoiceName.substring(0,10)+'...' : settings.ttsVoiceName)),
              ),
            ),"""

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
                  audio.speak(AppStrings.str(lang, 'tts_speed_changed', [(val * 100).toInt().toString()])); // Reusing speech confirmation
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
                      
                      if (options.isEmpty) {
                        ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(lang == 'en' ? 'No voice available for this language' : 'Tidak ada suara untuk bahasa ini')));
                        return;
                      }

                      _showSelectionBottomSheet(
                        title: AppStrings.str(lang, 'tts_voice'),
                        options: options,
                        currentValue: settings.ttsVoiceName,
                        onSelected: (val) {
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

if bad_ui in text:
    text = text.replace(bad_ui, good_ui)
    with open('lib/screens/settings_screen.dart', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Fixed UI in settings_screen.dart")
else:
    print("Could not find bad_ui in settings_screen.dart")

