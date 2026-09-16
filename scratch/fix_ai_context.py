import re

with open('lib/core/ai_service.dart', 'r', encoding='utf-8') as f:
    text = f.read()

old_context = """      contextInfo = "\\nThe user is currently editing a recipe: '${currentRecipe.name}'.\\nCurrent state: ${currentRecipe.coffeeGrams}g coffee, ${currentRecipe.totalWaterMl}ml water.\\nPhases: ${currentRecipe.phases.map((e) => 'At ${e.startTimeSeconds}s: ${e.action.name} ${e.pourAmountMl}ml').join(', ')}\\nPlease modify this recipe based on the user's request.";"""
new_context = """      contextInfo = "\\nThe user is currently editing a recipe: '${currentRecipe.name}'.\\nCurrent Grind Size: ${currentRecipe.targetGrindSizeMicrons} microns.\\nCurrent Extra Ingredients: ${currentRecipe.extraIngredients}\\nCurrent Description: ${currentRecipe.description}\\nCurrent state: ${currentRecipe.coffeeGrams}g coffee, ${currentRecipe.totalWaterMl}ml water.\\nPhases: ${currentRecipe.phases.map((e) => 'At ${e.startTimeSeconds}s: ${e.action.name} ${e.pourAmountMl}ml').join(', ')}\\nPlease modify this recipe based on the user's request, ensuring you preserve or update the flavor profile and ingredients.";"""

if old_context in text:
    text = text.replace(old_context, new_context)
    with open('lib/core/ai_service.dart', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Updated contextInfo to read all elements.")
else:
    print("Could not find old_context.")
