import re

with open('lib/core/app_strings.dart', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace all A\ufffdC with °C
content = content.replace("A\ufffdC", "°C")
content = content.replace("AC", "°C")
content = content.replace("A\xef\xbf\xbdC", "°C")

# Replace any remaining A\ufffd with A
content = content.replace("A\ufffd", "A")
content = content.replace("A", "A")
content = content.replace("A\xef\xbf\xbd", "A")

# Fix BUKA -> BUKA
content = content.replace("BUKA\ufffd", "BUKA")
content = content.replace("BUKA", "BUKA")

with open('lib/core/app_strings.dart', 'w', encoding='utf-8') as f:
    f.write(content)
print("Fixed!")
