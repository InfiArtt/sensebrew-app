import re

# FIX GRINDER_DATABASE.DART
with open('lib/core/grinder_database.dart', 'r', encoding='utf-8') as f:
    grinder_code = f.read()

old_func = """String getGrindCategoryName(int microns) {
  if (microns < 500) return 'Halus';
  if (microns < 700) return 'Sedang-Halus';
  if (microns < 1000) return 'Sedang';
  return 'Kasar';
}"""

new_func = """String getGrindCategoryName(int microns, String lang) {
  if (microns <= 400) return AppStrings.str(lang, 'custom_grind_400');
  if (microns <= 600) return AppStrings.str(lang, 'custom_grind_600');
  if (microns <= 800) return AppStrings.str(lang, 'custom_grind_800');
  if (microns <= 1000) return AppStrings.str(lang, 'custom_grind_1000');
  if (microns <= 1200) return AppStrings.str(lang, 'custom_grind_1200');
  return AppStrings.str(lang, 'custom_grind_1400');
}"""

grinder_code = grinder_code.replace(old_func, new_func)

# add import for AppStrings
if 'app_strings.dart' not in grinder_code:
    grinder_code = "import 'app_strings.dart';\n" + grinder_code

with open('lib/core/grinder_database.dart', 'w', encoding='utf-8') as f:
    f.write(grinder_code)

print("Fixed grinder_database.dart")
