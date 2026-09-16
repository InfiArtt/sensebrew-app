import re

def fix_recipes(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # 1. Fix Alan Adler
    content = content.replace(
        'name: "Alan Adler (Original)",',
        'name: "Alan Adler (Original)",\n    extraIngredients: "140ml Air panas tambahan (Bypass)",'
    )
    content = content.replace(
        'totalWaterMl: 200,\n      totalDurationSeconds: 90,\n      method: BrewMethod.aeropress,\n      targetGrindSizeMicrons: 500,\n      phases: [\n        RecipePhase(startTimeSeconds: 0, pourAmountMl: 60',
        'totalWaterMl: 60,\n      totalDurationSeconds: 90,\n      method: BrewMethod.aeropress,\n      targetGrindSizeMicrons: 500,\n      phases: [\n        RecipePhase(startTimeSeconds: 0, pourAmountMl: 60'
    )
    
    # 2. Fix Aeropress Robusta Sweet
    content = content.replace(
        'name: "Aeropress Robusta Sweet",\n    description: "Khusus untuk kopi Robusta. Ekstraksi singkat dengan suhu 85C agar tidak terlalu pahit.\\n\\nEstimasi Rasa: Pahit khas Robusta namun diimbangi tekstur kental dan rasa nutty yang manis.",\n    coffeeGrams: 15, totalWaterMl: 60,\n      extraIngredients: "Air panas/es tambahan untuk mengencerkan (Bypass)", totalDurationSeconds: 120,\n    method: BrewMethod.aeropress, targetGrindSizeMicrons: 700, beanType: \'Robusta\',\n    phases: [\n      RecipePhase(startTimeSeconds: 0, pourAmountMl: 200',
        'name: "Aeropress Robusta Sweet",\n    description: "Khusus untuk kopi Robusta. Ekstraksi singkat dengan suhu 85C agar tidak terlalu pahit.\\n\\nEstimasi Rasa: Pahit khas Robusta namun diimbangi tekstur kental dan rasa nutty yang manis.",\n    coffeeGrams: 15, totalWaterMl: 60,\n      extraIngredients: "Air panas/es tambahan untuk mengencerkan (Bypass)", totalDurationSeconds: 120,\n    method: BrewMethod.aeropress, targetGrindSizeMicrons: 700, beanType: \'Robusta\',\n    phases: [\n      RecipePhase(startTimeSeconds: 0, pourAmountMl: 60'
    )
    
    # 3. Fix time mismatches
    recipes = content.split('Recipe(')
    new_content = recipes[0]
    for i, r in enumerate(recipes):
        if i == 0: continue
        
        duration_match = re.search(r'totalDurationSeconds:\s*([\d]+)', r)
        starts = re.findall(r'startTimeSeconds:\s*([\d]+)', r)
        
        if duration_match and starts:
            duration = int(duration_match.group(1))
            last_start = max([int(s) for s in starts])
            
            if last_start >= duration:
                # Need to replace the totalDurationSeconds
                new_duration = last_start + 30
                # Be careful, replace only the specific one
                # r is the recipe string
                r = r.replace(f'totalDurationSeconds: {duration}', f'totalDurationSeconds: {new_duration}', 1)
                
        new_content += 'Recipe(' + r
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

fix_recipes('lib/core/recipe.dart')
