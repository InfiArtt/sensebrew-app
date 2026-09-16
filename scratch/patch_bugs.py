import re

# 1. FIX TIMER_STATE.DART
with open('lib/core/timer_state.dart', 'r', encoding='utf-8') as f:
    timer_code = f.read()

timer_code = timer_code.replace(
    "AudioPlayer.global.setAudioContext(audioContext);",
    "AudioPlayer.global.setAudioContext(audioContext);\n    _audioPlayer.setAudioContext(audioContext);"
)

with open('lib/core/timer_state.dart', 'w', encoding='utf-8') as f:
    f.write(timer_code)

# 2. FIX BREWING_SCREEN.DART
with open('lib/screens/brewing_screen.dart', 'r', encoding='utf-8') as f:
    brewing_code = f.read()

# Replace getGrindCategoryName
old_grind = """  String getGrindCategoryName(int microns) {
    if (microns <= 400) return "Sangat Halus (Espresso)";
    if (microns <= 600) return "Halus (Aeropress / Moka Pot)";
    if (microns <= 800) return "Sedang (V60 / Kalita)";
    if (microns <= 1000) return "Sedang Kasar (Chemex)";
    if (microns <= 1200) return "Kasar (French Press / Switch)";
    return "Sangat Kasar (Cold Brew)";
  }"""

new_grind = """  String getGrindCategoryName(int microns, String lang) {
    if (microns <= 400) return AppStrings.str(lang, 'custom_grind_400');
    if (microns <= 600) return AppStrings.str(lang, 'custom_grind_600');
    if (microns <= 800) return AppStrings.str(lang, 'custom_grind_800');
    if (microns <= 1000) return AppStrings.str(lang, 'custom_grind_1000');
    if (microns <= 1200) return AppStrings.str(lang, 'custom_grind_1200');
    return AppStrings.str(lang, 'custom_grind_1400');
  }"""

brewing_code = brewing_code.replace(old_grind, new_grind)
brewing_code = brewing_code.replace(
    "getGrindCategoryName(widget.recipe.targetGrindSizeMicrons)",
    "getGrindCategoryName(widget.recipe.targetGrindSizeMicrons, lang)"
)

# Replace the rotStr generations
def fix_rot_str(code):
    bad_rot_1 = 'String rotStr = (roundedRotations % 1 == 0) ? "${roundedRotations.toInt()} putaran" : "${roundedRotations.toStringAsFixed(1).replaceAll(\'.5\', \' setengah\').replaceAll(\'.0\', \'\')} putaran";'
    good_rot_1 = 'String unit = lang == "en" ? "rotations" : "putaran"; String half = AppStrings.str(lang, "rotations_half") ?? " setengah"; String rotStr = (roundedRotations % 1 == 0) ? "${roundedRotations.toInt()} $unit" : "${roundedRotations.toStringAsFixed(1).replaceAll(\'.5\', half).replaceAll(\'.0\', \'\')} $unit";'
    return code.replace(bad_rot_1, good_rot_1)

brewing_code = fix_rot_str(brewing_code)

with open('lib/screens/brewing_screen.dart', 'w', encoding='utf-8') as f:
    f.write(brewing_code)

# 3. FIX METHOD_RECIPE_SCREEN.DART Grind size
with open('lib/screens/method_recipe_screen.dart', 'r', encoding='utf-8') as f:
    method_code = f.read()

method_code = method_code.replace(old_grind, new_grind)
method_code = method_code.replace(
    "getGrindCategoryName(recipe.targetGrindSizeMicrons)",
    "getGrindCategoryName(recipe.targetGrindSizeMicrons, lang)"
)

with open('lib/screens/method_recipe_screen.dart', 'w', encoding='utf-8') as f:
    f.write(method_code)

print("Patch applied to dart files.")
