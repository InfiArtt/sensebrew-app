import re
with open('lib/core/recipe.dart', 'r', encoding='utf-8') as f:
    text = f.read()

v60_recipes = re.findall(r'name: [\'"](.*?)[\'"].*?method: BrewMethod\.v60', text, re.DOTALL)
print(f"Total v60 found: {len(v60_recipes)}")
for name in v60_recipes:
    print(name)
