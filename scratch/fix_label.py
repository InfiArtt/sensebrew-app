with open('lib/screens/custom_recipe_screen.dart', 'r', encoding='utf-8') as f:
    code = f.read()

code = code.replace("AppStrings.str(lang, 'recipe_note')", "'Deskripsi Resep'")

with open('lib/screens/custom_recipe_screen.dart', 'w', encoding='utf-8') as f:
    f.write(code)

print('Labels fixed')
