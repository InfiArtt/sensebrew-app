import re

with open('lib/core/recipe.dart', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace empty extraIngredients with extra_key_7 for Tradisional Vietnam Drip
pattern = r'(name:\s*"Tradisional Vietnam Drip"[^}]+?extraIngredients:\s*""\s*,)'
def repl(m):
    return m.group(1).replace('extraIngredients: ""', 'extraIngredients: "extra_key_7"')

new_text = re.sub(pattern, repl, text, flags=re.DOTALL)

with open('lib/core/recipe.dart', 'w', encoding='utf-8') as f:
    f.write(new_text)
print("Added extra_key_7 to Tradisional Vietnam Drip")
