import re

with open('lib/core/ai_service.dart', 'r', encoding='utf-8') as f:
    text = f.read()

bad_ai_return = """    return Recipe(
      id: currentRecipe?.id, // Preserve ID if editing!
      name: data['name'] as String? ?? (currentRecipe != null ? currentRecipe.name : 'AI Recipe'),
      description: data['description'] as String? ?? '',
      coffeeGrams: (data['coffeeGrams'] as num?)?.toDouble() ?? 15.0,
      totalWaterMl: totalWater,
      totalDurationSeconds: totalDuration,
      phases: phases,
      targetGrindSizeMicrons: data['targetGrindSizeMicrons'] as int? ?? 800,
      extraIngredients: data['extraIngredients'] as String? ?? '',
    );"""

good_ai_return = """    return Recipe(
      id: currentRecipe?.id, // Preserve ID if editing!
      name: data['name'] as String? ?? (currentRecipe != null ? currentRecipe.name : 'AI Recipe'),
      description: data['description'] as String? ?? '',
      coffeeGrams: (data['coffeeGrams'] as num?)?.toDouble() ?? 15.0,
      totalWaterMl: totalWater,
      totalDurationSeconds: totalDuration,
      phases: phases,
      targetGrindSizeMicrons: data['targetGrindSizeMicrons'] as int? ?? 800,
      extraIngredients: data['extraIngredients'] as String? ?? '',
      beanType: data['beanType'] as String? ?? currentRecipe?.beanType ?? 'Arabica',
      method: currentRecipe?.method ?? BrewMethod.v60,
    );"""

text = text.replace(bad_ai_return, good_ai_return)

with open('lib/core/ai_service.dart', 'w', encoding='utf-8') as f:
    f.write(text)

print("Fixed AiService method preservation.")
