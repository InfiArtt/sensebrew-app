import re

def final_audit(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    recipes = content.split('Recipe(')
    
    for i, r in enumerate(recipes):
        if i == 0: continue
        
        name_match = re.search(r'name:\s*"([^"]+)"', r)
        name = name_match.group(1) if name_match else f"Recipe {i}"
        
        # 1. Estimasi Rasa
        desc_match = re.search(r'description:\s*"([^"]+)"', r)
        if desc_match:
            desc = desc_match.group(1)
            if "Estimasi Rasa:" not in desc:
                print(f"[{name}] WARNING: No 'Estimasi Rasa:' in description")
        else:
            print(f"[{name}] ERROR: No description")
            
        # 2. Brew Ratio
        coffee_match = re.search(r'coffeeGrams:\s*([\d\.]+)', r)
        water_match = re.search(r'totalWaterMl:\s*([\d\.]+)', r)
        
        if coffee_match and water_match:
            coffee = float(coffee_match.group(1))
            water = float(water_match.group(1))
            
            if coffee > 0:
                ratio = water / coffee
                if ratio < 3.0:
                    print(f"[{name}] WARNING: Extremely low brew ratio 1:{ratio:.1f}")
                elif ratio > 25.0:
                    print(f"[{name}] WARNING: Extremely high brew ratio 1:{ratio:.1f}")
        
        # 3. Grind Size
        grind_match = re.search(r'targetGrindSizeMicrons:\s*([\d]+)', r)
        if grind_match:
            grind = int(grind_match.group(1))
            if grind < 250 or grind > 1800:
                print(f"[{name}] WARNING: Unusual grind size: {grind} microns")
        
        # 4. Bean Type
        bean_match = re.search(r'beanType:\s*\'([^\']+)\'', r)
        if not bean_match:
            bean_match2 = re.search(r'beanType:\s*"([^"]+)"', r)
            if not bean_match2:
                print(f"[{name}] WARNING: No beanType specified")

final_audit('lib/core/recipe.dart')
