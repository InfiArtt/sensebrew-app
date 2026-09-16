import re

with open('lib/screens/custom_recipe_screen.dart', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. We need to add _targetGrindSizeMicrons assignment in didChangeDependencies
target_deps = r"(_timeController\.text = widget\.initialRecipe!\.totalDurationSeconds\.toString\(\);)"

replacement_deps = r"""\1
        
        // Snap grind size to predefined values
        int rawGrind = widget.initialRecipe!.targetGrindSizeMicrons;
        List<int> validGrinds = [400, 600, 800, 1000, 1200, 1400];
        _targetGrindSizeMicrons = validGrinds.reduce((a, b) => (rawGrind - a).abs() < (rawGrind - b).abs() ? a : b);
        
        _extraIngredientsController.text = widget.initialRecipe!.extraIngredients;"""

code = re.sub(target_deps, replacement_deps, code)

# 2. Also make sure the variables are declared
if "_extraIngredientsController" not in code:
    print("Oops, need to add _extraIngredientsController")
    target_vars = r"(final TextEditingController _noteController = TextEditingController\(\);)"
    replacement_vars = r"""\1
  final TextEditingController _extraIngredientsController = TextEditingController();"""
    code = re.sub(target_vars, replacement_vars, code)

with open('lib/screens/custom_recipe_screen.dart', 'w', encoding='utf-8') as f:
    f.write(code)

print('Edit state fixed!')
