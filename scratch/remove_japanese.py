import re

with open('lib/core/recipe.dart', 'r', encoding='utf-8') as f:
    text = f.read()

# Target block to remove
target = r'''  Recipe\(
    name: "Japanese Iced Coffee \(V60\)",
    description: "Menyeduh kopi di atas es batu agar aroma terkunci. Gilingan lebih halus karena air panas dikurangi.",
    coffeeGrams: 20,
    totalWaterMl: 200,
    extraIngredients: "100 gram es batu",
    totalDurationSeconds: 150,
    method: BrewMethod\.v60,
    targetGrindSizeMicrons: 700,
    phases: \[
      RecipePhase\(startTimeSeconds: 0, pourAmountMl: 60, action: PhaseAction\.pourCircle\),
      RecipePhase\(startTimeSeconds: 45, pourAmountMl: 70, action: PhaseAction\.pourCircle\),
      RecipePhase\(startTimeSeconds: 75, pourAmountMl: 70, action: PhaseAction\.pourCenter\),
    \],
  \),\s*'''

new_text = re.sub(target, '', text, flags=re.DOTALL)

with open('lib/core/recipe.dart', 'w', encoding='utf-8') as f:
    f.write(new_text)

print("Removed Japanese Iced Coffee (V60)")
