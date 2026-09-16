import json

def get_recipes():
    with open('lib/core/recipe.dart', 'r', encoding='utf-8') as f:
        text = f.read()
    db = text.split('recipeDatabase = [')[1]
    recipes = db.split('\n  Recipe(')[1:]
    return recipes

recipes = get_recipes()
for i, r in enumerate(recipes):
    if "James Hoffmann Ultimate V60" in r:
        print(f"--- Index {i} ---")
        print(r[:500])
