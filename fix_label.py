import re

with open("lib/core/app_strings.dart", "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace(
    "'recipe_label': 'Recipe {0}. {1} grams of coffee. {2} milliliters of water.',",
    "'recipe_label': '{0} recipe. {1} grams of coffee. {2} milliliters of water.',"
)

with open("lib/core/app_strings.dart", "w", encoding="utf-8") as f:
    f.write(content)
print("Updated recipe_label")
