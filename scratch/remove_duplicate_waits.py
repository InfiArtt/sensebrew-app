import re

with open('lib/core/recipe.dart', 'r', encoding='utf-8') as f:
    text = f.read()

parts = text.split("Recipe(")
new_parts = [parts[0]]

for r in parts[1:]:
    phases_m = re.search(r'phases:\s*\[(.*?)\]', r, re.DOTALL)
    if not phases_m:
        new_parts.append(r)
        continue
        
    phases_str = phases_m.group(1)
    phases_raw = re.findall(r'RecipePhase\([^)]+\)', phases_str)
    
    parsed = []
    for raw in phases_raw:
        st_m = re.search(r'startTimeSeconds:\s*(\d+)', raw)
        act_m = re.search(r'action:\s*PhaseAction\.(\w+)', raw)
        if st_m and act_m:
            parsed.append({'start': int(st_m.group(1)), 'action': act_m.group(1), 'raw': raw})
            
    # Remove exact duplicates or back-to-back waits
    new_phases = []
    for i, p in enumerate(parsed):
        is_duplicate = False
        if p['action'] == 'wait':
            # Check if there is another wait within 2 seconds before this one
            for existing in new_phases:
                if existing['action'] == 'wait' and abs(existing['start'] - p['start']) <= 2:
                    is_duplicate = True
                    break
        if not is_duplicate:
            new_phases.append(p)
            
    # Reconstruct
    def get_start(phase):
        return phase['start']
    new_phases.sort(key=get_start)
    
    new_phases_str = ',\n          '.join([p['raw'] for p in new_phases])
    new_r = r[:phases_m.start(1)] + "\n          " + new_phases_str + ",\n        " + r[phases_m.end(1):]
    new_parts.append(new_r)

with open('lib/core/recipe.dart', 'w', encoding='utf-8') as f:
    f.write("Recipe(".join(new_parts))
print("Removed duplicate wait phases!")
