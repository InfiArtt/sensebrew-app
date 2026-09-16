import re

with open('lib/screens/custom_recipe_screen.dart', 'r', encoding='utf-8') as f:
    crs = f.read()

crs = crs.replace(
    "child: Column(\n                                  mainAxisSize: MainAxisSize.min,\n                                  children: PhaseAction.values.map((action) {",
    "child: SingleChildScrollView(\n                                  child: Column(\n                                    mainAxisSize: MainAxisSize.min,\n                                    children: PhaseAction.values.map((action) {"
)
crs = crs.replace(
    "}).toList(),\n                                ),\n                              );",
    "}).toList(),\n                                  ),\n                                ),\n                              );"
)

with open('lib/screens/custom_recipe_screen.dart', 'w', encoding='utf-8') as f:
    f.write(crs)

print("Fixed SingleChildScrollView")
