import re

with open('lib/screens/home_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    "const Padding(\n                padding: EdgeInsets.symmetric(horizontal: 16.0, vertical: 8.0),\n                child: Text(AppStrings.str(lang, 'home_select_method')",
    "Padding(\n                padding: const EdgeInsets.symmetric(horizontal: 16.0, vertical: 8.0),\n                child: Text(AppStrings.str(lang, 'home_select_method')"
)

with open('lib/screens/home_screen.dart', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed const Padding in home_screen")
