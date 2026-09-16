import os

strings_file = "lib/core/app_strings.dart"
with open(strings_file, 'r', encoding='utf-8') as f:
    text = f.read()

# Update ID
text = text.replace(
    "'action_flip': 'Balikkan Alat',",
    "'action_flip': 'Balikkan ke atas gelas',"
)

# Update EN
text = text.replace(
    "'action_flip': 'Flip Device',",
    "'action_flip': 'Flip onto cup',"
)

with open(strings_file, 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated action_flip strings successfully.")
