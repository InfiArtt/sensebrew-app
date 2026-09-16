import re

with open('lib/core/app_strings.dart', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace Indonesian labels
text = text.replace("'Tombol buat resep seduh kustom.'", "'Buat resep seduh kustom.'")
text = text.replace("'Tombol buat resep otomatis dengan AI.'", "'Buat resep otomatis dengan AI.'")

# Replace English labels
text = text.replace("'Button to create a custom brew recipe.'", "'Create a custom brew recipe.'")
text = text.replace("'Button to automatically create a recipe with AI.'", "'Create a recipe automatically with AI.'") # if it exists
text = text.replace("'Button to generate recipe automatically with AI.'", "'Generate recipe automatically with AI.'") # alternate guess

# Write back
with open('lib/core/app_strings.dart', 'w', encoding='utf-8') as f:
    f.write(text)

print("Removed 'Tombol/Button' prefix from accessibility labels.")
