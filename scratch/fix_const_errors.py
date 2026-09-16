import re

# 1. Fix brewing_screen.dart
with open('lib/screens/brewing_screen.dart', 'r', encoding='utf-8') as f:
    bs = f.read()

bs = bs.replace(
    "const Text(AppStrings.str(lang, 'brew_desc_title')",
    "Text(AppStrings.str(lang, 'brew_desc_title')"
)

with open('lib/screens/brewing_screen.dart', 'w', encoding='utf-8') as f:
    f.write(bs)


# 2. Fix custom_recipe_screen.dart
with open('lib/screens/custom_recipe_screen.dart', 'r', encoding='utf-8') as f:
    crs = f.read()

crs = crs.replace(
    "items: const [\n                  DropdownMenuItem(value: 'Arabica'",
    "items: [\n                  const DropdownMenuItem(value: 'Arabica', child: Text('Arabica')),\n                  const DropdownMenuItem(value: 'Robusta', child: Text('Robusta')),"
)

# Replace all the const items with just items: [
# Since there are multiple "items: const [", I'll just use regex
crs = re.sub(
    r"items:\s*const\s*\[",
    r"items: [",
    crs
)

# And if I need to re-add const for the untranslated items, they aren't strictly required to be const.
# But just removing `const` from `items: const [` is enough to let it compile.
with open('lib/screens/custom_recipe_screen.dart', 'w', encoding='utf-8') as f:
    f.write(crs)

print("Fixed const errors")
