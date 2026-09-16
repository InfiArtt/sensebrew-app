import re

with open('lib/core/recipe.dart', 'r', encoding='utf-8') as f:
    text = f.read()

names = re.findall(r'Recipe\(\s*name: "(.*?)",\s*description: "(.*?)"', text, flags=re.DOTALL)
missing = [n for n, d in names if 'Estimasi Rasa' not in d]
for m in missing:
    print(m)
