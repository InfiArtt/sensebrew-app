import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../core/settings_state.dart';
import '../core/timer_state.dart';
import '../core/recipe_repository.dart';
import '../core/app_strings.dart';
import '../widgets/native_text_field.dart';


class SettingsScreen extends StatefulWidget {
  const SettingsScreen({Key? key}) : super(key: key);

  @override
  State<SettingsScreen> createState() => _SettingsScreenState();
}

class _SettingsScreenState extends State<SettingsScreen> {
  bool _isGeminiObscured = true;
  bool _isGroqObscured = true;
  void _syncAudioSettings() {
    final settings = Provider.of<SettingsState>(context, listen: false);
    final audio = Provider.of<TimerAudioState>(context, listen: false);
    audio.applySettings(
      settings.appLanguage,
      settings.ttsSpeed,
      settings.isTtsEnabled,
      settings.audioOutputMode,
      settings.ttsPitch,
      settings.ttsVolume,
      (settings.ttsVoiceName ?? ''),
      settings.ttsVoiceLocale,
      settings.hapticMetronome,
      settings.audioMetronome,
    );
  }

  void _showSelectionBottomSheet({
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
  }

  @override
  Widget build(BuildContext context) {
    final settings = Provider.of<SettingsState>(context);
    final audio = Provider.of<TimerAudioState>(context, listen: false);
    final lang = settings.appLanguage;

    return Scaffold(
      appBar: AppBar(
        title: Text(AppStrings.str(lang, 'settings_title')),
      ),
      body: SingleChildScrollView(child: Column(
        children: [
          const SizedBox(height: 16),
          ListTile(
            title: Text(AppStrings.str(lang, 'app_lang'), style: const TextStyle(fontSize: 18)),
            subtitle: Text(AppStrings.str(lang, 'app_lang_desc')),
            trailing: ElevatedButton(
              onPressed: () {
                _showSelectionBottomSheet(
                  title: AppStrings.str(lang, 'app_lang_label'),
                  options: [
                    {'value': 'en', 'label': 'English'},
                    {'value': 'id', 'label': 'Bahasa Indonesia'},
                  ],
                  currentValue: settings.appLanguage,
                  onSelected: (val) {
                    settings.setAppLanguage(val);
                  },
                );
              },
              child: Text(settings.appLanguage == 'en' ? 'English' : 'Indonesia'),
            ),
          ),
          const Divider(),
          ListTile(
            title: Text(AppStrings.str(lang, 'gemini_title'), style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            subtitle: Text(AppStrings.str(lang, 'gemini_desc')),
            trailing: ElevatedButton(
              onPressed: () {
                _showSelectionBottomSheet(
                  title: AppStrings.str(lang, 'gemini_title'),
                  options: [
                    {'value': 'gemini', 'label': 'Google Gemini'},
                    {'value': 'groq', 'label': 'Groq (Llama 3)'},
                  ],
                  currentValue: settings.aiProvider,
                  onSelected: (val) {
                    settings.setAiProvider(val);
                  },
                );
              },
              child: Text(settings.aiProvider == 'gemini' ? 'Gemini' : 'Groq'),
            ),
          ),
          const SizedBox(height: 8),
          if (settings.aiProvider == 'gemini')
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 16.0),
              child: Row(
                children: [
                  Expanded(
                    child: NativeTextField(
                      key: const ValueKey('gemini_api_key'),
                      label: AppStrings.str(lang, 'gemini_api_key_label') ?? 'Google Gemini API Key',
                      value: settings.geminiApiKey,
                      isPassword: _isGeminiObscured,
                      onChanged: (val) => settings.setGeminiApiKey(val),
                    ),
                  ),
                  IconButton(
                    icon: Icon(_isGeminiObscured ? Icons.visibility : Icons.visibility_off),
                    tooltip: AppStrings.str(lang, _isGeminiObscured ? 'show_api_key' : 'hide_api_key') ?? 'Toggle API Key',
                    onPressed: () {
                      setState(() {
                        _isGeminiObscured = !_isGeminiObscured;
                      });
                    },
                  ),
                ],
              ),
            ),

          if (settings.aiProvider == 'groq')
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 16.0),
              child: Row(
                children: [
                  Expanded(
                    child: NativeTextField(
                      key: const ValueKey('groq_api_key'),
                      label: AppStrings.str(lang, 'groq_api_key_label') ?? 'Groq API Key',
                      value: settings.groqApiKey,
                      isPassword: _isGroqObscured,
                      onChanged: (val) => settings.setGroqApiKey(val),
                    ),
                  ),
                  IconButton(
                    icon: Icon(_isGroqObscured ? Icons.visibility : Icons.visibility_off),
                    tooltip: AppStrings.str(lang, _isGroqObscured ? 'show_api_key' : 'hide_api_key') ?? 'Toggle API Key',
                    onPressed: () {
                      setState(() {
                        _isGroqObscured = !_isGroqObscured;
                      });
                    },
                  ),
                ],
              ),
            ),

          const SizedBox(height: 8),
          Align(
            alignment: Alignment.centerLeft,
            child: TextButton.icon(
              icon: const Icon(Icons.help_outline),
              label: Text(AppStrings.str(lang, settings.aiProvider == 'gemini' ? 'gemini_help_title' : 'groq_help_title')),
              onPressed: () {
                showDialog(
                  context: context,
                  builder: (context) => AlertDialog(
                    title: Text(AppStrings.str(lang, settings.aiProvider == 'gemini' ? 'gemini_help_title' : 'groq_help_title')),
                    content: SingleChildScrollView(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        mainAxisSize: MainAxisSize.min,
                        children: [
                            if (settings.aiProvider == 'gemini') ...[
                              const Text("Google Gemini (Gemini 2.5 Flash):", style: TextStyle(fontWeight: FontWeight.bold)),
                              ...AppStrings.str(lang, 'gemini_help_content').split('\n').where((s) => s.trim().isNotEmpty).map((line) => Padding(padding: const EdgeInsets.only(top: 8.0), child: Text(line))),
                            ],
                            if (settings.aiProvider == 'groq') ...[
                              const Text("Groq (Llama 3):", style: TextStyle(fontWeight: FontWeight.bold)),
                              ...AppStrings.str(lang, 'groq_help_content').split('\n').where((s) => s.trim().isNotEmpty).map((line) => Padding(padding: const EdgeInsets.only(top: 8.0), child: Text(line))),
                            ],
                        ],
                      ),
                    ),
                    actions: [
                      TextButton(
                        onPressed: () => Navigator.pop(context),
                        child: Text(AppStrings.str(lang, 'close')),
                      ),
                    ],
                  ),
                );
              },
            ),
          ),

          Padding(
            padding: const EdgeInsets.all(16.0),
            child: Text(AppStrings.str(lang, 'tts_title'), style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
          ),
          SwitchListTile(
            title: Text(
              AppStrings.str(lang, 'tts_enable'), 
              style: const TextStyle(fontSize: 18),
            ),
            subtitle: Text(AppStrings.str(lang, 'tts_enable_desc')),
            value: settings.isTtsEnabled,
            onChanged: (val) {
              settings.setTtsEnabled(val);
              _syncAudioSettings();
            },
          ),
          SwitchListTile(
            title: Text(
              lang == 'en' ? 'Audio Metronome' : 'Metronom Suara', 
              style: const TextStyle(fontSize: 18),
            ),
            subtitle: Text(lang == 'en' ? 'Play tick sound on every beat' : 'Mainkan suara detik di setiap ketukan'),
            value: settings.audioMetronome,
            onChanged: (val) {
              settings.setAudioMetronome(val);
              _syncAudioSettings();
            },
          ),
          SwitchListTile(
            title: Text(
              lang == 'en' ? 'Visual Metronome' : 'Metronom Visual', 
              style: const TextStyle(fontSize: 18),
            ),
            subtitle: Text(lang == 'en' ? 'Screen flashes on every beat' : 'Layar berkedip di setiap ketukan'),
            value: settings.visualMetronome,
            onChanged: (val) {
              settings.setVisualMetronome(val);
            },
          ),
          SwitchListTile(
            title: Text(
              lang == 'en' ? 'Haptic Metronome' : 'Getaran Metronom', 
              style: const TextStyle(fontSize: 18),
            ),
            subtitle: Text(lang == 'en' ? 'Vibrate device on every beat' : 'Perangkat bergetar di setiap ketukan'),
            value: settings.hapticMetronome,
            onChanged: (val) {
              settings.setHapticMetronome(val);
              _syncAudioSettings();
            },
          ),
          ListTile(
            title: Text(AppStrings.str(lang, 'tts_channel'), style: const TextStyle(fontSize: 18)),
            subtitle: Text(AppStrings.str(lang, 'tts_channel_desc')),
            trailing: ElevatedButton(
              onPressed: () {
                _showSelectionBottomSheet(
                  title: AppStrings.str(lang, 'tts_channel'),
                  options: [
                    {'value': 'tts', 'label': AppStrings.str(lang, 'tts_channel_app')},
                    {'value': 'screen_reader', 'label': AppStrings.str(lang, 'tts_channel_sr')},
                  ],
                  currentValue: settings.audioOutputMode,
                  onSelected: (val) {
                    settings.setAudioOutputMode(val);
                    _syncAudioSettings();
                    audio.speak(AppStrings.str(lang, 'tts_channel_changed'));
                  },
                );
              },
              child: Text(settings.audioOutputMode == 'tts' ? AppStrings.str(lang, 'tts_channel_app') : AppStrings.str(lang, 'tts_channel_sr')),
            ),
          ),
          if (settings.audioOutputMode == 'tts') ...[
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
            ),
          ],
          const SizedBox(height: 32),
          const Divider(),
          const SizedBox(height: 16),
          ListTile(
            title: Text(AppStrings.str(lang, 'settings_restore_title'), style: const TextStyle(fontSize: 18, color: Colors.red)),
            subtitle: Text(AppStrings.str(lang, 'settings_restore_sub')),
            trailing: const Icon(Icons.restore, color: Colors.red),
            onTap: () async {
              final repo = Provider.of<RecipeRepository>(context, listen: false);
              await repo.restoreDefaults();
              if (mounted) {
                ScaffoldMessenger.of(context).showSnackBar(
                  SnackBar(content: Text(AppStrings.str(lang, 'restore_success') ?? 'Restored')),
                );
              }
            },
          ),
          const SizedBox(height: 32),
        ],
      )),
    );
  }
}



