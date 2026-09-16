import re
import json

with open('lib/core/recipe.dart', 'r', encoding='utf-8') as f:
    text = f.read()

# We'll just define the new recipes here as strings.
new_v60 = """
  // === NEW V60 RECIPES ===
  Recipe(
    name: "James Hoffmann Ultimate V60",
    description: "Teknik 1 penuangan dengan adukan awal dan swirl di akhir. Menghasilkan ekstraksi merata untuk kopi light roast.",
    coffeeGrams: 15, totalWaterMl: 250, totalDurationSeconds: 180,
    method: BrewMethod.v60, targetGrindSizeMicrons: 800, beanType: 'Arabica',
    phases: [
      RecipePhase(startTimeSeconds: 0, pourAmountMl: 50, action: PhaseAction.pourCenter),
      RecipePhase(startTimeSeconds: 10, action: PhaseAction.stir),
      RecipePhase(startTimeSeconds: 45, pourAmountMl: 200, action: PhaseAction.pourCircle),
    ],
  ),
  Recipe(
    name: "Lance Hedrick 1-Pour",
    description: "Satu tuangan panjang dan tinggi untuk agitasi maksimal. Hasilkan ekstraksi tinggi dan rasa manis.",
    coffeeGrams: 15, totalWaterMl: 250, totalDurationSeconds: 150,
    method: BrewMethod.v60, targetGrindSizeMicrons: 900, beanType: 'Arabica',
    phases: [
      RecipePhase(startTimeSeconds: 0, pourAmountMl: 50, action: PhaseAction.pourCenter),
      RecipePhase(startTimeSeconds: 45, pourAmountMl: 200, action: PhaseAction.pourCircle),
    ],
  ),
  Recipe(
    name: "Orea V3 Fast Pour",
    description: "Tuangan cepat untuk dripper datar (flat bed) seperti Orea atau Kalita Wave. Menyoroti acidity.",
    coffeeGrams: 12, totalWaterMl: 200, totalDurationSeconds: 120,
    method: BrewMethod.v60, targetGrindSizeMicrons: 700, beanType: 'Arabica',
    phases: [
      RecipePhase(startTimeSeconds: 0, pourAmountMl: 40, action: PhaseAction.pourCircle),
      RecipePhase(startTimeSeconds: 30, pourAmountMl: 80, action: PhaseAction.pourCircle),
      RecipePhase(startTimeSeconds: 60, pourAmountMl: 80, action: PhaseAction.pourCircle),
    ],
  ),
  Recipe(
    name: "April Brewer Recipe",
    description: "Resep resmi Patrik Rolf. Suhu air rendah (90C) dan 2 kali tuangan yang sama rata.",
    coffeeGrams: 13, totalWaterMl: 200, totalDurationSeconds: 150,
    method: BrewMethod.v60, targetGrindSizeMicrons: 900, beanType: 'Arabica',
    phases: [
      RecipePhase(startTimeSeconds: 0, pourAmountMl: 100, action: PhaseAction.pourCircle),
      RecipePhase(startTimeSeconds: 35, pourAmountMl: 100, action: PhaseAction.pourCircle),
    ],
  ),
  Recipe(
    name: "V60 Dark Roast (Low Temp)",
    description: "Gunakan air suhu 85C dan tuangan cepat untuk menghindari rasa gosong dan pahit berlebih.",
    coffeeGrams: 15, totalWaterMl: 250, totalDurationSeconds: 150,
    method: BrewMethod.v60, targetGrindSizeMicrons: 1000, beanType: 'Blend',
    phases: [
      RecipePhase(startTimeSeconds: 0, pourAmountMl: 50, action: PhaseAction.pourCenter),
      RecipePhase(startTimeSeconds: 30, pourAmountMl: 100, action: PhaseAction.pourCircle),
      RecipePhase(startTimeSeconds: 60, pourAmountMl: 100, action: PhaseAction.pourCircle),
    ],
  ),
  Recipe(
    name: "Kasuya Devil Recipe",
    description: "Menggunakan suhu air berbeda (air biasa untuk bloom, lalu air mendidih) di V60 Switch.",
    coffeeGrams: 20, totalWaterMl: 280, totalDurationSeconds: 120,
    method: BrewMethod.v60, targetGrindSizeMicrons: 800, beanType: 'Arabica',
    phases: [
      RecipePhase(startTimeSeconds: 0, pourAmountMl: 60, action: PhaseAction.pourCenter),
      RecipePhase(startTimeSeconds: 30, action: PhaseAction.closeValve),
      RecipePhase(startTimeSeconds: 35, pourAmountMl: 220, action: PhaseAction.pourCircle),
      RecipePhase(startTimeSeconds: 90, action: PhaseAction.openValve),
    ],
  ),
  Recipe(
    name: "Hybrid Immersion (Switch)",
    description: "100% Imersi penuh di Hario Switch dari awal, lalu dibuka di menit ke-2.",
    coffeeGrams: 15, totalWaterMl: 250, totalDurationSeconds: 150,
    method: BrewMethod.v60, targetGrindSizeMicrons: 900, beanType: 'Arabica',
    phases: [
      RecipePhase(startTimeSeconds: 0, action: PhaseAction.closeValve),
      RecipePhase(startTimeSeconds: 5, pourAmountMl: 250, action: PhaseAction.pourCircle),
      RecipePhase(startTimeSeconds: 120, action: PhaseAction.openValve),
    ],
  ),
"""

