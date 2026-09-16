import json

with open('lib/core/app_strings.dart', 'r', encoding='utf-8') as f:
    text = f.read()

en_part = text.split("'en': {")[1]

# Check for common ID words in EN section
id_words = [" dan ", " yang ", " dengan ", " untuk ", " air ", " kopi ", " seduh "]

for i in range(58):
    key = f"'desc_key_{i}': '"
    if key in en_part:
        start_idx = en_part.find(key) + len(key)
        end_idx = en_part.find("',", start_idx)
        val = en_part[start_idx:end_idx]
        
        found_words = [w for w in id_words if w in val.lower()]
        if found_words:
            print(f"ID words in EN {key.strip()}: {found_words}")
            print(val)
            print("-" * 40)
