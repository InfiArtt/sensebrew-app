import re

with open('lib/core/recipe.dart', 'r', encoding='utf-8') as f:
    text = f.read()

db_match = re.search(r'List<Recipe> recipeDatabase = \[(.*?)\];', text, re.DOTALL)
if not db_match:
    print("Database not found")
    exit(1)

db_str = db_match.group(1)
recipes = db_str.split('\n  Recipe(')

other_recipes = []
for r in recipes[1:]:
    if 'BrewMethod.v60' not in r:
        name_match = re.search(r'name:\s*"([^"]+)"', r)
        name = name_match.group(1) if name_match else "Unknown"
        
        method_match = re.search(r'method:\s*BrewMethod\.([a-zA-Z0-9_]+)', r)
        method = method_match.group(1) if method_match else "Unknown"
        
        other_recipes.append(f"[{method}] {name}")

print("Other Recipes found:")
for or_r in other_recipes:
    print(or_r)
