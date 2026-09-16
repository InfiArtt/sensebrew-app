import re
with open('lib/screens/custom_recipe_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('extraIngredients: extra,\n          method: widget.initialRecipe?.method', 'extraIngredients: _extraIngredientsController.text,\n          method: widget.initialRecipe?.method')

with open('lib/screens/custom_recipe_screen.dart', 'w', encoding='utf-8') as f:
    f.write(content)
