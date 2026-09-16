import re
import json

with open("lib/core/app_strings.dart", "r", encoding="utf-8") as f:
    content = f.read()

en_block_match = re.search(r"('en': \{)(.*?)(\n    \},)", content, re.DOTALL)
en_text = en_block_match.group(2)

id_block_match = re.search(r"('id': \{)(.*?)(\n    \},)", content, re.DOTALL)
id_text = id_block_match.group(2)

id_keys = set()
for line in id_text.split('\n'):
    m = re.search(r"^\s*'([^']+)':", line)
    if m: id_keys.add(m.group(1))

en_keys = set()
for line in en_text.split('\n'):
    m = re.search(r"^\s*'([^']+)':", line)
    if m: en_keys.add(m.group(1))

print("Total keys in ID:", len(id_keys))
print("Total keys in EN:", len(en_keys))

# let's just find the exact lines in ID that are identically present in EN
# which means they are untranslated.
untranslated = []
for k in id_keys:
    # get value in ID
    id_val_m = re.search(rf"^\s*'{k}': '(.*?)',?$", id_text, re.MULTILINE)
    en_val_m = re.search(rf"^\s*'{k}': '(.*?)',?$", en_text, re.MULTILINE)
    if id_val_m and en_val_m:
        if id_val_m.group(1) == en_val_m.group(1):
            untranslated.append(k)

print(f"Found {len(untranslated)} untranslated keys:")
for k in untranslated:
    print(k, ":", id_val_m.group(1)[:50]) # just printing the key to see what they are

