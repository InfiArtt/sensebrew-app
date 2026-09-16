import re
import json
from deep_translator import GoogleTranslator

# 1. Read recipe.dart
with open('lib/core/recipe.dart', 'r', encoding='utf-8') as f:
    recipe_code = f.read()

# 2. Extract description and extraIngredients strings
desc_matches = re.findall(r'description:\s*"(.*?)",', recipe_code)
extra_matches = re.findall(r'extraIngredients:\s*"(.*?)",', recipe_code)

# Combine and deduplicate, remove empty
strings_to_translate = list(set([s for s in desc_matches + extra_matches if s.strip() != ""]))

# Initialize translator
translator = GoogleTranslator(source='id', target='en')

translations = {}
for idx, s in enumerate(strings_to_translate):
    print(f"Translating {idx+1}/{len(strings_to_translate)}: {s}")
    # deep-translator handles it well. 
    # Let's clean the string a bit just in case, but keep exact match for the key!
    try:
        translated = translator.translate(s)
        # escape single quotes for dart map insertion
        safe_key = s.replace("'", "\\'")
        safe_val = translated.replace("'", "\\'")
        translations[safe_key] = safe_val
    except Exception as e:
        print(f"Error translating: {s}. Error: {e}")

# 3. Read app_strings.dart
with open('lib/core/app_strings.dart', 'r', encoding='utf-8') as f:
    app_strings = f.read()

# 4. Generate the dart map entries for 'en'
en_additions = "\n      // AUTO TRANSLATED RECIPE DESCRIPTIONS\n"
for key, val in translations.items():
    en_additions += f"      '{key}': '{val}',\n"

# Insert into 'en' block
app_strings = re.sub(
    r"('en':\s*\{)",
    r"\1" + en_additions,
    app_strings
)

with open('lib/core/app_strings.dart', 'w', encoding='utf-8') as f:
    f.write(app_strings)

print("Translations generated and injected successfully!")
