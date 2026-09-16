import re
import time
from deep_translator import GoogleTranslator
import sys

# Ensure stdout doesn't crash on windows
sys.stdout.reconfigure(encoding='utf-8')

with open('lib/core/recipe.dart', 'r', encoding='utf-8') as f:
    recipe_code = f.read()

desc_matches = re.findall(r'description:\s*"(.*?)",', recipe_code)
extra_matches = re.findall(r'extraIngredients:\s*"(.*?)",', recipe_code)
name_matches = re.findall(r'name:\s*"(.*?)",', recipe_code)

strings_to_translate = list(set([s for s in desc_matches + extra_matches + name_matches if s.strip() != ""]))

translator = GoogleTranslator(source='id', target='en')

translations = {}
print(f"Starting translation of {len(strings_to_translate)} strings...")

for idx, s in enumerate(strings_to_translate):
    print(f"Translating {idx+1}/{len(strings_to_translate)}...")
    success = False
    retries = 0
    while not success and retries < 3:
        try:
            translated = translator.translate(s)
            safe_key = s.replace("'", "\\'")
            safe_val = translated.replace("'", "\\'")
            translations[safe_key] = safe_val
            success = True
            time.sleep(1.5) # avoid rate limits
        except Exception as e:
            retries += 1
            print(f"Error, retrying... {e}")
            time.sleep(3)

with open('lib/core/app_strings.dart', 'r', encoding='utf-8') as f:
    app_strings = f.read()

# Remove old injection marker if exists
app_strings = app_strings.replace("      // AUTO TRANSLATED RECIPE DESCRIPTIONS\n", "")

en_additions = "      // AUTO TRANSLATED RECIPE DESCRIPTIONS\n"
for key, val in translations.items():
    en_additions += f"      '{key}': '{val}',\n"

app_strings = re.sub(
    r"('en':\s*\{)",
    r"\1\n" + en_additions,
    app_strings
)

with open('lib/core/app_strings.dart', 'w', encoding='utf-8') as f:
    f.write(app_strings)

print("Translations successful and injected!")
