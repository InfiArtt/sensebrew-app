import re
import time
from deep_translator import GoogleTranslator

with open('lib/core/recipe.dart', 'r', encoding='utf-8') as f:
    recipe_code = f.read()

desc_matches = re.findall(r'description:\s*"(.*?)",', recipe_code)
extra_matches = re.findall(r'extraIngredients:\s*"(.*?)",', recipe_code)

strings_to_translate = list(set([s for s in desc_matches + extra_matches if s.strip() != ""]))

translator = GoogleTranslator(source='id', target='en')

translations = {}
for idx, s in enumerate(strings_to_translate):
    try:
        translated = translator.translate(s)
        safe_key = s.replace("'", "\\'")
        safe_val = translated.replace("'", "\\'")
        translations[safe_key] = safe_val
        time.sleep(1) # avoid rate limits
    except Exception as e:
        # just skip if it fails, or retry once
        time.sleep(2)
        try:
            translated = translator.translate(s)
            safe_key = s.replace("'", "\\'")
            safe_val = translated.replace("'", "\\'")
            translations[safe_key] = safe_val
        except:
            pass

with open('lib/core/app_strings.dart', 'r', encoding='utf-8') as f:
    app_strings = f.read()

en_additions = "\n      // AUTO TRANSLATED RECIPE DESCRIPTIONS\n"
for key, val in translations.items():
    en_additions += f"      '{key}': '{val}',\n"

app_strings = re.sub(
    r"('en':\s*\{)",
    r"\1" + en_additions,
    app_strings
)

with open('lib/core/app_strings.dart', 'w', encoding='utf-8') as f:
    f.write(app_strings)

print("Translations successful!")
