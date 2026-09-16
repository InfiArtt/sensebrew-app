import re

with open('lib/core/recipe.dart', 'r', encoding='utf-8') as f:
    text = f.read()

out_text = ""
def print_method_recipes(method):
    global out_text
    out_text += f"\n============= {method.upper()} =============\n"
    for match in re.finditer(r'  Recipe\(\s*name:\s*"([^"]+)",\s*description:\s*"([^"]+)",.*?method:\s*BrewMethod\.' + method + r'.*?phases:\s*\[(.*?)\]', text, re.DOTALL):
        name = match.group(1)
        desc = match.group(2)
        phases = match.group(3).strip()
        out_text += f"--- {name} ---\n"
        out_text += f"Desc: {desc}\n"
        for p in phases.split('\n'):
            if p.strip():
                out_text += "  " + p.strip() + "\n"

print_method_recipes('frenchPress')
print_method_recipes('aeropress')
print_method_recipes('vietnamDrip')
print_method_recipes('cupping')

with open('scratch/dump_others.txt', 'w', encoding='utf-8') as f:
    f.write(out_text)
print("Done dumping to scratch/dump_others.txt")
