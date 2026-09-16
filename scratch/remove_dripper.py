import re

# 1. Update brewing_screen.dart
with open('lib/screens/brewing_screen.dart', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace("'Swirl the dripper.'", "'Swirl the brewer.'")
text = text.replace("'Swirl dripper'", "'Swirl brewer'")
text = text.replace("'Goyangkan/Swirl dripper'", "'Goyangkan/Swirl alat seduh'")

with open('lib/screens/brewing_screen.dart', 'w', encoding='utf-8') as f:
    f.write(text)

# 2. Update custom_recipe_screen.dart
with open('lib/screens/custom_recipe_screen.dart', 'r', encoding='utf-8') as f:
    text2 = f.read()

text2 = text2.replace("'Swirl Dripper'", "'Swirl Brewer'")
text2 = text2.replace("'Swirl/Goyang Dripper'", "'Swirl/Goyang Alat Seduh'")

with open('lib/screens/custom_recipe_screen.dart', 'w', encoding='utf-8') as f:
    f.write(text2)

print("Removed 'dripper' from swirl instructions.")
