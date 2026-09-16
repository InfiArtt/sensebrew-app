import re
import json

with open("lib/core/app_strings.dart", "r", encoding="utf-8") as f:
    content = f.read()

id_block_match = re.search(r"('id': \{)(.*?)(\n    \},)", content, re.DOTALL)
id_text = id_block_match.group(2)

# To parse it safely, let's use a regex that matches keys and values.
# A key is 'key_name': 
# A value is '...' followed by , or end of block.
# Since Dart strings can contain \n, we must match up to the next key or end of string.

pattern = r"^\s*'([^']+)':\s*'(.*?)'(?:,|\s*$)"
# This won't work for multiline strings if we use ^\s* with MULTILINE because the value has \n in it.

# Let's split by "': '"
# This is tricky. Let's just use a simple state machine to parse the dart map.
data = {}
lines = id_text.split('\n')
current_key = None
current_val = []

for line in lines:
    m = re.match(r"^\s*'([^']+)':\s*'(.*)", line)
    if m:
        if current_key is not None:
            # We missed the end of the previous string? No, a new key means the previous string ended on the line before.
            pass
        current_key = m.group(1)
        val_start = m.group(2)
        if val_start.endswith("',"):
            data[current_key] = val_start[:-2]
            current_key = None
        elif val_start.endswith("'"):
            data[current_key] = val_start[:-1]
            current_key = None
        else:
            current_val.append(val_start)
    else:
        if current_key is not None:
            if line.endswith("',"):
                current_val.append(line[:-2])
                data[current_key] = '\n'.join(current_val)
                current_key = None
                current_val = []
            elif line.endswith("'"):
                current_val.append(line[:-1])
                data[current_key] = '\n'.join(current_val)
                current_key = None
                current_val = []
            else:
                current_val.append(line)

with open("full_id.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
print(f"Extracted {len(data)} keys.")
