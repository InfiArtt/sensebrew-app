import re

with open('lib/core/recipe.dart', 'r', encoding='utf-8') as f:
    text = f.read()

recipes = re.split(r'Recipe\(', text)[1:]
for r in recipes:
    if 'BrewMethod.aeropress' in r and 'PhaseAction.press' not in r:
        name_m = re.search(r'name:\s*"([^"]+)"', r)
        print('Missing press:', name_m.group(1) if name_m else 'Unknown')
