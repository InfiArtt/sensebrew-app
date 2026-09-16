import re
import glob

for filename in ['lib/screens/home_screen.dart', 'lib/screens/settings_screen.dart']:
    with open(filename, 'r', encoding='utf-8') as f:
        text = f.read()

    # Find all occurrences of applySettings
    # We just need to insert `settings.ttsVolume,` after `settings.ttsPitch,`
    
    text = text.replace(
        "settings.ttsPitch,\n        settings.ttsVoiceName,",
        "settings.ttsPitch,\n        settings.ttsVolume,\n        settings.ttsVoiceName,"
    )
    text = text.replace(
        "settings.ttsPitch,\n      settings.ttsVoiceName,",
        "settings.ttsPitch,\n      settings.ttsVolume,\n      settings.ttsVoiceName,"
    )

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(text)

print("Fixed applySettings calls in UI screens.")
