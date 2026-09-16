import re

def check_recipes(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    recipes = content.split('Recipe(')
    for i, r in enumerate(recipes):
        if i == 0: continue # First part is preamble
        
        name_match = re.search(r'name:\s*"([^"]+)"', r)
        name = name_match.group(1) if name_match else f"Recipe {i}"
        
        water_match = re.search(r'totalWaterMl:\s*([\d\.]+)', r)
        total_water = float(water_match.group(1)) if water_match else 0.0
        
        pour_amounts = re.findall(r'pourAmountMl:\s*([\d\.]+)', r)
        sum_pours = sum([float(p) for p in pour_amounts])
        
        if abs(total_water - sum_pours) > 1.0:
            print(f"[{name}] WATER MISMATCH! totalWaterMl: {total_water}, sum of pours: {sum_pours}")
            
        # Let's also check totalDurationSeconds vs last phase start time
        duration_match = re.search(r'totalDurationSeconds:\s*([\d]+)', r)
        duration = int(duration_match.group(1)) if duration_match else 0
        
        starts = re.findall(r'startTimeSeconds:\s*([\d]+)', r)
        if starts:
            last_start = max([int(s) for s in starts])
            if last_start >= duration:
                print(f"[{name}] TIME MISMATCH! duration {duration} is <= last phase {last_start}")

check_recipes('lib/core/recipe.dart')
