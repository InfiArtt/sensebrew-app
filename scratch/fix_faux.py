import re

with open('lib/core/recipe.dart', 'r', encoding='utf-8') as f:
    text = f.read()

# Remove pourAmountMl: 0 from Faux-Presso
text = text.replace(
    'RecipePhase(startTimeSeconds: 60, pourAmountMl: 0, action: PhaseAction.pourCenter)',
    'RecipePhase(startTimeSeconds: 20, action: PhaseAction.cap),\n      RecipePhase(startTimeSeconds: 25, action: PhaseAction.wait),\n      RecipePhase(startTimeSeconds: 60, action: PhaseAction.press)'
)

with open('lib/core/recipe.dart', 'w', encoding='utf-8') as f:
    f.write(text)

print("Fixed Faux-Presso.")
