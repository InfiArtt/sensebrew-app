import re
import urllib.request
import urllib.parse
import json
import time

def translate_text(text):
    if not text.strip(): return ""
    try:
        url = "https://translate.googleapis.com/translate_a/single?client=gtx&sl=id&tl=en&dt=t&q=" + urllib.parse.quote(text)
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(req, timeout=5)
        data = json.loads(response.read().decode('utf-8'))
        return "".join([x[0] for x in data[0]])
    except Exception as e:
        print("Failed to translate:", text[:20])
        return text # fallback to ID

with open('lib/core/recipe.dart', 'r', encoding='utf-8') as f:
    content = f.read()

desc_matches = re.findall(r'description:\s*"([^"]+)"', content)
extra_matches = re.findall(r'extraIngredients:\s*"([^"]+)"', content)

desc_map = {}
extra_map = {}

for d in desc_matches:
    if d not in desc_map:
        desc_map[d] = f"desc_key_{len(desc_map)}"

for e in extra_matches:
    if e not in extra_map:
        extra_map[e] = f"extra_key_{len(extra_map)}"

new_content = content
for d, key in desc_map.items():
    new_content = new_content.replace(f'description: "{d}"', f'description: "{key}"')
for e, key in extra_map.items():
    new_content = new_content.replace(f'extraIngredients: "{e}"', f'extraIngredients: "{key}"')

with open('lib/core/recipe.dart', 'w', encoding='utf-8') as f:
    f.write(new_content)

id_additions = "      // AUTO GENERATED ID RECIPES\n"
en_additions = "      // AUTO GENERATED EN RECIPES\n"

all_strings = {**desc_map, **extra_map}
for id_text, key in all_strings.items():
    en_text = translate_text(id_text)
    
    safe_key = key
    safe_id = id_text.replace('\\n', '\\\\n').replace("'", "\\'")
    safe_en = en_text.replace('\\n', '\\\\n').replace("'", "\\'")
    
    id_additions += f"      '{safe_key}': '{safe_id}',\n"
    en_additions += f"      '{safe_key}': '{safe_en}',\n"
    time.sleep(0.1) # to prevent 429

with open('lib/core/app_strings.dart', 'r', encoding='utf-8') as f:
    app_strings = f.read()

# Insert ID additions at the end of 'id' block
app_strings = re.sub(
    r"('id':\s*\{)",
    r"\1\n" + id_additions,
    app_strings
)

# Insert EN additions at the end of 'en' block
app_strings = re.sub(
    r"('en':\s*\{)",
    r"\1\n" + en_additions,
    app_strings
)

with open('lib/core/app_strings.dart', 'w', encoding='utf-8') as f:
    f.write(app_strings)

print("Done! Keys generated and injected.")
