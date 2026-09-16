import re
import json

with open('lib/core/app_strings.dart', 'r', encoding='utf-8') as f:
    content = f.read()

id_block_match = re.search(r"'id': \{(.*?)\n    \},", content, re.DOTALL)
id_text = id_block_match.group(1)

data_to_translate = {}
for line in id_text.split('\n'):
    m = re.search(r"'(desc_key_\d+|extra_key_\d+)': '(.*?)',", line)
    if m:
        data_to_translate[m.group(1)] = m.group(2)

with open('id_data.json', 'w', encoding='utf-8') as f:
    json.dump(data_to_translate, f, indent=2)
