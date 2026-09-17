import re

# Patch method_recipe_screen.dart
with open('lib/screens/method_recipe_screen.dart', 'r', encoding='utf-8') as f:
    text = f.read()

old_nav = "MaterialPageRoute(builder: (_) => CustomRecipeScreen()),"
new_nav = "MaterialPageRoute(builder: (_) => CustomRecipeScreen(targetMethod: widget.method)),"

if old_nav in text:
    text = text.replace(old_nav, new_nav)
    with open('lib/screens/method_recipe_screen.dart', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Patched method_recipe_screen.dart")
else:
    print("Could not find old_nav in method_recipe_screen.dart")

# Patch custom_recipe_screen.dart
with open('lib/screens/custom_recipe_screen.dart', 'r', encoding='utf-8') as f:
    text2 = f.read()

old_class = "class CustomRecipeScreen extends StatefulWidget {\n  final Recipe? initialRecipe;\n  const CustomRecipeScreen({super.key, this.initialRecipe});"
new_class = "class CustomRecipeScreen extends StatefulWidget {\n  final Recipe? initialRecipe;\n  final BrewMethod? targetMethod;\n  const CustomRecipeScreen({super.key, this.initialRecipe, this.targetMethod});"
text2 = text2.replace(old_class, new_class)

old_draft = "currentDraft = Recipe(\n        id: widget.initialRecipe?.id,"
new_draft = "currentDraft = Recipe(\n        id: widget.initialRecipe?.id,\n        method: widget.initialRecipe?.method ?? widget.targetMethod ?? BrewMethod.v60,"
text2 = text2.replace(old_draft, new_draft)

old_save = "final recipe = Recipe(\n      id: saveAsNew ? null : widget.initialRecipe?.id,"
new_save = "final recipe = Recipe(\n      id: saveAsNew ? null : widget.initialRecipe?.id,\n      method: widget.initialRecipe?.method ?? widget.targetMethod ?? BrewMethod.v60,"
text2 = text2.replace(old_save, new_save)

with open('lib/screens/custom_recipe_screen.dart', 'w', encoding='utf-8') as f:
    f.write(text2)
print("Patched custom_recipe_screen.dart")
