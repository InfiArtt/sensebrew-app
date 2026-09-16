import os

strings_file = "lib/core/app_strings.dart"
with open(strings_file, 'r', encoding='utf-8') as f:
    text = f.read()

# Update ID
text = text.replace(
    "'action_swirl': 'Swirl / Goyang Alat',",
    "'action_swirl': 'Swirl perlahan',"
)

# Update EN
text = text.replace(
    "'action_swirl': 'Swirl Device',",
    "'action_swirl': 'Swirl gently',"
)

with open(strings_file, 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated action_swirl strings successfully.")
