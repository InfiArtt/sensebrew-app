import re

def update_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        text = f.read()

    # In brewing_screen.dart: widget.recipe.name
    text = re.sub(r'Text\(widget\.recipe\.name\)', r"Text(AppStrings.str(lang, widget.recipe.name))", text)
    text = re.sub(r'\'\$\{widget\.recipe\.name\}\\n\$\{widget\.recipe\.coffeeGrams\}', r"'${AppStrings.str(lang, widget.recipe.name)}\n${widget.recipe.coffeeGrams}", text)
    text = re.sub(r'widget\.recipe\.name\,', r"AppStrings.str(lang, widget.recipe.name),", text)

    # In method_recipe_screen.dart: recipe.name
    text = re.sub(r'Text\(recipe\.name\,', r"Text(AppStrings.str(lang, recipe.name),", text)
    text = re.sub(r'recipe\.name\,', r"AppStrings.str(lang, recipe.name),", text)
    text = re.sub(r'recipe\.name\)\)', r"AppStrings.str(lang, recipe.name)))", text)

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(text)

update_file('lib/screens/brewing_screen.dart')
update_file('lib/screens/method_recipe_screen.dart')
print("Updated UI files!")
