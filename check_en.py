import re

with open("lib/core/app_strings.dart", "r", encoding="utf-8") as f:
    content = f.read()

en_block_match = re.search(r"('en': \{)(.*?)(\n    \},)", content, re.DOTALL)
en_text = en_block_match.group(2)

for line in en_text.split('\n'):
    if re.search(r"detik|menit|putaran|Tuang|Aduk|Tekan|Tunggu", line):
        print(line)

