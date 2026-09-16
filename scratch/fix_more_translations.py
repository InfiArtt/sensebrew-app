import re

# 1. Update app_strings.dart
with open('lib/core/app_strings.dart', 'r', encoding='utf-8') as f:
    content = f.read()

id_keys = """
      'brew_dose': 'Takar Kopi: {0} sendok',
      'brew_grind': 'Gilingan',
      'brew_bean': 'Jenis Biji Kopi',
      'brew_extra': 'Bahan Tambahan',
      'brew_desc_title': 'Deskripsi Resep:',
      'rotations_half': ' setengah',
      'custom_grind_400': 'Sangat Halus (Espresso)',
      'custom_grind_600': 'Halus (Aeropress)',
      'custom_grind_800': 'Sedang (V60 / Kalita)',
      'custom_grind_1000': 'Agak Kasar (Chemex)',
      'custom_grind_1200': 'Kasar (French Press / Switch)',
      'custom_grind_1400': 'Sangat Kasar (Cold Brew)',
      'custom_bean_blend': 'Blend (Campuran)',
      'custom_bean_bebas': 'Bebas (Semua)',
"""

en_keys = """
      'brew_dose': 'Coffee Dose: {0} scoops',
      'brew_grind': 'Grind Size',
      'brew_bean': 'Coffee Bean',
      'brew_extra': 'Extra Ingredients',
      'brew_desc_title': 'Recipe Description:',
      'rotations_half': ' and a half',
      'custom_grind_400': 'Very Fine (Espresso)',
      'custom_grind_600': 'Fine (Aeropress)',
      'custom_grind_800': 'Medium (V60 / Kalita)',
      'custom_grind_1000': 'Medium Coarse (Chemex)',
      'custom_grind_1200': 'Coarse (French Press / Switch)',
      'custom_grind_1400': 'Very Coarse (Cold Brew)',
      'custom_bean_blend': 'Blend (Mixed)',
      'custom_bean_bebas': 'Any (All)',
"""

content = re.sub(r"('id':\s*\{)", r"\1\n" + id_keys, content)
content = re.sub(r"('en':\s*\{)", r"\1\n" + en_keys, content)

with open('lib/core/app_strings.dart', 'w', encoding='utf-8') as f:
    f.write(content)


# 2. Patch custom_recipe_screen.dart
with open('lib/screens/custom_recipe_screen.dart', 'r', encoding='utf-8') as f:
    crs = f.read()

crs = crs.replace("Text('Blend (Campuran)')", "Text(AppStrings.str(lang, 'custom_bean_blend'))")
crs = crs.replace("Text('Bebas (Semua)')", "Text(AppStrings.str(lang, 'custom_bean_bebas'))")

crs = crs.replace("Text('Sangat Halus (Espresso)')", "Text(AppStrings.str(lang, 'custom_grind_400'))")
crs = crs.replace("Text('Halus (Aeropress)')", "Text(AppStrings.str(lang, 'custom_grind_600'))")
crs = crs.replace("Text('Sedang (V60 / Kalita)')", "Text(AppStrings.str(lang, 'custom_grind_800'))")
crs = crs.replace("Text('Agak Kasar (Chemex)')", "Text(AppStrings.str(lang, 'custom_grind_1000'))")
crs = crs.replace("Text('Kasar (French Press / Switch)')", "Text(AppStrings.str(lang, 'custom_grind_1200'))")
crs = crs.replace("Text('Sangat Kasar (Cold Brew)')", "Text(AppStrings.str(lang, 'custom_grind_1400'))")
crs = crs.replace("ExcludeSemantics(child: Text('Target Gilingan', style: const TextStyle(fontWeight: FontWeight.bold)))", "ExcludeSemantics(child: Text(AppStrings.str(lang, 'brew_grind'), style: const TextStyle(fontWeight: FontWeight.bold)))")

with open('lib/screens/custom_recipe_screen.dart', 'w', encoding='utf-8') as f:
    f.write(crs)


# 3. Patch brewing_screen.dart
with open('lib/screens/brewing_screen.dart', 'r', encoding='utf-8') as f:
    bs = f.read()

bs = bs.replace(
    "String rotStr = (roundedRotations % 1 == 0) ? \"${roundedRotations.toInt()}\" : roundedRotations.toStringAsFixed(1).replaceAll('.5', ' setengah').replaceAll('.0', '');",
    "String rotStr = (roundedRotations % 1 == 0) ? \"${roundedRotations.toInt()}\" : roundedRotations.toStringAsFixed(1).replaceAll('.5', AppStrings.str(lang, 'rotations_half') ?? ' setengah').replaceAll('.0', '');"
)

bs = bs.replace("Text(\"Takar Kopi: $spoonStr sendok\"", "Text(AppStrings.str(lang, 'brew_dose', [spoonStr])")
bs = bs.replace("String grindText = \"Gilingan: ${getGrindCategoryName(widget.recipe.targetGrindSizeMicrons)}\";", "String grindText = \"${AppStrings.str(lang, 'brew_grind')}: ${getGrindCategoryName(widget.recipe.targetGrindSizeMicrons)}\";")
bs = bs.replace("Text(\"Jenis Biji Kopi: ${widget.recipe.beanType}\"", "Text(\"${AppStrings.str(lang, 'brew_bean')}: ${widget.recipe.beanType}\"")
bs = bs.replace("Text(\"Bahan Tambahan: ${widget.recipe.extraIngredients}\"", "Text(\"${AppStrings.str(lang, 'brew_extra')}: ${widget.recipe.extraIngredients}\"")
bs = bs.replace("Text(\"Deskripsi Resep:\"", "Text(AppStrings.str(lang, 'brew_desc_title')")

with open('lib/screens/brewing_screen.dart', 'w', encoding='utf-8') as f:
    f.write(bs)

print("Patched UI strings")
