import re

with open("lib/core/app_strings.dart", "r", encoding="utf-8") as f:
    content = f.read()

# Add grinder_clicks
content = content.replace(
    "'id': {",
    "'id': {\n      'grinder_clicks': 'klik',"
)
content = content.replace(
    "'en': {",
    "'en': {\n      'grinder_clicks': 'clicks',"
)

with open("lib/core/app_strings.dart", "w", encoding="utf-8") as f:
    f.write(content)

with open("lib/core/grinder_database.dart", "r", encoding="utf-8") as f:
    grinder_content = f.read()

grinder_content = grinder_content.replace(
    " klik'",
    " \'"
)

# wait, we need to import app_strings.dart in grinder_database.dart if not already imported
if 'app_strings.dart' not in grinder_content:
    grinder_content = "import 'package:v60_blind_guide/core/app_strings.dart';\n" + grinder_content

with open("lib/core/grinder_database.dart", "w", encoding="utf-8") as f:
    f.write(grinder_content)

print("Updated grinder_database.dart and app_strings.dart!")
