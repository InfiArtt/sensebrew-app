import re

with open('lib/core/app_strings.dart', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("\ufffdC", "°C")
content = content.replace("\ufffd", "A")

# Let's fix any over-replaced stuff: 
# C°C might happen? No, \ufffdC -> °C.
# BUKA -> BUKA (was BUK\ufffd -> BUKA)

with open('lib/core/app_strings.dart', 'w', encoding='utf-8') as f:
    f.write(content)
print("Fixed ghosts!")
