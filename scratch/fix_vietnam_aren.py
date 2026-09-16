import re

with open('lib/core/recipe.dart', 'r', encoding='utf-8') as f:
    text = f.read()

bad_recipe = """  Recipe(
    name: "Vietnam Drip Gula Aren",
    description: "Gilingan medium. Gunakan sirup gula aren di dasar gelas. Seduh perlahan (tetasan 4-5 menit). Aduk rata lalu tambahkan es.\\n\\nEstimasi Rasa: Manis legit aren berpadu dengan pahit kopi, creamy, aroma rempah/karamel.",
    coffeeGrams: 18,
      beanType: "Robusta",
    totalWaterMl: 130,
    extraIngredients: "Sirup Gula Aren (20ml), Es Batu (150g)",
    totalDurationSeconds: 300,
    method: BrewMethod.vietnamDrip,
    targetGrindSizeMicrons: 800,"""

good_recipe = """  Recipe(
    name: "Vietnam Drip Gula Aren",
    description: "Kombinasi klasik Susu Kental Manis (SKM) dan Sirup Gula Aren. SKM memberikan tekstur 'creamy' khas Vietnam Drip, sementara aren memberikan aroma legit karamel. Tuang SKM dan aren di dasar gelas, seduh perlahan, aduk rata lalu tambahkan es.\\n\\nEstimasi Rasa: Sangat creamy, manis legit aren berpadu dengan rasa kopi yang kuat dan tebal.",
    coffeeGrams: 18,
      beanType: "Robusta",
    totalWaterMl: 130,
    extraIngredients: "Susu Kental Manis (15-20ml), Sirup Gula Aren (10-15ml), Es Batu",
    totalDurationSeconds: 300,
    method: BrewMethod.vietnamDrip,
    targetGrindSizeMicrons: 800,"""

if bad_recipe in text:
    text = text.replace(bad_recipe, good_recipe)
    print("Replaced Vietnam Drip Gula Aren recipe")
else:
    print("Could not find the target recipe text")

with open('lib/core/recipe.dart', 'w', encoding='utf-8') as f:
    f.write(text)
