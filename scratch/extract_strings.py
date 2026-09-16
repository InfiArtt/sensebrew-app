import re
import json

with open('lib/core/recipe.dart', 'r', encoding='utf-8') as f:
    recipe_code = f.read()

desc_matches = re.findall(r'description:\s*"(.*?)",', recipe_code)
extra_matches = re.findall(r'extraIngredients:\s*"(.*?)",', recipe_code)
name_matches = re.findall(r'name:\s*"(.*?)",', recipe_code)

strings_to_translate = list(set([s for s in desc_matches + extra_matches + name_matches if s.strip() != ""]))

with open('scratch/strings_to_translate.json', 'w', encoding='utf-8') as f:
    json.dump(strings_to_translate, f, ensure_ascii=False, indent=2)

print("Saved to strings_to_translate.json")
