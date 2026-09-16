import re

with open('lib/screens/custom_recipe_screen.dart', 'r', encoding='utf-8') as f:
    crs = f.read()

crs = crs.replace(
    "const DropdownMenuItem(value: 'Arabica', child: Text('Arabica')),\n                  const DropdownMenuItem(value: 'Robusta', child: Text('Robusta')),, child: Text('Arabica')),\n                  DropdownMenuItem(value: 'Robusta', child: Text('Robusta')),",
    "const DropdownMenuItem(value: 'Arabica', child: Text('Arabica')),\n                  const DropdownMenuItem(value: 'Robusta', child: Text('Robusta')),"
)

with open('lib/screens/custom_recipe_screen.dart', 'w', encoding='utf-8') as f:
    f.write(crs)

print("Fixed syntax error in items list")
