import re

with open('lib/core/recipe.dart', 'r', encoding='utf-8') as f:
    content = f.read()

db_start = content.find('List<Recipe> recipeDatabase = [')
if db_start != -1:
    before = content[:db_start]
    after = content[db_start:]
    
    # regex replace Recipe( followed by whitespace and name:
    after = re.sub(r'Recipe\(\s+name:', 'Recipe(\n    isBuiltIn: true,\n    name:', after)
    
    with open('lib/core/recipe.dart', 'w', encoding='utf-8') as f:
        f.write(before + after)
    print("Replaced!")
else:
    print("Not found")
