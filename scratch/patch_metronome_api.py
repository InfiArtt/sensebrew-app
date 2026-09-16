import re

# 1. FIX TIMER_STATE.DART
with open('lib/core/timer_state.dart', 'r', encoding='utf-8') as f:
    timer_code = f.read()

timer_code = timer_code.replace(
    "_audioPlayer.seek(Duration.zero);\n        _audioPlayer.resume();",
    "_audioPlayer.play(AssetSource('tick.wav'));"
)

with open('lib/core/timer_state.dart', 'w', encoding='utf-8') as f:
    f.write(timer_code)

# 2. FIX SETTINGS_SCREEN.DART
with open('lib/screens/settings_screen.dart', 'r', encoding='utf-8') as f:
    settings_code = f.read()

old_gemini_content = """                            if (settings.aiProvider == 'gemini') ...[
                              const Text("Google Gemini (Gemini 2.5 Flash):", style: TextStyle(fontWeight: FontWeight.bold)),
                              Text(AppStrings.str(lang, 'gemini_help_content')),
                            ],
                            if (settings.aiProvider == 'groq') ...[
                              const Text("Groq (Llama 3):", style: TextStyle(fontWeight: FontWeight.bold)),
                              Text(AppStrings.str(lang, 'groq_help_content')),
                            ],"""

new_gemini_content = """                            if (settings.aiProvider == 'gemini') ...[
                              const Text("Google Gemini (Gemini 2.5 Flash):", style: TextStyle(fontWeight: FontWeight.bold)),
                              ...AppStrings.str(lang, 'gemini_help_content').split('\\n').where((s) => s.trim().isNotEmpty).map((line) => Padding(padding: const EdgeInsets.only(top: 8.0), child: Text(line))),
                            ],
                            if (settings.aiProvider == 'groq') ...[
                              const Text("Groq (Llama 3):", style: TextStyle(fontWeight: FontWeight.bold)),
                              ...AppStrings.str(lang, 'groq_help_content').split('\\n').where((s) => s.trim().isNotEmpty).map((line) => Padding(padding: const EdgeInsets.only(top: 8.0), child: Text(line))),
                            ],"""

settings_code = settings_code.replace(old_gemini_content, new_gemini_content)

with open('lib/screens/settings_screen.dart', 'w', encoding='utf-8') as f:
    f.write(settings_code)

print("Fixed metronome resume bug and settings dialog text!")
