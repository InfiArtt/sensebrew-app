import re

with open('lib/core/recipe.dart', 'r', encoding='utf-8') as f:
    text = f.read()

# Extract the database part
db_match = re.search(r'List<Recipe> recipeDatabase = \[(.*?)\];', text, re.DOTALL)
if not db_match:
    print("Database not found")
    exit(1)

db_str = db_match.group(1)
recipes = db_str.split('\n  Recipe(')

v60_recipes = []
for r in recipes[1:]:
    if 'BrewMethod.v60' in r:
        name_match = re.search(r'name:\s*"([^"]+)"', r)
        name = name_match.group(1) if name_match else "Unknown"
        
        water_match = re.search(r'totalWaterMl:\s*(\d+)', r)
        water = water_match.group(1) if water_match else "Unknown"
        
        coffee_match = re.search(r'coffeeGrams:\s*(\d+)', r)
        coffee = coffee_match.group(1) if coffee_match else "Unknown"
        
        phases_match = re.search(r'phases:\s*\[(.*?)\]', r, re.DOTALL)
        phases_str = phases_match.group(1) if phases_match else ""
        
        # Count pours
        pours = len(re.findall(r'pourAmountMl:', phases_str))
        # Count stirs/swirls
        stirs = len(re.findall(r'PhaseAction\.stir', phases_str))
        
        v60_recipes.append(f"- {name} ({coffee}g : {water}ml) -> {pours} Tuangan, {stirs} Aduk/Swirl")

print("V60 Recipes found:")
for vr in v60_recipes:
    print(vr)
