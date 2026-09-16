import re

with open('lib/core/recipe.dart', 'r', encoding='utf-8') as f:
    text = f.read()

# simple regex to find recipes
recipes = re.findall(r'Recipe\(\s*name: "(.*?)".*?description: "(.*?)".*?extraIngredients: "(.*?)".*?phases: \[(.*?)\]', text, flags=re.DOTALL)
if not recipes:
    recipes = re.findall(r'Recipe\(\s*name: "(.*?)".*?description: "(.*?)".*?phases: \[(.*?)\]', text, flags=re.DOTALL)

for r in recipes:
    print(f"Name: {r[0]}")
    print(f"Desc: {r[1]}")
    print("-----")
