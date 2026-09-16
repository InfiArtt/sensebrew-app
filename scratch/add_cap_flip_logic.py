import re

with open('lib/core/recipe.dart', 'r', encoding='utf-8') as f:
    text = f.read()

def insert_phase(recipe_name, search_phase, new_phase):
    global text
    pattern = r'(name: "' + recipe_name + r'".*?' + search_phase.replace('(', r'\(').replace(')', r'\)') + r')'
    text = re.sub(pattern, r'\1\n      ' + new_phase + ',', text, flags=re.DOTALL)

def replace_phase(recipe_name, search_phase, replace_phase):
    global text
    pattern = r'(name: "' + recipe_name + r'".*?)' + search_phase.replace('(', r'\(').replace(')', r'\)')
    text = re.sub(pattern, r'\1' + replace_phase, text, flags=re.DOTALL)

# 1. Tim Wendelboe Aeropress
# 0:15 stir, 0:20 wait -> replace 0:20 wait with cap, add wait
replace_phase("Tim Wendelboe Aeropress", "RecipePhase(startTimeSeconds: 20, action: PhaseAction.wait)", "RecipePhase(startTimeSeconds: 20, action: PhaseAction.cap)")
insert_phase("Tim Wendelboe Aeropress", "PhaseAction.cap),", "RecipePhase(startTimeSeconds: 25, action: PhaseAction.wait)")

# 2. James Hoffmann Ultimate Aeropress
insert_phase("James Hoffmann Ultimate Aeropress", "PhaseAction.pourCenter),", "RecipePhase(startTimeSeconds: 15, action: PhaseAction.cap),\n      RecipePhase(startTimeSeconds: 25, action: PhaseAction.wait)")

# 3. Inverted Classic
replace_phase("Inverted Classic", "RecipePhase(startTimeSeconds: 90, action: PhaseAction.wait)", "RecipePhase(startTimeSeconds: 40, action: PhaseAction.cap),\n      RecipePhase(startTimeSeconds: 45, action: PhaseAction.wait),\n      RecipePhase(startTimeSeconds: 90, action: PhaseAction.flip)")

# 4. Aeropress Espresso Concentrate
replace_phase("Aeropress Espresso Concentrate", "RecipePhase(startTimeSeconds: 70, action: PhaseAction.wait)", "RecipePhase(startTimeSeconds: 40, action: PhaseAction.cap),\n      RecipePhase(startTimeSeconds: 45, action: PhaseAction.wait),\n      RecipePhase(startTimeSeconds: 70, action: PhaseAction.flip)")

# 5. Aeropress Milk Punch
replace_phase("Aeropress Milk Punch", "RecipePhase(startTimeSeconds: 90, action: PhaseAction.press)", "RecipePhase(startTimeSeconds: 40, action: PhaseAction.cap),\n      RecipePhase(startTimeSeconds: 45, action: PhaseAction.wait),\n      RecipePhase(startTimeSeconds: 90, action: PhaseAction.press)")

# 6. Aeropress Iced Coffee
replace_phase("Aeropress Iced Coffee", "RecipePhase(startTimeSeconds: 60, pourAmountMl: 0, action: PhaseAction.pourCenter)", "RecipePhase(startTimeSeconds: 20, action: PhaseAction.cap),\n      RecipePhase(startTimeSeconds: 25, action: PhaseAction.wait),\n      RecipePhase(startTimeSeconds: 60, action: PhaseAction.press)")

# 7. Aeropress Espresso (Faux-Presso)
replace_phase("Aeropress Espresso (Faux-Presso)", "RecipePhase(startTimeSeconds: 60, pourAmountMl: 0, action: PhaseAction.pourCenter)", "RecipePhase(startTimeSeconds: 20, action: PhaseAction.cap),\n      RecipePhase(startTimeSeconds: 25, action: PhaseAction.wait),\n      RecipePhase(startTimeSeconds: 60, action: PhaseAction.press)")


with open('lib/core/recipe.dart', 'w', encoding='utf-8') as f:
    f.write(text)

print("Added cap and flip to Aeropress recipes.")
