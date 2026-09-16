import re
import json

with open('lib/core/app_strings.dart', 'r', encoding='utf-8') as f:
    text = f.read()

# Extract the 'id' dictionary
id_match = re.search(r"'id': \{(.*?)\n    \}", text, re.DOTALL)
id_str = id_match.group(1)

# Find all keys
keys = re.findall(r"'([^']+)':\s*'(.*?)'", id_str)

ui_keys = {}
for k, v in keys:
    if not k.startswith('desc_') and not k.startswith('extra_'):
        ui_keys[k] = v

with open('scratch/ui_keys.json', 'w', encoding='utf-8') as f:
    json.dump(ui_keys, f, indent=4)