new_ap = """
  // === NEW AEROPRESS RECIPES ===
  Recipe(
    name: "W.A.C Carolina Ibarra (2018)",
    description: "Resep juara dunia 2018. Posisi inverted, aduk kuat, hasilkan ekstraksi yang super fruity.",
    coffeeGrams: 34.9, totalWaterMl: 200, totalDurationSeconds: 90,
    method: BrewMethod.aeropress, targetGrindSizeMicrons: 800, beanType: 'Arabica',
    phases: [
      RecipePhase(startTimeSeconds: 0, pourAmountMl: 100, action: PhaseAction.pourFast),
      RecipePhase(startTimeSeconds: 30, action: PhaseAction.stir),
      RecipePhase(startTimeSeconds: 60, pourAmountMl: 100, action: PhaseAction.pourFast),
      RecipePhase(startTimeSeconds: 75, action: PhaseAction.press),
    ],
  ),
  Recipe(
    name: "W.A.C Paulina Miczka (2017)",
    description: "Resep juara 2017. Rasio 1:5 pekat di awal, ditambah air bypass di akhir. Inverted.",
    coffeeGrams: 35, totalWaterMl: 150, extraIngredients: "160ml air panas tambahan di akhir", totalDurationSeconds: 90,
    method: BrewMethod.aeropress, targetGrindSizeMicrons: 900, beanType: 'Arabica',
    phases: [
      RecipePhase(startTimeSeconds: 0, pourAmountMl: 150, action: PhaseAction.pourFast),
      RecipePhase(startTimeSeconds: 15, action: PhaseAction.stir),
      RecipePhase(startTimeSeconds: 60, action: PhaseAction.press),
    ],
  ),
  Recipe(
    name: "Tuomas Merikanto W.A.C",
    description: "Aeropress standar (tidak inverted). Air 80C, biarkan menetes perlahan lalu press sangat lambat.",
    coffeeGrams: 18, totalWaterMl: 250, totalDurationSeconds: 150,
    method: BrewMethod.aeropress, targetGrindSizeMicrons: 700, beanType: 'Arabica',
    phases: [
      RecipePhase(startTimeSeconds: 0, pourAmountMl: 50, action: PhaseAction.pourCircle),
      RecipePhase(startTimeSeconds: 30, pourAmountMl: 200, action: PhaseAction.pourCircle),
      RecipePhase(startTimeSeconds: 90, action: PhaseAction.press),
    ],
  ),
  Recipe(
    name: "Aeropress Flow Control",
    description: "Menggunakan cap Prismo atau Flow Control. Imersi penuh tanpa inverted.",
    coffeeGrams: 15, totalWaterMl: 200, totalDurationSeconds: 120,
    method: BrewMethod.aeropress, targetGrindSizeMicrons: 600, beanType: 'Arabica',
    phases: [
      RecipePhase(startTimeSeconds: 0, pourAmountMl: 200, action: PhaseAction.pourFast),
      RecipePhase(startTimeSeconds: 30, action: PhaseAction.stir),
      RecipePhase(startTimeSeconds: 90, action: PhaseAction.press),
    ],
  ),
  Recipe(
    name: "Aeropress Espresso Fake",
    description: "Ekstraksi konsentrat tinggi yang menyerupai espresso. Gunakan Prismo/Flow Control dan gilingan espresso.",
    coffeeGrams: 18, totalWaterMl: 60, totalDurationSeconds: 60,
    method: BrewMethod.aeropress, targetGrindSizeMicrons: 300, beanType: 'Blend',
    phases: [
      RecipePhase(startTimeSeconds: 0, pourAmountMl: 60, action: PhaseAction.pourFast),
      RecipePhase(startTimeSeconds: 10, action: PhaseAction.stir),
      RecipePhase(startTimeSeconds: 45, action: PhaseAction.press),
    ],
  ),
  Recipe(
    name: "Aeropress Tea-like Extract",
    description: "Rasio renggang dan gilingan kasar untuk rasa kopi yang mirip teh dan menyegarkan.",
    coffeeGrams: 12, totalWaterMl: 250, totalDurationSeconds: 150,
    method: BrewMethod.aeropress, targetGrindSizeMicrons: 1200, beanType: 'Arabica',
    phases: [
      RecipePhase(startTimeSeconds: 0, pourAmountMl: 250, action: PhaseAction.pourFast),
      RecipePhase(startTimeSeconds: 120, action: PhaseAction.press),
    ],
  ),
  Recipe(
    name: "Aeropress Robusta Sweet",
    description: "Khusus untuk kopi Robusta. Ekstraksi singkat dengan suhu 85C agar tidak terlalu pahit.",
    coffeeGrams: 15, totalWaterMl: 200, totalDurationSeconds: 90,
    method: BrewMethod.aeropress, targetGrindSizeMicrons: 800, beanType: 'Robusta',
    phases: [
      RecipePhase(startTimeSeconds: 0, pourAmountMl: 200, action: PhaseAction.pourFast),
      RecipePhase(startTimeSeconds: 10, action: PhaseAction.stir),
      RecipePhase(startTimeSeconds: 60, action: PhaseAction.press),
    ],
  ),
"""

