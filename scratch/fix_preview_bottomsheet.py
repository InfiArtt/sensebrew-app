import re

with open('lib/screens/settings_screen.dart', 'r', encoding='utf-8') as f:
    text = f.read()

bad_bottom_sheet = """  void _showSelectionBottomSheet({
    required String title,
    required List<Map<String, String>> options,
    required String currentValue,
    required Function(String) onSelected,
  }) {
    showModalBottomSheet(
      context: context,
      builder: (context) {
        return SafeArea(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Padding(
                padding: const EdgeInsets.all(16.0),
                child: Text(title, style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
              ),
              Expanded(
                child: ListView.builder(
                  itemCount: options.length,
                  itemBuilder: (context, index) {
                    final opt = options[index];
                    return ListTile(
                      title: Text(opt['label']!),
                      trailing: currentValue == opt['value'] ? const Icon(Icons.check, color: Colors.blue) : null,
                      onTap: () {
                        onSelected(opt['value']!);
                        Navigator.pop(context);
                      },
                    );
                  },
                ),
              ),
            ],
          ),
        );
      },
    );
  }"""
good_bottom_sheet = """  void _showSelectionBottomSheet({
    required String title,
    required List<Map<String, String>> options,
    required String currentValue,
    required Function(String) onSelected,
    Function(String)? onPreview,
  }) {
    showModalBottomSheet(
      context: context,
      builder: (context) {
        return SafeArea(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Padding(
                padding: const EdgeInsets.all(16.0),
                child: Text(title, style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
              ),
              Expanded(
                child: ListView.builder(
                  itemCount: options.length,
                  itemBuilder: (context, index) {
                    final opt = options[index];
                    return ListTile(
                      title: Text(opt['label']!),
                      trailing: Row(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          if (onPreview != null)
                            IconButton(
                              icon: const Icon(Icons.play_circle_fill, color: Colors.blue),
                              tooltip: 'Preview Voice',
                              onPressed: () => onPreview(opt['value']!),
                            ),
                          if (currentValue == opt['value'])
                            const Icon(Icons.check, color: Colors.blue),
                        ],
                      ),
                      onTap: () {
                        onSelected(opt['value']!);
                        Navigator.pop(context);
                      },
                    );
                  },
                ),
              ),
            ],
          ),
        );
      },
    ).whenComplete(() {
      if (onPreview != null) {
        _syncAudioSettings();
      }
    });
  }"""

if bad_bottom_sheet in text:
    text = text.replace(bad_bottom_sheet, good_bottom_sheet)
    print("Replaced _showSelectionBottomSheet")
else:
    print("Failed to replace _showSelectionBottomSheet")

bad_voice_ui = """            ListTile(
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
                        currentValue: (settings.ttsVoiceName ?? ''),
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
                        (settings.ttsVoiceName ?? '').isEmpty ? AppStrings.str(lang, 'default') : (settings.ttsVoiceName ?? ''),
                        overflow: TextOverflow.ellipsis,
                      ),
                    ),
                  ),
                ],
              ),
            ),"""

good_voice_ui = """            ListTile(
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
                    currentValue: settings.ttsVoiceName ?? '',
                    onSelected: (val) {
                      final selectedVoice = audio.availableVoices.firstWhere((v) => v['name'] == val);
                      settings.setTtsVoice(val, selectedVoice['locale'] ?? '');
                      _syncAudioSettings();
                      audio.speak(AppStrings.str(lang, 'tts_voice_changed'));
                    },
                    onPreview: (val) {
                      final selectedVoice = audio.availableVoices.firstWhere((v) => v['name'] == val);
                      audio.previewVoice(lang == 'en' ? 'This is a sample of this voice.' : 'Ini adalah contoh dari suara ini.', tempVoiceName: val, tempVoiceLocale: selectedVoice['locale']);
                    }
                  );
                },
                child: ConstrainedBox(
                  constraints: const BoxConstraints(maxWidth: 100),
                  child: Text(
                    (settings.ttsVoiceName ?? '').isEmpty ? AppStrings.str(lang, 'default') : (settings.ttsVoiceName ?? ''),
                    overflow: TextOverflow.ellipsis,
                  ),
                ),
              ),
            ),"""

if bad_voice_ui in text:
    text = text.replace(bad_voice_ui, good_voice_ui)
    print("Replaced voice UI")
else:
    print("Failed to replace voice UI")

with open('lib/screens/settings_screen.dart', 'w', encoding='utf-8') as f:
    f.write(text)
