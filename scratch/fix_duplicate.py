import re

with open('lib/core/recipe.dart', 'r', encoding='utf-8') as f:
    text = f.read()

bad_str = """    method: BrewMethod.vietnamDrip,
    extraIngredients: "Santan/Krim Kelapa (30ml), SKM (15g), Es Batu (100g)",
    targetGrindSizeMicrons: 700,
    beanType: 'Robusta',
    extraIngredients: "40 ml susu kental manis, 60 ml santan cair (atau susu kelapa), 100 gram es batu. (Campur semua di gelas penampung)",
    phases: ["""

good_str = """    method: BrewMethod.vietnamDrip,
    targetGrindSizeMicrons: 700,
    beanType: 'Robusta',
    extraIngredients: "40 ml susu kental manis, 60 ml santan cair (atau susu kelapa), 100 gram es batu. (Campur semua di gelas penampung)",
    phases: ["""

text = text.replace(bad_str, good_str)

with open('lib/core/recipe.dart', 'w', encoding='utf-8') as f:
    f.write(text)

print("Fixed duplicate extraIngredients in recipe.dart.")
