import re

with open('lib/core/recipe.dart', 'r', encoding='utf-8') as f:
    text = f.read()

# First extract just the array part
db_match = re.search(r'List<Recipe>\s*recipeDatabase\s*=\s*\[(.*?)\];', text, re.DOTALL)
if not db_match:
    print("Could not find recipeDatabase")
    exit(1)

db_content = db_match.group(1)

# Now find all Recipe(...) blocks
# A robust way is to just find 'Recipe(' and match braces, but regex can do it if we are careful
matches = re.finditer(r'Recipe\(\s*name:\s*"([^"]+)",\s*description:\s*"([^"]+)",', db_content, re.DOTALL)

print("ALL RECIPES:")
for i, m in enumerate(matches):
    print(f"{i}: {m.group(1)}")
    print(f"  Desc: {m.group(2)}")
