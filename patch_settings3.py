import re

with open('lib/screens/settings_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("label: Text(lang == 'en' ? 'How to get an API Key?' : 'Cara Mendapatkan API Key'),", "label: Text(AppStrings.str(lang, 'gemini_help_title')),")

with open('lib/screens/settings_screen.dart', 'w', encoding='utf-8') as f:
    f.write(content)
