import re

with open('lib/core/app_strings.dart', 'r', encoding='utf-8') as f:
    app_strings = f.read()

app_strings = re.sub(
    r"(// AUTO TRANSLATED RECIPE DESCRIPTIONS\n).*?('brew_dose':)",
    r"\1\2",
    app_strings,
    flags=re.DOTALL
)

with open('lib/core/app_strings.dart', 'w', encoding='utf-8') as f:
    f.write(app_strings)

print("Cleaned up corrupted strings.")
