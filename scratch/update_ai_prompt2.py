import re

with open('lib/core/ai_service.dart', 'r', encoding='utf-8') as f:
    code = f.read()

target = 'The JSON must strictly follow this structure:\\n{'
replacement = '''RULES:
- For "targetGrindSizeMicrons", use 400 (Sangat Halus/Espresso), 600 (Halus/Aeropress), 800 (Sedang/V60), 1000 (Agak Kasar/Chemex), 1200 (Kasar/French Press), or 1400 (Sangat Kasar/Cold Brew).
- For "extraIngredients", write cleanly with metric units (e.g. "15 ml susu kental manis", "10 gram gula aren"). DO NOT use acronyms like "sdm" or "SKM". If none, leave blank string "".

The JSON must strictly follow this structure:
{'''

code = code.replace(target, replacement)

with open('lib/core/ai_service.dart', 'w', encoding='utf-8') as f:
    f.write(code)

print('AI Prompt updated 2!')
