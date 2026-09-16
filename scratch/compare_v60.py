import re

with open('lib/core/recipe.dart', 'r', encoding='utf-8') as f:
    text = f.read()

def print_recipe(name):
    match = re.search(r'name:\s*"' + re.escape(name) + r'".*?phases:\s*\[(.*?)\]', text, re.DOTALL)
    if match:
        print(f'--- {name} ---')
        phases = match.group(1).strip()
        for p in phases.split('\n'):
            if p.strip():
                print(p.strip())

print_recipe('James Hoffmann Ultimate V60')
print_recipe('Orea V3/Kalita Wave')
print_recipe('V60 Dark Roast (Low Temp)')
print_recipe('Scott Rao V60')
print_recipe('Hario Official V60')
print_recipe('Clever Dripper / Full Immersion')
