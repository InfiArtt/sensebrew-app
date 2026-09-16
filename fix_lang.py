import re
with open('lib/screens/custom_recipe_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('if (newRecipe != null && newRecipe is Recipe) {\n        setState(() {', 'if (newRecipe != null && newRecipe is Recipe) {\n        final lang = Provider.of<SettingsState>(context, listen: false).appLanguage;\n        setState(() {')

with open('lib/screens/custom_recipe_screen.dart', 'w', encoding='utf-8') as f:
    f.write(content)
