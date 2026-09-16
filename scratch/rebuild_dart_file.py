import re
import codecs

with open('backup_recipe.dart', 'r', encoding='utf-16') as f:
    text = f.read()

header = text[:text.find('List<Recipe> recipeDatabase = [')]
body = text[text.find('List<Recipe> recipeDatabase = ['):]

# Extract all recipes using regex. 
# We'll split by "Recipe(" and then match matching braces.
# Actually, since it's hard to parse matching braces in standard regex, let's use a simpler approach:
# Split by "\n    Recipe("
recipes_raw = re.split(r'\r?\n\s+Recipe\(', body)
header_body = recipes_raw[0] # contains "const List<Recipe> recipeDatabase = ["

parsed_recipes = []
for i in range(1, len(recipes_raw)):
    block = "Recipe(" + recipes_raw[i]
    if block.endswith("];"):
        block = block[:-2].strip()
    if block.endswith("];\n"):
        block = block[:-3].strip()
    if block.endswith(",\n"):
        block = block[:-2]
    if block.endswith(","):
        block = block[:-1]
    
    # Check method
    method_match = re.search(r'method:\s*BrewMethod\.(\w+)', block)
    if method_match:
        method = method_match.group(1)
        if method == 'coldBrew':
            continue # drop cold brew
            
        # Determine beanType based on existing block logic
        if "beanType:" not in block:
            # Inject beanType right before phases:
            name_match = re.search(r'name:\s*"([^"]+)"', block)
            desc_match = re.search(r'description:\s*"([^"]+)"', block)
            
            name = name_match.group(1).lower() if name_match else ""
            desc = desc_match.group(1).lower() if desc_match else ""
            
            bean = "Arabica"
            if method == "vietnamDrip":
                bean = "Robusta"
                if "arabica" in name or "arabica" in desc: bean = "Arabica"
                if "blend" in name: bean = "Blend"
            elif method == "cupping":
                bean = "Bebas"
                if "robusta" in name: bean = "Robusta"
                if "arabica" in name: bean = "Arabica"
            else:
                if "robusta" in name: bean = "Robusta"
                if "blend" in name or "campur" in desc: bean = "Blend"
                if "excelsa" in name: bean = "Excelsa"
                if "liberica" in name: bean = "Liberica"
                if "decaf" in name: bean = "Bebas"
                if "spiced" in name: bean = "Bebas"
                
            # Replace targetGrindSizeMicrons to also append beanType
            block = re.sub(r'(targetGrindSizeMicrons:\s*\d+,)', r"\1\n      beanType: '" + bean + "',", block)
            
        parsed_recipes.append("    " + block + ",")

with codecs.open('scratch/new_db.txt', 'r', encoding='utf-8') as f:
    new_recipes = f.read()

# Build final output
final_out = header + header_body
for r in parsed_recipes:
    final_out += "\n" + r

final_out += "\n" + new_recipes + "\n  ];\n"

with codecs.open('lib/core/recipe.dart', 'w', encoding='utf-8') as f:
    f.write(final_out)

print("Rewrite complete. Total old recipes kept: " + str(len(parsed_recipes)))
