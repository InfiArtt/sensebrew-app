import re

with open('lib/screens/custom_recipe_screen.dart', 'r', encoding='utf-8') as f:
    code = f.read()

target = '''        totalDurationSeconds: time,
        phases: phases,
      );'''

replacement = '''        totalDurationSeconds: time,
        phases: phases,
        targetGrindSizeMicrons: _targetGrindSizeMicrons,
        extraIngredients: _extraIngredientsController.text,
      );'''

code = code.replace(target, replacement)

with open('lib/screens/custom_recipe_screen.dart', 'w', encoding='utf-8') as f:
    f.write(code)

print('Save recipe fixed!')
