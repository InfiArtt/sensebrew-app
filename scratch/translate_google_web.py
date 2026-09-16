import re
import urllib.request
import urllib.parse
import json
import time
import sys
import ssl

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/strings_to_translate.json', 'r', encoding='utf-8') as f:
    strings_to_translate = json.load(f)

translations = {}
print(f"Translating {len(strings_to_translate)} strings using Google Web API...")

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

for idx, s in enumerate(strings_to_translate):
    print(f"{idx+1}/{len(strings_to_translate)}")
    url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=id&tl=en&dt=t&q={urllib.parse.quote(s)}"
    
    success = False
    retries = 0
    while not success and retries < 2:
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=3, context=ctx) as response:
                data = json.loads(response.read().decode())
                translated = "".join([x[0] for x in data[0]])
                
                safe_key = s.replace('\\n', '\\\\n').replace("'", "\\'")
                safe_val = translated.replace('\n', '\\n').replace('\\n', '\\\\n').replace("'", "\\'")
                
                translations[safe_key] = safe_val
                success = True
                time.sleep(1) # wait 1s to avoid ban
        except Exception as e:
            retries += 1
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

print("Translations successful and injected safely!")
