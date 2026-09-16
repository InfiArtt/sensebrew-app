import re

with open('lib/core/recipe.dart', 'r', encoding='utf-8') as f:
    text = f.read()

# I will systematically find all 'Recipe(' blocks, analyze them, and rebuild their 'phases' array.
# Let's split by 'Recipe(' but be careful about the first part of the file.

parts = text.split("Recipe(")
new_parts = [parts[0]]

for r in parts[1:]:
    # Find phases array
    phases_m = re.search(r'phases:\s*\[(.*?)\]', r, re.DOTALL)
    if not phases_m:
        new_parts.append(r)
        continue
        
    phases_str_inner = phases_m.group(1)
    phases_raw = re.findall(r'RecipePhase\([^)]+\)', phases_str_inner)
    
    parsed = []
    for raw in phases_raw:
        st_m = re.search(r'startTimeSeconds:\s*(\d+)', raw)
        act_m = re.search(r'action:\s*PhaseAction\.(\w+)', raw)
        if st_m and act_m:
            parsed.append({'start': int(st_m.group(1)), 'action': act_m.group(1), 'raw': raw})
            
    new_phases = []
    for i in range(len(parsed)):
        p = parsed[i]
        new_phases.append(p['raw'])
        
        if p['action'] in ['swirl', 'stir', 'cap', 'flip']:
            next_start = parsed[i+1]['start'] if i+1 < len(parsed) else None
            # Find total duration if no next phase
            if next_start is None:
                td_m = re.search(r'totalDurationSeconds:\s*(\d+)', r)
                next_start = int(td_m.group(1)) if td_m else p['start'] + 10
            
            diff = next_start - p['start']
            if diff > 15:
                wait_time = p['start'] + (10 if p['action'] == 'stir' else 5)
                # Only insert if no phase exists at this exact time
                exists = any(x['start'] == wait_time for x in parsed)
                if not exists:
                    new_phases.append(f"RecipePhase(startTimeSeconds: {wait_time}, action: PhaseAction.wait)")

    # Sort the new phases array properly
    def get_start(phase_str):
        m = re.search(r'startTimeSeconds:\s*(\d+)', phase_str)
        return int(m.group(1)) if m else 0
    new_phases.sort(key=get_start)

    new_phases_str = ',\n        '.join(new_phases)
    new_r = r[:phases_m.start(1)] + "\n        " + new_phases_str + ",\n      " + r[phases_m.end(1):]
    new_parts.append(new_r)

with open('lib/core/recipe.dart', 'w', encoding='utf-8') as f:
    f.write("Recipe(".join(new_parts))

print("Smart injected wait phases AND sorted them!")
