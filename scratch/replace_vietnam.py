import re

with open('lib/core/recipe.dart', 'r', encoding='utf-8') as f:
    code = f.read()

target_egg = '''    Recipe(
      name: "Egg Coffee (Ca Phe Trung)",
      description: "Kopi telur khas Hanoi. Tuangkan kopi tetes ini ke dalam gelas berisi krim kuning telur kocok.",
      coffeeGrams: 20,
      totalWaterMl: 100,
      totalDurationSeconds: 480,
      targetGrindSizeMicrons: 800,
      extraIngredients: "1 kuning telur, 15 ml susu kental manis",
      phases: [
        RecipePhase(startTimeSeconds: 0, pourAmountMl: 20, action: PhaseAction.pourCenter),
        RecipePhase(startTimeSeconds: 30, pourAmountMl: 80, action: PhaseAction.pourCenter),
        RecipePhase(startTimeSeconds: 480, action: PhaseAction.wait),
      ],
    ),'''

replacement_egg = '''    Recipe(
      name: "Vietnam Drip (Kopi Hitam)",
      description: "Ca Phe Da. Kopi tetes hitam pekat tanpa susu kental manis, sangat nikmat disajikan dengan es batu.",
      coffeeGrams: 20,
      totalWaterMl: 120,
      totalDurationSeconds: 480,
      targetGrindSizeMicrons: 800,
      extraIngredients: "100 gram es batu",
      phases: [
        RecipePhase(startTimeSeconds: 0, pourAmountMl: 20, action: PhaseAction.pourCenter),
        RecipePhase(startTimeSeconds: 30, pourAmountMl: 100, action: PhaseAction.pourCenter),
        RecipePhase(startTimeSeconds: 480, action: PhaseAction.wait),
      ],
    ),'''

target_salt = '''    Recipe(
      name: "Salted Coffee (Ca Phe Muoi)",
      description: "Kopi garam gaya Vietnam Tengah. Rasa manis, asin, dan pahit menyatu indah.",
      coffeeGrams: 15,
      totalWaterMl: 100,
      totalDurationSeconds: 480,
      targetGrindSizeMicrons: 800,
      extraIngredients: "15 ml susu kental manis, sejumpit garam",
      phases: [
        RecipePhase(startTimeSeconds: 0, pourAmountMl: 20, action: PhaseAction.pourCenter),
        RecipePhase(startTimeSeconds: 30, pourAmountMl: 80, action: PhaseAction.pourCenter),
        RecipePhase(startTimeSeconds: 480, action: PhaseAction.wait),
      ],
    ),'''

replacement_salt = '''    Recipe(
      name: "Vietnam Drip (Kopi Susu Panas)",
      description: "Ca Phe Sua Nong. Resep klasik kopi susu Vietnam tetes pelan tanpa es batu.",
      coffeeGrams: 15,
      totalWaterMl: 100,
      totalDurationSeconds: 480,
      targetGrindSizeMicrons: 800,
      extraIngredients: "20 ml susu kental manis",
      phases: [
        RecipePhase(startTimeSeconds: 0, pourAmountMl: 20, action: PhaseAction.pourCenter),
        RecipePhase(startTimeSeconds: 30, pourAmountMl: 80, action: PhaseAction.pourCenter),
        RecipePhase(startTimeSeconds: 480, action: PhaseAction.wait),
      ],
    ),'''

code = code.replace(target_egg, replacement_egg)
code = code.replace(target_salt, replacement_salt)

with open('lib/core/recipe.dart', 'w', encoding='utf-8') as f:
    f.write(code)

print('Vietnam recipes replaced.')
