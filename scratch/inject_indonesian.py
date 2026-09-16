import re

with open('lib/core/recipe.dart', 'r', encoding='utf-8') as f:
    text = f.read()

new_recipes = '''
  Recipe(
    name: "Ryan Wibawa WBrC 2024",
    description: "Adaptasi resep Juara 3 World Brewers Cup 2024. Menggunakan 4 fase tuangan yang volumenya mengecil di akhir untuk mencegah ekstraksi berlebih. Menghasilkan rasa yang balance dan syrupy.",
    coffeeGrams: 16, totalWaterMl: 240, totalDurationSeconds: 160,
    method: BrewMethod.v60, targetGrindSizeMicrons: 800, beanType: 'Arabica',
    phases: [
      RecipePhase(startTimeSeconds: 0, pourAmountMl: 50, action: PhaseAction.pourCenter),
      RecipePhase(startTimeSeconds: 40, pourAmountMl: 70, action: PhaseAction.pourCircle),
      RecipePhase(startTimeSeconds: 80, pourAmountMl: 60, action: PhaseAction.pourCircle),
      RecipePhase(startTimeSeconds: 110, pourAmountMl: 60, action: PhaseAction.pourCircle),
    ],
  ),
  Recipe(
    name: "Yoshua Tanu Fast Flow",
    description: "Teknik seduh cepat (2 menit) dari 3x Juara Barista Indonesia. Agitasi kuat dan suhu tinggi (93°C) untuk menonjolkan aroma biji proses eksperimental tanpa berbau earthy.",
    coffeeGrams: 15, totalWaterMl: 225, totalDurationSeconds: 120,
    method: BrewMethod.v60, targetGrindSizeMicrons: 900, beanType: 'Arabica',
    phases: [
      RecipePhase(startTimeSeconds: 0, pourAmountMl: 45, action: PhaseAction.pourCircle),
      RecipePhase(startTimeSeconds: 5, action: PhaseAction.stir),
      RecipePhase(startTimeSeconds: 30, pourAmountMl: 90, action: PhaseAction.pourCircle),
      RecipePhase(startTimeSeconds: 70, pourAmountMl: 90, action: PhaseAction.pourCircle),
      RecipePhase(startTimeSeconds: 80, action: PhaseAction.stir),
    ],
  ),
'''

# Insert before Orea V3
text = text.replace('  Recipe(\n    name: "Orea V3/Kalita Wave"', new_recipes + '  Recipe(\n    name: "Orea V3/Kalita Wave"')

with open('lib/core/recipe.dart', 'w', encoding='utf-8') as f:
    f.write(text)

print("Injected Ryan Wibawa and Yoshua Tanu recipes successfully.")