new_vd = """
  // === NEW VIETNAM DRIP RECIPES ===
  Recipe(
    name: "Ca Phe Muoi (Salted Coffee)",
    description: "Kopi Vietnam dengan buih krim asin (whip cream + garam). Campurkan kopi dengan krim setelah menetes selesai.",
    coffeeGrams: 15, totalWaterMl: 100, extraIngredients: "15ml susu kental manis, Krim kocok bergaram di atasnya", totalDurationSeconds: 300,
    method: BrewMethod.vietnamDrip, targetGrindSizeMicrons: 800, beanType: 'Robusta',
    phases: [
      RecipePhase(startTimeSeconds: 0, pourAmountMl: 20, action: PhaseAction.pourCenter),
      RecipePhase(startTimeSeconds: 30, pourAmountMl: 80, action: PhaseAction.pourCenter),
    ],
  ),
  Recipe(
    name: "Ca Phe Trung (Egg Coffee)",
    description: "Kopi pekat yang dicampur dengan kuning telur yang dikocok bersama susu kental manis hingga mengembang.",
    coffeeGrams: 15, totalWaterMl: 80, extraIngredients: "Krim kuning telur kocok (egg fluff)", totalDurationSeconds: 300,
    method: BrewMethod.vietnamDrip, targetGrindSizeMicrons: 800, beanType: 'Robusta',
    phases: [
      RecipePhase(startTimeSeconds: 0, pourAmountMl: 20, action: PhaseAction.pourCenter),
      RecipePhase(startTimeSeconds: 30, pourAmountMl: 60, action: PhaseAction.pourCenter),
    ],
  ),
  Recipe(
    name: "Ca Phe Sua Chua (Yogurt Coffee)",
    description: "Kombinasi asam segar dari Yogurt dan pahitnya Robusta. Kopi diteteskan ke atas es dan yogurt.",
    coffeeGrams: 15, totalWaterMl: 80, extraIngredients: "3 sendok makan plain yogurt, es batu", totalDurationSeconds: 300,
    method: BrewMethod.vietnamDrip, targetGrindSizeMicrons: 800, beanType: 'Robusta',
    phases: [
      RecipePhase(startTimeSeconds: 0, pourAmountMl: 20, action: PhaseAction.pourCenter),
      RecipePhase(startTimeSeconds: 30, pourAmountMl: 60, action: PhaseAction.pourCenter),
    ],
  ),
  Recipe(
    name: "Phin Arabica Light",
    description: "Vietnam Drip khusus untuk biji Arabica. Sedikit dipadatkan, suhu 92C untuk body tebal nan fruity.",
    coffeeGrams: 18, totalWaterMl: 150, totalDurationSeconds: 300,
    method: BrewMethod.vietnamDrip, targetGrindSizeMicrons: 900, beanType: 'Arabica',
    phases: [
      RecipePhase(startTimeSeconds: 0, pourAmountMl: 30, action: PhaseAction.pourCenter),
      RecipePhase(startTimeSeconds: 40, pourAmountMl: 120, action: PhaseAction.pourCenter),
    ],
  ),
  Recipe(
    name: "Vietnam Drip Mocha",
    description: "Tambahkan cokelat bubuk ke dalam susu kental manis sebelum ditetesi kopi.",
    coffeeGrams: 15, totalWaterMl: 100, extraIngredients: "20ml susu kental manis, 5 gram cokelat bubuk", totalDurationSeconds: 300,
    method: BrewMethod.vietnamDrip, targetGrindSizeMicrons: 800, beanType: 'Blend',
    phases: [
      RecipePhase(startTimeSeconds: 0, pourAmountMl: 20, action: PhaseAction.pourCenter),
      RecipePhase(startTimeSeconds: 30, pourAmountMl: 80, action: PhaseAction.pourCenter),
    ],
  ),
  Recipe(
    name: "Phin Coconut (Bac Xiu)",
    description: "Bac Xiu adalah varian Vietnam Drip dengan rasio susu (dan santan/susu kelapa) yang jauh lebih banyak dari kopinya.",
    coffeeGrams: 12, totalWaterMl: 60, extraIngredients: "40ml susu kental manis, 60ml susu cair/santan, banyak es", totalDurationSeconds: 240,
    method: BrewMethod.vietnamDrip, targetGrindSizeMicrons: 800, beanType: 'Robusta',
    phases: [
      RecipePhase(startTimeSeconds: 0, pourAmountMl: 20, action: PhaseAction.pourCenter),
      RecipePhase(startTimeSeconds: 30, pourAmountMl: 40, action: PhaseAction.pourCenter),
    ],
  ),
"""

import sys

output_file = "scratch/new_db.txt"
with open(output_file, "w", encoding="utf-8") as out:
    out.write(new_v60 + new_ap + new_vd)

print("Generated new additions.")
