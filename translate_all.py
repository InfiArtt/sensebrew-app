import re
import json
import os
import google.genai as genai
from google.genai import types

with open('lib/core/app_strings.dart', 'r', encoding='utf-8') as f:
    content = f.read()

id_block_match = re.search(r"'id': \{(.*?)\n    \},", content, re.DOTALL)
id_text = id_block_match.group(1)

data_to_translate = {}
for line in id_text.split('\n'):
    m = re.search(r"'(desc_key_\d+|extra_key_\d+)': '(.*?)',", line)
    if m:
        data_to_translate[m.group(1)] = m.group(2)

print(f"Found {len(data_to_translate)} keys to translate.")

client = genai.Client()
prompt = "Translate the following Indonesian coffee brewing descriptions to English. Ensure the terminology is professional (e.g., 'grind size', 'bloom', 'yield'). Output the result as a valid JSON object mapping keys to translated strings. Input data:\n" + json.dumps(data_to_translate, indent=2)

response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=prompt,
    config=types.GenerateContentConfig(
        response_mime_type="application/json",
    )
)

translated_data = json.loads(response.text)
with open('translated_new.json', 'w', encoding='utf-8') as f:
    json.dump(translated_data, f, indent=2, ensure_ascii=False)
print(f"Translated {len(translated_data)} keys.")
