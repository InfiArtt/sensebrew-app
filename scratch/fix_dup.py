import re

with open('lib/screens/custom_recipe_screen.dart', 'r', encoding='utf-8') as f:
    text = f.read()

# Remove the duplicated method line
text = text.replace("        method: widget.initialRecipe?.method ?? BrewMethod.v60,\n", "")
text = text.replace("      method: widget.initialRecipe?.method ?? BrewMethod.v60,\n", "")

with open('lib/screens/custom_recipe_screen.dart', 'w', encoding='utf-8') as f:
    f.write(text)
