import re
import urllib.request
import urllib.parse
import json
import time
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/strings_to_translate.json', 'r', encoding='utf-8') as f:
    strings_to_translate = json.load(f)

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
                
                # ESCAPE NEWLINES AND QUOTES CORRECTLY
                safe_key = s.replace('\\n', '\\\\n').replace("'", "\\'")
                safe_val = translated.replace('\n', '\\n').replace('\\n', '\\\\n').replace("'", "\\'")
                
                translations[safe_key] = safe_val
                success = True
                time.sleep(0.2)
        except Exception as e:
            retries += 1
            print(f"Error, retrying... {e}")
            time.sleep(1)

with open('lib/core/app_strings.dart', 'r', encoding='utf-8') as f:
    app_strings = f.read()

# Make sure we don't duplicate
app_strings = app_strings.replace("      // AUTO TRANSLATED RECIPE DESCRIPTIONS\n", "")

en_additions = "      // AUTO TRANSLATED RECIPE DESCRIPTIONS\n"
for key, val in translations.items():
    # Make sure we properly escape the key as well since json uses \n but dart needs \\n for literal newline in string
    # Wait, the strings from json already have \\n as literal text!
    # Because json.dump escapes \n to \\n.
    # We'll just write it exactly.
    en_additions += f"      '{key}': '{val}',\n"

app_strings = re.sub(
    r"('en':\s*\{)",
    r"\1\n" + en_additions,
    app_strings
)

with open('lib/core/app_strings.dart', 'w', encoding='utf-8') as f:
    f.write(app_strings)

print("Translations successful and injected safely!")
