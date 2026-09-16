import re

with open('lib/core/recipe.dart', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix Alan Adler totalWaterMl
content = re.sub(
    r'name:\s*"Alan Adler \(Original\)",(.*?totalWaterMl:\s*)200,',
    r'name: "Alan Adler (Original)",\160,',
    content,
    flags=re.DOTALL
)

with open('lib/core/recipe.dart', 'w', encoding='utf-8') as f:
    f.write(content)
