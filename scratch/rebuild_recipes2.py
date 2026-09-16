import re

with open('backup_recipe.dart', 'r', encoding='utf-16') as f:
    text = f.read()

# 1. Remove PhaseAction.pourFast from Enum
text = text.replace('pourFast,   // Pour directly/fast, no metronome\n', '')
text = text.replace('pourFast, // Pour directly/fast, no metronome\n', '')
text = text.replace('pourFast,', '')
text = text.replace('PhaseAction.pourFast', 'PhaseAction.pourCenter')

# 2. Extract database
pre_db, rest = text.split('List<Recipe> recipeDatabase = [')
db_str, post_db = rest.split('];\n', 1)

# Split recipes
recipe_texts = db_str.split('\n  Recipe(')
recipes = []
for r in recipe_texts[1:]:
    if r.strip():
        recipes.append('  Recipe(' + r)

# 3. Clean and filter recipes
filtered_recipes = []
for r in recipes:
    # Skip cold brew
    if 'BrewMethod.coldBrew' in r:
        continue
    
    name_match = re.search(r'name:\s*"([^"]+)"', r)
    name = name_match.group(1) if name_match else ""
    
    # Process old recipes
    if name == "James Hoffmann Ultimate V60":
        # Fix description and phases to match 3-pour reality
        r = re.sub(r'description:\s*"[^"]+"', 'description: "Resep andalan James Hoffmann. 3 fase tuangan (bloom dan 2 tuangan utama). Menghasilkan ekstraksi merata untuk kopi light roast."', r)
        # Update phases
        r = re.sub(r'phases:\s*\[.*?\]\s*,', '''phases: [
      RecipePhase(startTimeSeconds: 0, pourAmountMl: 50, action: PhaseAction.pourCenter),
      RecipePhase(startTimeSeconds: 10, action: PhaseAction.stir),
      RecipePhase(startTimeSeconds: 45, pourAmountMl: 100, action: PhaseAction.pourCircle),
      RecipePhase(startTimeSeconds: 75, pourAmountMl: 100, action: PhaseAction.pourCircle),
      RecipePhase(startTimeSeconds: 105, action: PhaseAction.stir),
    ],''', r, flags=re.DOTALL)
    
    elif name == "Tetsu Kasuya 4-6 Method":
        r = re.sub(r'description:\s*"[^"]+"', 'description: "Metode 4-6 membagi air seduhan menjadi 40% (untuk keseimbangan asam/manis) dan 60% (untuk kekuatan rasa). Terdiri dari 5 fase tuangan berjarak 45 detik."', r)
    elif name == "Lance Hedrick V60":
        # Skip the old Lance Hedrick V60 to make room for Japanese
        continue
    elif name == "Osmotic Flow":
        r = re.sub(r'description:\s*"[^"]+"', 'description: "Teknik berfokus pada aliran lambat di tengah (center) untuk menjaga bentuk kubah bubuk kopi. Menonjolkan rasa manis dengan sedikit agitasi."', r)
    elif name == "April Pour-Over":
        r = re.sub(r'description:\s*"[^"]+"', 'description: "Resep khas April Coffee (Patrik Rolf). Mengandalkan suhu air lebih rendah dan penuangan circle untuk kejelasan rasa."', r)
    elif name == "Scott Rao V60":
        r = re.sub(r'description:\s*"[^"]+"', 'description: "Fokus pada agitasi (putaran/swirl) yang efisien untuk mencegah channeling dan meratakan ekstraksi."', r)
    
    filtered_recipes.append(r)

# 4. Add Japanese Iced Coffee variants
japanese_1 = '''  Recipe(
    name: "Japanese Iced Coffee (Fruity)",
    description: "Resep es kopi Jepang yang memfokuskan ekstraksi cepat di awal untuk menonjolkan rasa buah (fruity). (Catatan: 100g air diganti es batu di server).",
    coffeeGrams: 15, totalWaterMl: 150, totalDurationSeconds: 150,
    method: BrewMethod.v60, targetGrindSizeMicrons: 700, beanType: 'Arabica',
    phases: [
      RecipePhase(startTimeSeconds: 0, pourAmountMl: 50, action: PhaseAction.pourCenter),
      RecipePhase(startTimeSeconds: 40, pourAmountMl: 100, action: PhaseAction.pourCircle),
    ],
  ),'''
