import re

with open('lib/core/recipe.dart', 'r', encoding='utf-8') as f:
    text = f.read()

recipes = re.split(r'Recipe\(', text)[1:]
for r in recipes:
    if 'BrewMethod.vietnamDrip' in r:
        name_m = re.search(r'name:\s*"([^"]+)"', r)
        if name_m:
            print(name_m.group(1))
