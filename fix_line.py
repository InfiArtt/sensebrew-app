import re
with open('lib/screens/custom_recipe_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('        final lang = Provider.of<SettingsState>(context, listen: false).appLanguage; _extraIngredientsController.text = AppStrings.str(lang, newRecipe.extraIngredients);\n', '')

with open('lib/screens/custom_recipe_screen.dart', 'w', encoding='utf-8') as f:
    f.write(content)
