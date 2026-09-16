import re

with open('lib/core/recipe.dart', 'r', encoding='utf-8') as f:
    text = f.read()

recipes = re.findall(r'name:\s*"([^"]+)"', text)
for r in recipes:
    print(r)
