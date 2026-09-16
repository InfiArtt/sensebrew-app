import re

with open('lib/core/app_strings.dart', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace all degree symbols back to capital A
content = content.replace("°", "A")

# Now, any number followed by AC should be °C. For example 90AC -> 90°C
content = re.sub(r'(\d+)AC', r'\1°C', content)

# Also fix 80C to 80°C if it exists without the degree symbol?
# No, let's just stick to fixing the AC.

with open('lib/core/app_strings.dart', 'w', encoding='utf-8') as f:
    f.write(content)
print("Restored ALL A characters!")
