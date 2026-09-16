import re

with open('lib/screens/settings_screen.dart', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
skip = False

for line in lines:
    if "ListTile(" in line and "tts_speed" in line:
        skip = True
        new_lines.append("          if (settings.audioOutputMode == 'tts') ...[\n")
        new_lines.append("""            ListTile(
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
              title: Text(lang == 'en' ? 'TTS Volume' : 'Volume Suara (TTS)', style: const TextStyle(fontSize: 18)),
              subtitle: Slider(
                value: settings.ttsVolume,
                min: 0.0,
                max: 1.0,
                divisions: 10,
                label: (settings.ttsVolume * 100).toInt().toString() + '%',
                onChanged: (val) {
                  settings.setTtsVolume(val);
                },
                onChangeEnd: (val) {
                  _syncAudioSettings();
                  audio.speak(lang == 'en' ? 'Volume set to ${(val * 100).toInt()} percent' : 'Volume suara diubah ke ${(val * 100).toInt()} persen');
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
                      audio.previewVoice(lang == 'en' ? 'This is a sample voice.' : 'Ini adalah contoh suara dari pengaturan saat ini.');
                    },
                  ),
                  const SizedBox(width: 8),
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
                        currentValue: settings.ttsVoiceName ?? '',
                        onChanged: (val) {
                          final selected = audio.availableVoices.firstWhere((v) => v['name'] == val);
                          settings.setTtsVoice(selected['name'], selected['locale']);
                          _syncAudioSettings();
                          audio.speak(AppStrings.str(lang, 'tts_voice_changed'));
                        },
                      );
                    },
                    child: Text(settings.ttsVoiceName ?? AppStrings.str(lang, 'tts_voice_default')),
                  ),
                ],
              ),
            ),
          ],
""")
        continue
    
    if skip:
        # We need to stop skipping after we pass the old tts_voice ListTile
        # Which ends with `child: Text(settings.ttsVoiceName ?? AppStrings.str(lang, 'tts_voice_default')),`
        if "child: Text(settings.ttsVoiceName" in line:
            # We skip this line and the next 2 lines (`),`, `),`)
            pass
        elif "if (settings.audioOutputMode == 'tts')" in line:
            # skip it
            pass
        elif "            )," in line and "            )," in lines[lines.index(line)-1]:
            # This is a bit risky but we know the structure.
            skip = False
        continue
    
    new_lines.append(line)

with open('lib/screens/settings_screen.dart', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
print("State machine replacement done.")
