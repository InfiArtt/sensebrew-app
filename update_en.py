import re

with open('lib/core/app_strings.dart', 'r', encoding='utf-8') as f:
    content = f.read()

# I will write a smarter python script to update existing keys and add new ones inside the 'en' dict
en_start = content.find("'en': {")
en_end = content.find("  };", en_start)

en_block = content[en_start:en_end]

import json
with open('translated.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# we will just replace the value of existing keys in en_block or add them.
# actually, let's just parse en_block line by line
new_en_block_lines = []
for line in en_block.split('\n'):
    match = re.search(r"^\s*'((desc|extra)_key_\d+)':", line)
    if match:
        key = match.group(1)
        if key in data.get('desc', {}):
            val = data['desc'][key].replace("'", "\\'")
            new_en_block_lines.append(f"        '{key}': '{val}',")
        elif key in data.get('extra', {}):
            val = data['extra'][key].replace("'", "\\'")
            new_en_block_lines.append(f"        '{key}': '{val}',")
        else:
            new_en_block_lines.append(line)
    else:
        new_en_block_lines.append(line)

new_en_block = '\n'.join(new_en_block_lines)
new_content = content[:en_start] + new_en_block + content[en_end:]

with open('lib/core/app_strings.dart', 'w', encoding='utf-8') as f:
    f.write(new_content)
print("Updated en block cleanly!")
