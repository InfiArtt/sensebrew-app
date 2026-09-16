import re

with open('lib/screens/settings_screen.dart', 'r', encoding='utf-8') as f:
    text = f.read()

start_marker = "if (settings.audioOutputMode == 'tts') ...["
idx = text.find(start_marker)

if idx != -1:
    good_end = """if (settings.audioOutputMode == 'tts') ...[
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
                    child: ConstrainedBox(
                      constraints: const BoxConstraints(maxWidth: 100),
                      child: Text(
                        settings.ttsVoiceName.isEmpty ? AppStrings.str(lang, 'default') : settings.ttsVoiceName,
                        overflow: TextOverflow.ellipsis,
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ],
          const SizedBox(height: 32),
          const Divider(),
          const SizedBox(height: 16),
          ListTile(
            title: const Text('Restore Default Recipes', style: TextStyle(fontSize: 18, color: Colors.red)),
            subtitle: const Text('Kembalikan resep bawaan yang terhapus'),
            trailing: const Icon(Icons.restore, color: Colors.red),
            onTap: () async {
              final repo = Provider.of<RecipeRepository>(context, listen: false);
              await repo.restoreDefaults();
              if (mounted) {
                ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(content: Text('Resep bawaan berhasil dikembalikan!')),
                );
              }
            },
          ),
          const SizedBox(height: 32),
        ],
      ),
    );
  }
}
"""
    new_text = text[:idx] + good_end
    with open('lib/screens/settings_screen.dart', 'w', encoding='utf-8') as f:
        f.write(new_text)
    print("Replaced the end of the file!")
else:
    print("Could not find start_marker.")
