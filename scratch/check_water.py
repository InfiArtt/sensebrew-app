import re

def parse_recipes(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    recipe_pattern = re.compile(r'Recipe\((.*?)\),', re.DOTALL)
    recipes = recipe_pattern.findall(content)
    
    for i, r in enumerate(recipes):
        name_match = re.search(r'name:\s*"([^"]+)"', r)
        name = name_match.group(1) if name_match else f"Recipe {i}"
        
        water_match = re.search(r'totalWaterMl:\s*([\d\.]+)', r)
        total_water = float(water_match.group(1)) if water_match else 0.0
        
        pour_amounts = re.findall(r'pourAmountMl:\s*([\d\.]+)', r)
        sum_pours = sum([float(p) for p in pour_amounts])
        
        if abs(total_water - sum_pours) > 1.0:
            print(f"[{name}] MISMATCH! totalWaterMl: {total_water}, sum of pours: {sum_pours}")

parse_recipes('lib/core/recipe.dart')
