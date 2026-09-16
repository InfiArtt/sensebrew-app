import re

with open('lib/screens/brewing_screen.dart', 'r', encoding='utf-8') as f:
    text = f.read()

# Fix line 84
text = text.replace("name: AppStrings.str(lang, widget.recipe.name),", "name: widget.recipe.name,")

# Fix line 376
text = text.replace("appBar: AppBar(title: Text(AppStrings.str(lang, widget.AppStrings.str(lang, recipe.name)))),", "appBar: AppBar(title: Text(AppStrings.str(lang, widget.recipe.name))),")

with open('lib/screens/brewing_screen.dart', 'w', encoding='utf-8') as f:
    f.write(text)

print("Fixed syntax errors in brewing_screen.dart")
