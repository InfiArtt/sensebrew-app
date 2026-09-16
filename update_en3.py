import re
import json

with open("translated_new.json", "r", encoding="utf-8") as f:
    translated_data = json.load(f)

with open("lib/core/app_strings.dart", "r", encoding="utf-8") as f:
    content = f.read()

# The 'en' block starts with: 'en': {
# Let's find it.
en_block_match = re.search(r"'en': \{(.*?)\n    \}(,|)", content, re.DOTALL)
if not en_block_match:
    print("Could not find en block")
    exit(1)

en_text = en_block_match.group(1)

# we will replace each key in en_text if it is in translated_data
new_en_text = en_text
for key, val in translated_data.items():
    # we need to be careful with escaping
    # the existing text might have newlines \n
    # let's just find the line with 'key': '...'
    # it can span multiple lines because of \n
    
    # an easier way: just parse the Dart Map? No, it's Dart.
    # regex to find 'key': '... value ...' where value might contain escaped quotes or newlines.
    
    # Actually, the values we are replacing are the INDONESIAN ones which are currently in the en_text!
    # Let's find: 'key': 'something', (could be multiline)
    pattern = rf"('{key}': ')(.*?)(',\n|'\n)"
    
    # replacement
    # escape single quotes in val
    safe_val = val.replace("'", "\\'")
    # replace literal newlines with \n 
    safe_val = safe_val.replace('\n', '\\n')
    
    new_en_text = re.sub(pattern, rf"\g<1>{safe_val}\g<3>", new_en_text, flags=re.DOTALL)

# replace in content
content = content.replace(en_text, new_en_text)

with open("lib/core/app_strings.dart", "w", encoding="utf-8") as f:
    f.write(content)

print("Updated app_strings.dart successfully!")
