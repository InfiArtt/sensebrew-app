with open('lib/core/app_strings.dart', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("A\ufffd", "A")
content = content.replace("A", "A")
content = content.replace("", "") # remove any remaining replacement chars
content = content.replace("AC", "°C")

with open('lib/core/app_strings.dart', 'w', encoding='utf-8') as f:
    f.write(content)
