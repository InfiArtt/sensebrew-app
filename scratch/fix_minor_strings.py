import os

strings_file = "lib/core/app_strings.dart"
with open(strings_file, 'r', encoding='utf-8') as f:
    text = f.read()

# Insert new keys into ID
text = text.replace(
    "'calib_q3': 'Butuh berapa TIK untuk 1 putaran tuang melingkar?',",
    "'calib_q3': 'Butuh berapa TIK untuk 1 putaran tuang melingkar?',\n      'toggle_api_key': 'Tampilkan atau sembunyikan API Key',\n      'restore_success': 'Resep bawaan berhasil dikembalikan!',"
)

# Insert new keys into EN
text = text.replace(
    "'calib_q3': 'How many TICKs for 1 circular pour rotation?',",
    "'calib_q3': 'How many TICKs for 1 circular pour rotation?',\n      'toggle_api_key': 'Show or hide API Key',\n      'restore_success': 'Default recipes restored successfully!',"
)

with open(strings_file, 'w', encoding='utf-8') as f:
    f.write(text)


settings_file = "lib/screens/settings_screen.dart"
with open(settings_file, 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace("'Tampilkan atau sembunyikan API Key'", "AppStrings.str(lang, 'toggle_api_key') ?? 'Show/Hide API Key'")
text = text.replace("const SnackBar(content: Text('Resep bawaan berhasil dikembalikan!'))", "SnackBar(content: Text(AppStrings.str(lang, 'restore_success') ?? 'Restored'))")

with open(settings_file, 'w', encoding='utf-8') as f:
    f.write(text)

print("Updates completed successfully.")
