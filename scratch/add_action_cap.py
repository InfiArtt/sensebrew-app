import os

strings_file = "lib/core/app_strings.dart"
with open(strings_file, 'r', encoding='utf-8') as f:
    text = f.read()

# Add action_cap if not exists in ID
if "'action_cap':" not in text.split("'en':")[0]:
    text = text.replace(
        "'action_flip':",
        "'action_cap': 'Pasang Tutup',\n      'action_flip':"
    )

with open(strings_file, 'w', encoding='utf-8') as f:
    f.write(text)

print("Added action_cap to ID strings if missing.")
