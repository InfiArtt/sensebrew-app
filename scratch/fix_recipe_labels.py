import os

strings_file = "lib/core/app_strings.dart"
with open(strings_file, 'r', encoding='utf-8') as f:
    text = f.read()

# ID
text = text.replace(
    "'recipe_label': 'Resep {0}, Kopi {1} gram, Air {2} ml',",
    "'recipe_label': 'Resep {0}. {1} gram kopi. {2} mililiter air.',"
)
text = text.replace(
    "'custom_recipe_label': 'Buat resep seduh kustom',",
    "'custom_recipe_label': 'Tombol buat resep seduh kustom.',"
)
text = text.replace(
    "'ai_recipe_label': 'Buat resep otomatis dengan AI',",
    "'ai_recipe_label': 'Tombol buat resep otomatis dengan AI.',"
)

# EN
text = text.replace(
    "'recipe_label': 'Recipe {0}, Coffee {1} grams, Water {2} ml',",
    "'recipe_label': '{0} recipe. {1} grams of coffee. {2} milliliters of water.',"
)
text = text.replace(
    "'custom_recipe_label': 'Create custom brewing recipe',",
    "'custom_recipe_label': 'Button to create a custom brew recipe.',"
)
text = text.replace(
    "'ai_recipe_label': 'Create recipe automatically with AI',",
    "'ai_recipe_label': 'Button to create a recipe automatically with AI.',"
)

with open(strings_file, 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated recipe label strings successfully.")
