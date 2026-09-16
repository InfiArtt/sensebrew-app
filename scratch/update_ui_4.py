import re

with open('lib/screens/settings_screen.dart', 'r', encoding='utf-8') as f:
    text = f.read()

# Instead of regex, let's find the exact indices
idx_start = text.find("          ListTile(\n            title: Text(AppStrings.str(lang, 'tts_speed'), style: const TextStyle(fontSize: 18)),")
idx_end = text.find("    final timerAudio = Provider.of<TimerAudioState>(context);")

if idx_start != -1 and idx_end != -1:
    # Just to be safe, find the end of the tts_voice block
    idx_voice_end = text.find("            ),", text.find("child: Text(settings.ttsVoiceName ?? AppStrings.str(lang, 'tts_voice_default')),", idx_start)) + 14
    
    old_block = text[idx_start:idx_voice_end]
    
    new_block = """          if (settings.audioOutputMode == 'tts') ...[
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
          ],"""
    
    text = text.replace(old_block, new_block)
    with open('lib/screens/settings_screen.dart', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Replaced UI successfully.")
else:
    print("Could not find index.")
