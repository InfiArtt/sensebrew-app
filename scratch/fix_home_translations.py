import re

with open('lib/core/app_strings.dart', 'r', encoding='utf-8') as f:
    content = f.read()

id_keys = """
      'home_select_method': 'Pilih Metode Seduh:',
      'method_v60_desc': 'Penyeduhan tuang dengan putaran spiral',
      'method_fp_desc': 'Penyeduhan rendam tanpa ampas',
      'method_ap_desc': 'Penyeduhan tekan dengan tekanan udara',
      'method_vd_desc': 'Penyeduhan tetes pelan (Kopi Susu)',
      'method_cup_desc': 'Standar internasional evaluasi kopi',
"""

en_keys = """
      'home_select_method': 'Select Brew Method:',
      'method_v60_desc': 'Pour-over brewing with spiral pours',
      'method_fp_desc': 'Full immersion brew without grounds',
      'method_ap_desc': 'Press method using air pressure',
      'method_vd_desc': 'Slow drip brewing (Coffee with Milk)',
      'method_cup_desc': 'International standard for coffee evaluation',
"""

# Insert into 'id' block
content = re.sub(
    r"('id':\s*\{)",
    r"\1\n" + id_keys,
    content
)

# Insert into 'en' block
content = re.sub(
    r"('en':\s*\{)",
    r"\1\n" + en_keys,
    content
)

with open('lib/core/app_strings.dart', 'w', encoding='utf-8') as f:
    f.write(content)

# Now fix home_screen.dart
with open('lib/screens/home_screen.dart', 'r', encoding='utf-8') as f:
    home = f.read()

home = home.replace(
    "Text('Pilih Metode Seduh:'",
    "Text(AppStrings.str(lang, 'home_select_method')"
)
home = home.replace(
    "_buildMethodCard(context, BrewMethod.v60, \"V60 / Pour-over\", \"Penyeduhan tuang dengan putaran spiral\", Icons.filter_alt),",
    "_buildMethodCard(context, BrewMethod.v60, \"V60 / Pour-over\", AppStrings.str(lang, 'method_v60_desc'), Icons.filter_alt),"
)
home = home.replace(
    "_buildMethodCard(context, BrewMethod.frenchPress, \"French Press\", \"Penyeduhan rendam tanpa ampas\", Icons.coffee),",
    "_buildMethodCard(context, BrewMethod.frenchPress, \"French Press\", AppStrings.str(lang, 'method_fp_desc'), Icons.coffee),"
)
home = home.replace(
    "_buildMethodCard(context, BrewMethod.aeropress, \"Aeropress\", \"Penyeduhan tekan dengan tekanan udara\", Icons.local_cafe),",
    "_buildMethodCard(context, BrewMethod.aeropress, \"Aeropress\", AppStrings.str(lang, 'method_ap_desc'), Icons.local_cafe),"
)
home = home.replace(
    "_buildMethodCard(context, BrewMethod.vietnamDrip, \"Vietnam Drip\", \"Penyeduhan tetes pelan (Kopi Susu)\", Icons.coffee_maker),",
    "_buildMethodCard(context, BrewMethod.vietnamDrip, \"Vietnam Drip\", AppStrings.str(lang, 'method_vd_desc'), Icons.coffee_maker),"
)
home = home.replace(
    "_buildMethodCard(context, BrewMethod.cupping, \"SCA Cupping Protocol\", \"Standar internasional evaluasi kopi\", Icons.emoji_food_beverage),",
    "_buildMethodCard(context, BrewMethod.cupping, \"SCA Cupping Protocol\", AppStrings.str(lang, 'method_cup_desc'), Icons.emoji_food_beverage),"
)

with open('lib/screens/home_screen.dart', 'w', encoding='utf-8') as f:
    f.write(home)

print("Fixed home screen translations")