japanese_2 = '''  Recipe(
    name: "Japanese Iced Coffee (Sweet)",
    description: "Seduhan es kopi Jepang dengan tuangan lebih perlahan. Mengekstrak lebih banyak rasa manis dan karamel. (Catatan: 100g air diganti es batu).",
    coffeeGrams: 15, totalWaterMl: 150, totalDurationSeconds: 180,
    method: BrewMethod.v60, targetGrindSizeMicrons: 750, beanType: 'Arabica',
    phases: [
      RecipePhase(startTimeSeconds: 0, pourAmountMl: 40, action: PhaseAction.pourCenter),
      RecipePhase(startTimeSeconds: 45, pourAmountMl: 55, action: PhaseAction.pourCircle),
      RecipePhase(startTimeSeconds: 90, pourAmountMl: 55, action: PhaseAction.pourCircle),
    ],
  ),'''
filtered_recipes.extend([japanese_1, japanese_2])

# 5. Bring in SOME new recipes from yesterday, replacing pourFast -> pourCenter, and omitting duplicate James/Lance
new_recipes_str = """
  Recipe(
    name: "Orea V3/Kalita Wave",
    description: "Tuangan konsisten untuk dripper datar (flat bed). Menyoroti acidity dan kebersihan rasa.",
    coffeeGrams: 15, totalWaterMl: 250, totalDurationSeconds: 150,
    method: BrewMethod.v60, targetGrindSizeMicrons: 800, beanType: 'Arabica',
    phases: [
      RecipePhase(startTimeSeconds: 0, pourAmountMl: 50, action: PhaseAction.pourCenter),
      RecipePhase(startTimeSeconds: 40, pourAmountMl: 100, action: PhaseAction.pourCenter),
      RecipePhase(startTimeSeconds: 80, pourAmountMl: 100, action: PhaseAction.pourCenter),
    ],
  ),
  Recipe(
    name: "V60 Dark Roast (Low Temp)",
    description: "Gunakan air suhu 85C dan tuangan cepat di tengah untuk menghindari rasa gosong dan pahit berlebih pada biji sangrai gelap.",
    coffeeGrams: 15, totalWaterMl: 250, totalDurationSeconds: 140,
    method: BrewMethod.v60, targetGrindSizeMicrons: 900, beanType: 'Blend',
    phases: [
      RecipePhase(startTimeSeconds: 0, pourAmountMl: 50, action: PhaseAction.pourCenter),
      RecipePhase(startTimeSeconds: 45, pourAmountMl: 100, action: PhaseAction.pourCenter),
      RecipePhase(startTimeSeconds: 85, pourAmountMl: 100, action: PhaseAction.pourCenter),
    ],
  ),
  Recipe(
    name: "Kasuya Devil Recipe (Switch)",
    description: "God Recipe V60 Switch. Menggunakan air biasa untuk bloom, lalu air mendidih setelahnya, dicampur dengan imersi.",
    coffeeGrams: 20, totalWaterMl: 280, totalDurationSeconds: 200,
    method: BrewMethod.v60, targetGrindSizeMicrons: 850, beanType: 'Arabica',
    phases: [
      RecipePhase(startTimeSeconds: 0, action: PhaseAction.openValve),
      RecipePhase(startTimeSeconds: 2, pourAmountMl: 60, action: PhaseAction.pourCenter),
      RecipePhase(startTimeSeconds: 40, action: PhaseAction.closeValve),
      RecipePhase(startTimeSeconds: 42, pourAmountMl: 120, action: PhaseAction.pourCenter),
      RecipePhase(startTimeSeconds: 80, pourAmountMl: 100, action: PhaseAction.pourCircle),
      RecipePhase(startTimeSeconds: 120, action: PhaseAction.openValve),
    ],
  ),
  Recipe(
    name: "W.A.C Carolina Ibarra (2018)",
    description: "Resep juara dunia Aeropress 2018. Posisi inverted, aduk kuat, hasilkan ekstraksi yang super fruity.",
    coffeeGrams: 35, totalWaterMl: 100, totalDurationSeconds: 90,
    method: BrewMethod.aeropress, targetGrindSizeMicrons: 800, beanType: 'Arabica',
    phases: [
      RecipePhase(startTimeSeconds: 0, pourAmountMl: 100, action: PhaseAction.pourCenter),
      RecipePhase(startTimeSeconds: 30, action: PhaseAction.stir),
      RecipePhase(startTimeSeconds: 60, action: PhaseAction.press),
    ],
  ),
  Recipe(
    name: "W.A.C Paulina Miczka (2017)",
    description: "Resep juara 2017. Rasio 1:5 pekat di awal, ditambah air bypass di akhir. Inverted.",
    coffeeGrams: 35, totalWaterMl: 150, totalDurationSeconds: 105,
    method: BrewMethod.aeropress, targetGrindSizeMicrons: 850, beanType: 'Arabica',
    phases: [
      RecipePhase(startTimeSeconds: 0, pourAmountMl: 150, action: PhaseAction.pourCenter),
      RecipePhase(startTimeSeconds: 15, action: PhaseAction.stir),
      RecipePhase(startTimeSeconds: 35, action: PhaseAction.stir),
      RecipePhase(startTimeSeconds: 75, action: PhaseAction.press),
    ],
  ),
  Recipe(
    name: "Tuomas Merikanto W.A.C",
    description: "Aeropress standar (tidak inverted). Air 80C, biarkan menetes perlahan lalu press sangat lambat.",
    coffeeGrams: 18, totalWaterMl: 200, totalDurationSeconds: 150,
    method: BrewMethod.aeropress, targetGrindSizeMicrons: 750, beanType: 'Arabica',
    phases: [
      RecipePhase(startTimeSeconds: 0, pourAmountMl: 50, action: PhaseAction.pourCenter),
      RecipePhase(startTimeSeconds: 10, action: PhaseAction.stir),
      RecipePhase(startTimeSeconds: 45, pourAmountMl: 150, action: PhaseAction.pourCenter),
      RecipePhase(startTimeSeconds: 90, action: PhaseAction.press),
    ],
  ),
  Recipe(
    name: "Aeropress Flow Control",
    description: "Menggunakan cap Prismo atau Flow Control. Imersi penuh tanpa inverted.",
    coffeeGrams: 18, totalWaterMl: 250, totalDurationSeconds: 150,
    method: BrewMethod.aeropress, targetGrindSizeMicrons: 700, beanType: 'Arabica',
    phases: [
      RecipePhase(startTimeSeconds: 0, pourAmountMl: 250, action: PhaseAction.pourCenter),
      RecipePhase(startTimeSeconds: 30, action: PhaseAction.stir),
      RecipePhase(startTimeSeconds: 120, action: PhaseAction.press),
    ],
  ),
  Recipe(
    name: "Aeropress Espresso Fake",
    description: "Ekstraksi konsentrat tinggi yang menyerupai espresso. Gunakan Prismo/Flow Control dan gilingan espresso.",
    coffeeGrams: 20, totalWaterMl: 60, totalDurationSeconds: 90,
    method: BrewMethod.aeropress, targetGrindSizeMicrons: 300, beanType: 'Blend',
    phases: [
      RecipePhase(startTimeSeconds: 0, pourAmountMl: 60, action: PhaseAction.pourCenter),
      RecipePhase(startTimeSeconds: 20, action: PhaseAction.stir),
      RecipePhase(startTimeSeconds: 60, action: PhaseAction.press),
    ],
  ),
  Recipe(
    name: "Aeropress Tea-like Extract",
    description: "Rasio renggang dan gilingan kasar untuk rasa kopi yang mirip teh dan menyegarkan.",
    coffeeGrams: 12, totalWaterMl: 250, totalDurationSeconds: 180,
    method: BrewMethod.aeropress, targetGrindSizeMicrons: 1000, beanType: 'Arabica',
    phases: [
      RecipePhase(startTimeSeconds: 0, pourAmountMl: 250, action: PhaseAction.pourCenter),
      RecipePhase(startTimeSeconds: 150, action: PhaseAction.press),
    ],
  ),
  Recipe(
    name: "Aeropress Robusta Sweet",
    description: "Khusus untuk kopi Robusta. Ekstraksi singkat dengan suhu 85C agar tidak terlalu pahit.",
    coffeeGrams: 15, totalWaterMl: 200, totalDurationSeconds: 120,
    method: BrewMethod.aeropress, targetGrindSizeMicrons: 700, beanType: 'Robusta',
    phases: [
      RecipePhase(startTimeSeconds: 0, pourAmountMl: 200, action: PhaseAction.pourCenter),
      RecipePhase(startTimeSeconds: 30, action: PhaseAction.stir),
      RecipePhase(startTimeSeconds: 90, action: PhaseAction.press),
    ],
  ),
  Recipe(
    name: "Ca Phe Muoi (Salted Coffee)",
    description: "Kopi Vietnam dengan buih krim asin (whip cream + garam). Campurkan kopi dengan krim setelah menetes selesai.",
    coffeeGrams: 20, totalWaterMl: 100, totalDurationSeconds: 300,
    method: BrewMethod.vietnamDrip, targetGrindSizeMicrons: 650, beanType: 'Robusta',
    phases: [
      RecipePhase(startTimeSeconds: 0, pourAmountMl: 20, action: PhaseAction.pourCenter),
      RecipePhase(startTimeSeconds: 30, pourAmountMl: 80, action: PhaseAction.pourCenter),
    ],
  ),
  Recipe(
    name: "Ca Phe Trung (Egg Coffee)",
    description: "Kopi pekat yang dicampur dengan kuning telur yang dikocok bersama susu kental manis hingga mengembang.",
    coffeeGrams: 20, totalWaterMl: 80, totalDurationSeconds: 300,
    method: BrewMethod.vietnamDrip, targetGrindSizeMicrons: 650, beanType: 'Robusta',
    phases: [
      RecipePhase(startTimeSeconds: 0, pourAmountMl: 20, action: PhaseAction.pourCenter),
      RecipePhase(startTimeSeconds: 45, pourAmountMl: 60, action: PhaseAction.pourCenter),
    ],
  ),
  Recipe(
    name: "Ca Phe Sua Chua (Yogurt Coffee)",
    description: "Kombinasi asam segar dari Yogurt dan pahitnya Robusta. Kopi diteteskan ke atas es dan yogurt.",
    coffeeGrams: 15, totalWaterMl: 100, totalDurationSeconds: 240,
    method: BrewMethod.vietnamDrip, targetGrindSizeMicrons: 700, beanType: 'Robusta',
    phases: [
      RecipePhase(startTimeSeconds: 0, pourAmountMl: 20, action: PhaseAction.pourCenter),
      RecipePhase(startTimeSeconds: 30, pourAmountMl: 80, action: PhaseAction.pourCenter),
    ],
  ),
  Recipe(
    name: "Phin Arabica Light",
    description: "Vietnam Drip khusus untuk biji Arabica. Sedikit dipadatkan, suhu 92C untuk body tebal nan fruity.",
    coffeeGrams: 15, totalWaterMl: 120, totalDurationSeconds: 240,
    method: BrewMethod.vietnamDrip, targetGrindSizeMicrons: 800, beanType: 'Arabica',
    phases: [
      RecipePhase(startTimeSeconds: 0, pourAmountMl: 30, action: PhaseAction.pourCenter),
      RecipePhase(startTimeSeconds: 45, pourAmountMl: 90, action: PhaseAction.pourCenter),
    ],
  ),
  Recipe(
    name: "Vietnam Drip Mocha",
    description: "Tambahkan cokelat bubuk ke dalam susu kental manis sebelum ditetesi kopi.",
    coffeeGrams: 15, totalWaterMl: 100, totalDurationSeconds: 300,
    method: BrewMethod.vietnamDrip, targetGrindSizeMicrons: 700, beanType: 'Blend',
    phases: [
      RecipePhase(startTimeSeconds: 0, pourAmountMl: 20, action: PhaseAction.pourCenter),
      RecipePhase(startTimeSeconds: 30, pourAmountMl: 80, action: PhaseAction.pourCenter),
    ],
  ),
  Recipe(
    name: "Phin Coconut (Bac Xiu)",
    description: "Bac Xiu adalah varian Vietnam Drip dengan rasio susu (dan santan/susu kelapa) yang jauh lebih banyak dari kopinya.",
    coffeeGrams: 15, totalWaterMl: 80, totalDurationSeconds: 300,
    method: BrewMethod.vietnamDrip, targetGrindSizeMicrons: 700, beanType: 'Robusta',
    phases: [
      RecipePhase(startTimeSeconds: 0, pourAmountMl: 20, action: PhaseAction.pourCenter),
      RecipePhase(startTimeSeconds: 45, pourAmountMl: 60, action: PhaseAction.pourCenter),
    ],
  )
"""
filtered_recipes.extend([r for r in new_recipes_str.split('\n  Recipe(')[1:] if r.strip()])

# Prepare final output
final_db_str = "const List<Recipe> recipeDatabase = [\n" + ",\n  Recipe(".join(filtered_recipes) + "];\n"

# Note: filtered_recipes already have "  Recipe(" stripped from the beginning by the split, 
# wait, my loop did `recipes.append('  Recipe(' + r)`, so they ALREADY start with "  Recipe(".
# Ah, the join should just be ',\n'.
final_db_str = "List<Recipe> recipeDatabase = [\n" + ",\n".join(filtered_recipes).replace(',,', ',') + "\n];\n"

final_text = pre_db + final_db_str + post_db

with open('lib/core/recipe.dart', 'w', encoding='utf-8') as f:
    f.write(final_text)

print("Rebuilt recipe.dart successfully.")
