import re

with open('lib/screens/custom_recipe_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('extraIngredients: extra,', 'extraIngredients: _extraIngredientsController.text,')

save_regex = r'(final recipe = Recipe\([\s\S]*?beanType: _beanType,\s*)extraIngredients: _extraIngredientsController\.text,'
content = re.sub(save_regex, r'\1extraIngredients: extra,', content)

with open('lib/screens/custom_recipe_screen.dart', 'w', encoding='utf-8') as f:
    f.write(content)
