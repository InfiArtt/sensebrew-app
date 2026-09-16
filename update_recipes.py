import re

def update_recipes():
    with open('lib/core/recipe.dart', 'r', encoding='utf-8') as f:
        content = f.read()
    
    parts = content.split('List<Recipe> recipeDatabase = [')
    header = parts[0]
    
    recipes = """List<Recipe> recipeDatabase = [
  // ====================================
  // V60 & POUR-OVER RECIPES (Total 10)
  // ====================================
  Recipe(
    name: "James Hoffmann Ultimate V60",
    description: "Resep andalan James Hoffmann. 5 fase tuangan presisi untuk V60.",
    coffeeGrams: 15.0,
    totalWaterMl: 250.0,
    totalDurationSeconds: 210,
    method: BrewMethod.v60,
    targetGrindSizeMicrons: 800,
    phases: [
      RecipePhase(startTimeSeconds: 0, pourAmountMl: 50.0, action: PhaseAction.pourCircle),
      RecipePhase(startTimeSeconds: 10, action: PhaseAction.stir),
      RecipePhase(startTimeSeconds: 15, action: PhaseAction.wait),
      RecipePhase(startTimeSeconds: 45, pourAmountMl: 100.0, action: PhaseAction.pourCircle),
      RecipePhase(startTimeSeconds: 75, pourAmountMl: 100.0, action: PhaseAction.pourCircle),
      RecipePhase(startTimeSeconds: 95, action: PhaseAction.stir),
      RecipePhase(startTimeSeconds: 100, action: PhaseAction.wait),
    ],
  ),
  Recipe(
    name: "Tetsu Kasuya 4-6 Method",
    description: "desc_kasuya",
    coffeeGrams: 20.0,
    totalWaterMl: 300.0,
    totalDurationSeconds: 210,
    method: BrewMethod.v60,
    targetGrindSizeMicrons: 1100,
    phases: [
      RecipePhase(startTimeSeconds: 0, pourAmountMl: 50.0, action: PhaseAction.pourCircle),
      RecipePhase(startTimeSeconds: 45, pourAmountMl: 70.0, action: PhaseAction.pourCircle),
      RecipePhase(startTimeSeconds: 90, pourAmountMl: 60.0, action: PhaseAction.pourCircle),
      RecipePhase(startTimeSeconds: 135, pourAmountMl: 60.0, action: PhaseAction.pourCircle),
      RecipePhase(startTimeSeconds: 180, pourAmountMl: 60.0, action: PhaseAction.pourCircle),
    ],
  ),
  Recipe(
    name: "Lance Hedrick V60",
    description: "desc_lance",
    coffeeGrams: 15.0,
    totalWaterMl: 250.0,
    totalDurationSeconds: 150,
    method: BrewMethod.v60,
    targetGrindSizeMicrons: 850,
    phases: [
      RecipePhase(startTimeSeconds: 0, pourAmountMl: 50.0, action: PhaseAction.pourCircle),
      RecipePhase(startTimeSeconds: 45, pourAmountMl: 200.0, action: PhaseAction.pourCircle),
    ],
  ),
  Recipe(
    name: "Osmotic Flow",
    description: "desc_osmotic",
    coffeeGrams: 20.0,
    totalWaterMl: 300.0,
    totalDurationSeconds: 180,
    method: BrewMethod.v60,
    targetGrindSizeMicrons: 750,
    phases: [
      RecipePhase(startTimeSeconds: 0, pourAmountMl: 30.0, action: PhaseAction.pourCenter),
      RecipePhase(startTimeSeconds: 30, pourAmountMl: 90.0, action: PhaseAction.pourCenter),
      RecipePhase(startTimeSeconds: 60, pourAmountMl: 60.0, action: PhaseAction.pourCenter),
      RecipePhase(startTimeSeconds: 90, pourAmountMl: 60.0, action: PhaseAction.pourCenter),
      RecipePhase(startTimeSeconds: 120, pourAmountMl: 60.0, action: PhaseAction.pourCenter),
    ],
  ),
  Recipe(
    name: "April Pour-Over",
    description: "desc_april",
    coffeeGrams: 13.0,
    totalWaterMl: 200.0,
    totalDurationSeconds: 150,
    method: BrewMethod.v60,
    targetGrindSizeMicrons: 900,
    phases: [
      RecipePhase(startTimeSeconds: 0, pourAmountMl: 30.0, action: PhaseAction.pourCircle),
      RecipePhase(startTimeSeconds: 5, pourAmountMl: 70.0, action: PhaseAction.pourCenter),
      RecipePhase(startTimeSeconds: 35, pourAmountMl: 30.0, action: PhaseAction.pourCircle),
      RecipePhase(startTimeSeconds: 40, pourAmountMl: 70.0, action: PhaseAction.pourCenter),
    ],
  ),
  Recipe(
    name: "Scott Rao V60",
    description: "desc_rao",
    coffeeGrams: 20.0,
    totalWaterMl: 300.0,
    totalDurationSeconds: 180,
    method: BrewMethod.v60,
    targetGrindSizeMicrons: 800,
    phases: [
      RecipePhase(startTimeSeconds: 0, pourAmountMl: 60.0, action: PhaseAction.pourCircle),
      RecipePhase(startTimeSeconds: 5, action: PhaseAction.stir),
      RecipePhase(startTimeSeconds: 10, action: PhaseAction.wait),
      RecipePhase(startTimeSeconds: 45, pourAmountMl: 240.0, action: PhaseAction.pourCircle),
      RecipePhase(startTimeSeconds: 90, action: PhaseAction.stir),
      RecipePhase(startTimeSeconds: 95, action: PhaseAction.wait),
    ],
  ),
  Recipe(
    name: "Hario Official V60",
    description: "Resep standar dari Hario. Mudah dan seimbang.",
    coffeeGrams: 12.0,
    totalWaterMl: 120.0,
    totalDurationSeconds: 120,
    method: BrewMethod.v60,
    targetGrindSizeMicrons: 700,
    phases: [
      RecipePhase(startTimeSeconds: 0, pourAmountMl: 30.0, action: PhaseAction.pourCircle),
      RecipePhase(startTimeSeconds: 30, pourAmountMl: 90.0, action: PhaseAction.pourCircle),
    ],
  ),
  Recipe(
    name: "Japanese Iced Coffee (V60)",
    description: "Siapkan 100g es batu di dalam server. Menyeduh kopi di atas es batu agar aroma terkunci. Gilingan lebih halus karena air panas dikurangi.",
    coffeeGrams: 20.0,
    totalWaterMl: 200.0,
    totalDurationSeconds: 150,
    method: BrewMethod.v60,
    targetGrindSizeMicrons: 700,
    phases: [
      RecipePhase(startTimeSeconds: 0, pourAmountMl: 60.0, action: PhaseAction.pourCircle),
      RecipePhase(startTimeSeconds: 45, pourAmountMl: 70.0, action: PhaseAction.pourCircle),
      RecipePhase(startTimeSeconds: 75, pourAmountMl: 70.0, action: PhaseAction.pourCenter),
    ],
  ),
  Recipe(
    name: "Hario Switch (Tetsu Kasuya)",
    description: "God Recipe ala Tetsu Kasuya. Perkolasi di fase pertama untuk kejernihan rasa, ditutup imersi di akhir untuk body.",
    coffeeGrams: 20.0,
    totalWaterMl: 300.0,
    totalDurationSeconds: 120,
    method: BrewMethod.v60,
    targetGrindSizeMicrons: 800,
    phases: [
      RecipePhase(startTimeSeconds: 0, action: PhaseAction.openValve),
      RecipePhase(startTimeSeconds: 1, pourAmountMl: 150.0, action: PhaseAction.pourCircle),
      RecipePhase(startTimeSeconds: 75, action: PhaseAction.closeValve),
      RecipePhase(startTimeSeconds: 76, pourAmountMl: 150.0, action: PhaseAction.pourCircle),
      RecipePhase(startTimeSeconds: 120, action: PhaseAction.openValve),
    ],
  ),
  Recipe(
    name: "Clever Dripper / Full Immersion",
    description: "Full immersion seduhan aman anti gagal. Tutup keran, tuang air, aduk, dan buka di akhir.",
    coffeeGrams: 15.0,
    totalWaterMl: 250.0,
    totalDurationSeconds: 150,
    method: BrewMethod.v60,
    targetGrindSizeMicrons: 850,
    phases: [
      RecipePhase(startTimeSeconds: 0, action: PhaseAction.closeValve),
      RecipePhase(startTimeSeconds: 1, pourAmountMl: 250.0, action: PhaseAction.pourCenter),
      RecipePhase(startTimeSeconds: 120, action: PhaseAction.stir),
      RecipePhase(startTimeSeconds: 150, action: PhaseAction.openValve),
    ],
  ),

  // ====================================
  // FRENCH PRESS RECIPES (Total 5)
  // ====================================
  Recipe(
    name: "James Hoffmann French Press",
    description: "Giling medium, tunggu 4 menit, hancurkan kerak, buang busa, tunggu 5 menit lagi sebelum ditekan.",
    coffeeGrams: 30.0,
    totalWaterMl: 500.0,
    totalDurationSeconds: 540,
    method: BrewMethod.frenchPress,
    targetGrindSizeMicrons: 900,
    phases: [
      RecipePhase(startTimeSeconds: 0, pourAmountMl: 500.0, action: PhaseAction.pourCenter),
      RecipePhase(startTimeSeconds: 240, action: PhaseAction.stir),
      RecipePhase(startTimeSeconds: 250, action: PhaseAction.wait),
      RecipePhase(startTimeSeconds: 540, action: PhaseAction.press),
    ],
  ),
  Recipe(
    name: "Traditional French Press",
    description: "Resep klasik 4 menit. Gilingan murni kasar, langsung ditekan setelah selesai.",
    coffeeGrams: 30.0,
    totalWaterMl: 500.0,
    totalDurationSeconds: 240,
    method: BrewMethod.frenchPress,
    targetGrindSizeMicrons: 1100,
    phases: [
      RecipePhase(startTimeSeconds: 0, pourAmountMl: 500.0, action: PhaseAction.pourCenter),
      RecipePhase(startTimeSeconds: 60, action: PhaseAction.stir),
      RecipePhase(startTimeSeconds: 240, action: PhaseAction.press),
    ],
  ),
  Recipe(
    name: "Cafe au Lait (Strong French Press)",
    description: "Rasio sangat ketat (1:10) untuk hasil pekat, didesain untuk dituang dengan susu panas.",
    coffeeGrams: 30.0,
    totalWaterMl: 300.0,
    totalDurationSeconds: 240,
    method: BrewMethod.frenchPress,
    targetGrindSizeMicrons: 1000,
    phases: [
      RecipePhase(startTimeSeconds: 0, pourAmountMl: 300.0, action: PhaseAction.pourCenter),
      RecipePhase(startTimeSeconds: 60, action: PhaseAction.stir),
      RecipePhase(startTimeSeconds: 240, action: PhaseAction.press),
    ],
  ),
  Recipe(
    name: "Lance Hedrick French Press",
    description: "Gilingan sedang-halus. Diamkan 5 menit, dan tekan plunger HANYA menyentuh permukaan air (tidak sampai bawah) agar ampas tertahan.",
    coffeeGrams: 30.0,
    totalWaterMl: 500.0,
    totalDurationSeconds: 300,
    method: BrewMethod.frenchPress,
    targetGrindSizeMicrons: 800,
    phases: [
      RecipePhase(startTimeSeconds: 0, pourAmountMl: 500.0, action: PhaseAction.pourCenter),
      RecipePhase(startTimeSeconds: 300, action: PhaseAction.press),
    ],
  ),
  Recipe(
    name: "Slayer French Press (Skim Early)",
    description: "Aduk kuat di awal dan langsung buang busa di menit pertama agar ekstraksi merata sejak awal.",
    coffeeGrams: 30.0,
    totalWaterMl: 500.0,
    totalDurationSeconds: 240,
    method: BrewMethod.frenchPress,
    targetGrindSizeMicrons: 950,
    phases: [
      RecipePhase(startTimeSeconds: 0, pourAmountMl: 500.0, action: PhaseAction.pourCenter),
      RecipePhase(startTimeSeconds: 60, action: PhaseAction.stir),
      RecipePhase(startTimeSeconds: 70, action: PhaseAction.wait), // Skim
      RecipePhase(startTimeSeconds: 240, action: PhaseAction.press),
    ],
  ),

  // ====================================
  // AEROPRESS RECIPES (Total 5)
  // ====================================
  Recipe(
    name: "Alan Adler (Original)",
    description: "Posisi standar. Gilingan halus. Aduk 10 detik, tekan perlahan.",
    coffeeGrams: 15.0,
    totalWaterMl: 200.0,
    totalDurationSeconds: 90,
    method: BrewMethod.aeropress,
    targetGrindSizeMicrons: 500,
    phases: [
      RecipePhase(startTimeSeconds: 0, pourAmountMl: 200.0, action: PhaseAction.pourCenter),
      RecipePhase(startTimeSeconds: 15, action: PhaseAction.stir),
      RecipePhase(startTimeSeconds: 25, action: PhaseAction.press),
    ],
  ),
  Recipe(
    name: "Tim Wendelboe Aeropress",
    description: "Posisi standar. Tuang semua, aduk kuat 3 kali, diamkan, lalu tekan setelah 1 menit.",
    coffeeGrams: 14.0,
    totalWaterMl: 200.0,
    totalDurationSeconds: 80,
    method: BrewMethod.aeropress,
    targetGrindSizeMicrons: 700,
    phases: [
      RecipePhase(startTimeSeconds: 0, pourAmountMl: 200.0, action: PhaseAction.pourCenter),
      RecipePhase(startTimeSeconds: 15, action: PhaseAction.stir),
      RecipePhase(startTimeSeconds: 20, action: PhaseAction.wait),
      RecipePhase(startTimeSeconds: 60, action: PhaseAction.press),
    ],
  ),
  Recipe(
    name: "James Hoffmann Ultimate Aeropress",
    description: "Lebih hemat kopi. Posisi standar. Seduh 2 menit, putar sedikit (swirl), diamkan 30 detik, lalu tekan perlahan.",
    coffeeGrams: 11.0,
    totalWaterMl: 200.0,
    totalDurationSeconds: 150,
    method: BrewMethod.aeropress,
    targetGrindSizeMicrons: 650,
    phases: [
      RecipePhase(startTimeSeconds: 0, pourAmountMl: 200.0, action: PhaseAction.pourCenter),
      RecipePhase(startTimeSeconds: 120, action: PhaseAction.stir),
      RecipePhase(startTimeSeconds: 125, action: PhaseAction.wait),
      RecipePhase(startTimeSeconds: 150, action: PhaseAction.press),
    ],
  ),
  Recipe(
    name: "Inverted Classic",
    description: "Posisi terbalik (Inverted). Aduk kuat, diamkan. Di menit 1:30, balikkan alat perlahan dan tekan.",
    coffeeGrams: 15.0,
    totalWaterMl: 200.0,
    totalDurationSeconds: 120,
    method: BrewMethod.aeropress,
    targetGrindSizeMicrons: 700,
    phases: [
      RecipePhase(startTimeSeconds: 0, pourAmountMl: 200.0, action: PhaseAction.pourCenter),
      RecipePhase(startTimeSeconds: 30, action: PhaseAction.stir),
      RecipePhase(startTimeSeconds: 90, action: PhaseAction.wait), // Instruction can say turn over
      RecipePhase(startTimeSeconds: 120, action: PhaseAction.press),
    ],
  ),
  Recipe(
    name: "Aeropress Espresso Concentrate",
    description: "Ekstrak pekat untuk campuran susu (Latte/Americano). Posisi Inverted. Kopi digiling halus, air sangat sedikit.",
    coffeeGrams: 18.0,
    totalWaterMl: 90.0,
    totalDurationSeconds: 90,
    method: BrewMethod.aeropress,
    targetGrindSizeMicrons: 450,
    phases: [
      RecipePhase(startTimeSeconds: 0, pourAmountMl: 90.0, action: PhaseAction.pourCenter),
      RecipePhase(startTimeSeconds: 30, action: PhaseAction.stir),
      RecipePhase(startTimeSeconds: 70, action: PhaseAction.wait),
      RecipePhase(startTimeSeconds: 90, action: PhaseAction.press),
    ],
  ),

  // ====================================
  // VIETNAM DRIP RECIPES (Total 5)
  // ====================================
  Recipe(
    name: "Tradisional Vietnam Drip (Susu)",
    description: "Susu kental manis di dasar gelas. Kopi diteteskan perlahan ke atas susu.",
    coffeeGrams: 15.0,
    totalWaterMl: 120.0,
    condensedMilkMl: 40,
    totalDurationSeconds: 300,
    method: BrewMethod.vietnamDrip,
    targetGrindSizeMicrons: 800,
    phases: [
      RecipePhase(startTimeSeconds: 0, pourAmountMl: 20.0, action: PhaseAction.pourCenter),
      RecipePhase(startTimeSeconds: 30, pourAmountMl: 100.0, action: PhaseAction.pourCenter),
    ],
  ),
  Recipe(
    name: "Ca Phe Sua Da (Kopi Susu Es)",
    description: "Susu lebih banyak dan kopi dibuat lebih pekat karena akan dilelehkan dengan es batu.",
    coffeeGrams: 20.0,
    totalWaterMl: 100.0,
    condensedMilkMl: 60,
    totalDurationSeconds: 300,
    method: BrewMethod.vietnamDrip,
    targetGrindSizeMicrons: 750,
    phases: [
      RecipePhase(startTimeSeconds: 0, pourAmountMl: 20.0, action: PhaseAction.pourCenter),
      RecipePhase(startTimeSeconds: 40, pourAmountMl: 80.0, action: PhaseAction.pourCenter),
    ],
  ),
  Recipe(
    name: "Ca Phe Den (Kopi Hitam)",
    description: "Vietnam Drip tanpa susu kental manis. Rasio air dibuat lebih panjang dan gilingan lebih kasar agar tidak pahit.",
    coffeeGrams: 15.0,
    totalWaterMl: 150.0,
    totalDurationSeconds: 300,
    method: BrewMethod.vietnamDrip,
    targetGrindSizeMicrons: 900,
    phases: [
      RecipePhase(startTimeSeconds: 0, pourAmountMl: 25.0, action: PhaseAction.pourCenter),
      RecipePhase(startTimeSeconds: 40, pourAmountMl: 125.0, action: PhaseAction.pourCenter),
    ],
  ),
  Recipe(
    name: "Modern Specialty Drip",
    description: "Pendekatan modern untuk biji kopi Light Roast. Mengekstrak acidity dengan bersih.",
    coffeeGrams: 15.0,
    totalWaterMl: 225.0,
    totalDurationSeconds: 240,
    method: BrewMethod.vietnamDrip,
    targetGrindSizeMicrons: 850,
    phases: [
      RecipePhase(startTimeSeconds: 0, pourAmountMl: 40.0, action: PhaseAction.pourCenter),
      RecipePhase(startTimeSeconds: 45, pourAmountMl: 185.0, action: PhaseAction.pourCenter),
    ],
  ),
  Recipe(
    name: "Drip Ristretto Style",
    description: "Kopi ditekan sangat padat, air panas sedikit. Tetesan super intens bagai sirup kopi tebal.",
    coffeeGrams: 20.0,
    totalWaterMl: 60.0,
    totalDurationSeconds: 300,
    method: BrewMethod.vietnamDrip,
    targetGrindSizeMicrons: 700,
    phases: [
      RecipePhase(startTimeSeconds: 0, pourAmountMl: 60.0, action: PhaseAction.pourCenter),
    ],
  ),

  // ====================================
  // CUPPING RECIPES (Total 5)
  // ====================================
  Recipe(
    name: "SCA Cupping Protocol",
    description: "Standar cupping. Menit ke-4 hancurkan kerak (break the crust). Mulai menyeruput di menit 10.",
    coffeeGrams: 11.0,
    totalWaterMl: 200.0,
    totalDurationSeconds: 660,
    method: BrewMethod.cupping,
    targetGrindSizeMicrons: 850,
    phases: [
      RecipePhase(startTimeSeconds: 0, pourAmountMl: 200.0, action: PhaseAction.pourCenter),
      RecipePhase(startTimeSeconds: 240, action: PhaseAction.stir),
      RecipePhase(startTimeSeconds: 245, action: PhaseAction.wait),
      RecipePhase(startTimeSeconds: 600, action: PhaseAction.wait),
    ],
  ),
  Recipe(
    name: "James Hoffmann Home Cupping",
    description: "Cupping ala rumahan. Gunakan sendok sayur untuk membersihkan busa di menit ke-4.",
    coffeeGrams: 12.0,
    totalWaterMl: 200.0,
    totalDurationSeconds: 720,
    method: BrewMethod.cupping,
    targetGrindSizeMicrons: 850,
    phases: [
      RecipePhase(startTimeSeconds: 0, pourAmountMl: 200.0, action: PhaseAction.pourCenter),
      RecipePhase(startTimeSeconds: 240, action: PhaseAction.stir),
      RecipePhase(startTimeSeconds: 245, action: PhaseAction.wait),
      RecipePhase(startTimeSeconds: 720, action: PhaseAction.wait), // 12 minutes
    ],
  ),
  Recipe(
    name: "Rapid QC Cupping",
    description: "Cupping cepat untuk Quality Control toko yang sibuk. Break di menit 3, evaluasi di menit 8.",
    coffeeGrams: 10.0,
    totalWaterMl: 180.0,
    totalDurationSeconds: 480,
    method: BrewMethod.cupping,
    targetGrindSizeMicrons: 850,
    phases: [
      RecipePhase(startTimeSeconds: 0, pourAmountMl: 180.0, action: PhaseAction.pourCenter),
      RecipePhase(startTimeSeconds: 180, action: PhaseAction.stir),
      RecipePhase(startTimeSeconds: 480, action: PhaseAction.wait),
    ],
  ),
  Recipe(
    name: "Roast Defect Cupping",
    description: "Mengekstrak paksa untuk mencari cacat sangrai. Gilingan lebih halus dan air mendidih (100°C).",
    coffeeGrams: 12.0,
    totalWaterMl: 200.0,
    totalDurationSeconds: 600,
    method: BrewMethod.cupping,
    targetGrindSizeMicrons: 700,
    phases: [
      RecipePhase(startTimeSeconds: 0, pourAmountMl: 200.0, action: PhaseAction.pourCenter),
      RecipePhase(startTimeSeconds: 240, action: PhaseAction.stir),
      RecipePhase(startTimeSeconds: 600, action: PhaseAction.wait),
    ],
  ),
  Recipe(
    name: "Cold Evaluation Cupping",
    description: "Evaluasi fokus di acidity kopi dingin (menit 15-20). Fase awal sama, namun tunggu sangat lama.",
    coffeeGrams: 11.0,
    totalWaterMl: 200.0,
    totalDurationSeconds: 900,
    method: BrewMethod.cupping,
    targetGrindSizeMicrons: 850,
    phases: [
      RecipePhase(startTimeSeconds: 0, pourAmountMl: 200.0, action: PhaseAction.pourCenter),
      RecipePhase(startTimeSeconds: 240, action: PhaseAction.stir),
      RecipePhase(startTimeSeconds: 900, action: PhaseAction.wait),
    ],
  ),

  // ====================================
  // COLD BREW RECIPES (Total 5)
  // ====================================
  Recipe(
    name: "Classic Cold Brew",
    description: "Tuang seluruh air, aduk. Simpan di kulkas 12-24 jam. Timer ini hanya membantu pengadukan awal.",
    coffeeGrams: 50.0,
    totalWaterMl: 500.0,
    totalDurationSeconds: 60,
    method: BrewMethod.coldBrew,
    targetGrindSizeMicrons: 1100,
    phases: [
      RecipePhase(startTimeSeconds: 0, pourAmountMl: 500.0, action: PhaseAction.pourCenter),
      RecipePhase(startTimeSeconds: 60, action: PhaseAction.stir),
    ],
  ),
  Recipe(
    name: "Hot Bloom Cold Brew",
    description: "Tuang 100ml air panas dulu selama 45 detik (Bloom), lalu lanjut tuang sisa air dingin. Simpan kulkas.",
    coffeeGrams: 50.0,
    totalWaterMl: 500.0,
    totalDurationSeconds: 120,
    method: BrewMethod.coldBrew,
    targetGrindSizeMicrons: 1100,
    phases: [
      RecipePhase(startTimeSeconds: 0, pourAmountMl: 100.0, action: PhaseAction.pourCenter), // Air panas
      RecipePhase(startTimeSeconds: 45, action: PhaseAction.stir),
      RecipePhase(startTimeSeconds: 60, pourAmountMl: 400.0, action: PhaseAction.pourCenter), // Air dingin
    ],
  ),
  Recipe(
    name: "Kyoto Drip (Setup)",
    description: "Rasio tetesan air es pelan. Timer ini membantu membasahi seluruh kopi di awal sebelum alat dihidupkan.",
    coffeeGrams: 40.0,
    totalWaterMl: 400.0,
    totalDurationSeconds: 120,
    method: BrewMethod.coldBrew,
    targetGrindSizeMicrons: 900,
    phases: [
      RecipePhase(startTimeSeconds: 0, action: PhaseAction.wait), // Wetting puck
    ],
  ),
  Recipe(
    name: "Aeropress Flash Cold Brew",
    description: "Seduh sangat pekat di Aeropress (air panas) lalu langsung ditekan ke atas gelas berisi bongkahan es.",
    coffeeGrams: 20.0,
    totalWaterMl: 100.0,
    totalDurationSeconds: 90,
    method: BrewMethod.coldBrew,
    targetGrindSizeMicrons: 600,
    phases: [
      RecipePhase(startTimeSeconds: 0, pourAmountMl: 100.0, action: PhaseAction.pourCenter),
      RecipePhase(startTimeSeconds: 60, action: PhaseAction.stir),
      RecipePhase(startTimeSeconds: 90, action: PhaseAction.press),
    ],
  ),
  Recipe(
    name: "Milk Brew",
    description: "Ekstraksi dingin langsung di dalam Susu (tanpa air). Aduk di awal. Biarkan 12 jam di kulkas.",
    coffeeGrams: 40.0,
    totalWaterMl: 400.0, // This implies milk
    totalDurationSeconds: 60,
    method: BrewMethod.coldBrew,
    targetGrindSizeMicrons: 1000,
    phases: [
      RecipePhase(startTimeSeconds: 0, pourAmountMl: 400.0, action: PhaseAction.pourCenter), // Susu
      RecipePhase(startTimeSeconds: 60, action: PhaseAction.stir),
    ],
  ),
];
"""

    new_content = header + recipes
    with open('lib/core/recipe.dart', 'w', encoding='utf-8') as f:
        f.write(new_content)

if __name__ == "__main__":
    update_recipes()
