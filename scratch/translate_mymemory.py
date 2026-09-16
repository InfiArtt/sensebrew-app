import re
import urllib.request
import urllib.parse
import json
import time
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('lib/core/recipe.dart', 'r', encoding='utf-8') as f:
    recipe_code = f.read()

desc_matches = re.findall(r'description:\s*"(.*?)",', recipe_code)
extra_matches = re.findall(r'extraIngredients:\s*"(.*?)",', recipe_code)

strings_to_translate = list(set([s for s in desc_matches + extra_matches if s.strip() != ""]))

translations = {}
print(f"Translating {len(strings_to_translate)} strings using MyMemory API...")

for idx, s in enumerate(strings_to_translate):
    print(f"{idx}/{len(strings_to_translate)}")
    url = f"https://api.mymemory.translated.net/get?q={urllib.parse.quote(s)}&langpair=id|en"
    
    success = False
    retries = 0
    while not success and retries < 3:
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode())
                translated = data['responseData']['translatedText']
                safe_key = s.replace("'", "\\'")
                safe_val = translated.replace("'", "\\'")
                translations[safe_key] = safe_val
                success = True
                time.sleep(0.5)
        except Exception as e:
            retries += 1
            print(f"Error, retrying... {e}")
            time.sleep(2)

with open('lib/core/app_strings.dart', 'r', encoding='utf-8') as f:
    app_strings = f.read()

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

print("Translations successful and injected via MyMemory!")
