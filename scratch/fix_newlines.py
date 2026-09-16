import re

with open('lib/screens/brewing_screen.dart', 'r', encoding='utf-8') as f:
    text = f.read()

# Fix the broken multiline string
pattern = r"'\$\{AppStrings\.str\(lang, widget\.recipe\.name\)\}\n\$\{widget\.recipe\.coffeeGrams\}g"
text = re.sub(pattern, r"'\${AppStrings.str(lang, widget.recipe.name)}\\n${widget.recipe.coffeeGrams}g", text)

with open('lib/screens/brewing_screen.dart', 'w', encoding='utf-8') as f:
    f.write(text)

print("Fixed newlines in brewing_screen.dart")
