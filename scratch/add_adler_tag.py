import re

with open('lib/core/app_strings.dart', 'r', encoding='utf-8') as f:
    text = f.read()

id_part, en_part = text.split("'en': {", 1)

# Standard:
standard_ids = [15]

# ID part
for i in standard_ids:
    pattern = rf"('desc_key_{i}': ')(.*?)(',)"
    def repl(m):
        desc = m.group(2)
        if '[Metode:' not in desc:
            return m.group(1) + '[Metode: Standard] ' + desc + m.group(3)
        return m.group(0)
    id_part = re.sub(pattern, repl, id_part)

# EN part
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

print("Updated app_strings.dart with Adler.")
