import re

with open('lib/core/app_strings.dart', 'r', encoding='utf-8') as f:
    text = f.read()

id_part, en_part = text.split("'en': {", 1)

# Inverted:
inverted_ids = [18, 19, 45, 46]
# Standard:
standard_ids = [16, 17, 20, 21, 22, 23, 24, 47, 48, 49, 50, 51]
# Not sure: Alan Adler (desc 15 - wait desc 15 is standard?). Wait, Adler's original is standard. I'll just check all aeropress ones.
# Actually, I can just do a regex replace for the known aeropress desc keys:

# ID part
for i in inverted_ids:
    pattern = rf"('desc_key_{i}': ')(.*?)(',)"
    def repl(m):
        desc = m.group(2)
        if '[Metode:' not in desc:
            return m.group(1) + '[Metode: Inverted] ' + desc + m.group(3)
        return m.group(0)
    id_part = re.sub(pattern, repl, id_part)

for i in standard_ids:
    pattern = rf"('desc_key_{i}': ')(.*?)(',)"
    def repl(m):
        desc = m.group(2)
        if '[Metode:' not in desc:
            return m.group(1) + '[Metode: Standard] ' + desc + m.group(3)
        return m.group(0)
    id_part = re.sub(pattern, repl, id_part)

# EN part
for i in inverted_ids:
    pattern = rf"('desc_key_{i}': ')(.*?)(',)"
    def repl(m):
        desc = m.group(2)
        if '[Method:' not in desc:
            return m.group(1) + '[Method: Inverted] ' + desc + m.group(3)
        return m.group(0)
    en_part = re.sub(pattern, repl, en_part)

for i in standard_ids:
    pattern = rf"('desc_key_{i}': ')(.*?)(',)"
    def repl(m):
        desc = m.group(2)
        if '[Method:' not in desc:
            return m.group(1) + '[Method: Standard] ' + desc + m.group(3)
        return m.group(0)
    en_part = re.sub(pattern, repl, en_part)

text = id_part + "'en': {" + en_part
with open('lib/core/app_strings.dart', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated app_strings.dart with method tags.")
