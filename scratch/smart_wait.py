import re

with open('lib/core/recipe.dart', 'r', encoding='utf-8') as f:
    text = f.read()

# I will systematically find all 'Recipe(...)' blocks, analyze them, and rebuild their 'phases' array.
def fix_recipe_phases(match):
    recipe_str = match.group(0)
    
    phases_m = re.search(r'phases:\s*\[(.*?)\]', recipe_str, re.DOTALL)
    if not phases_m: return recipe_str
    
    phases_str_inner = phases_m.group(1)
    # Extract all phases
    phases_raw = re.findall(r'RecipePhase\([^)]+\)', phases_str_inner)
    
    parsed = []
    for raw in phases_raw:
        st_m = re.search(r'startTimeSeconds:\s*(\d+)', raw)
        act_m = re.search(r'action:\s*PhaseAction\.(\w+)', raw)
        if st_m and act_m:
            parsed.append({'start': int(st_m.group(1)), 'action': act_m.group(1), 'raw': raw})
            
    # Add wait phases where needed
    new_phases = []
    for i in range(len(parsed)):
        p = parsed[i]
        new_phases.append(p['raw'])
        
        if p['action'] in ['swirl', 'stir', 'cap', 'flip']:
            next_start = parsed[i+1]['start'] if i+1 < len(parsed) else None
            # Find total duration if no next phase
            if next_start is None:
                td_m = re.search(r'totalDurationSeconds:\s*(\d+)', recipe_str)
                next_start = int(td_m.group(1)) if td_m else p['start'] + 10
            
            diff = next_start - p['start']
            # If the next phase is another action more than 15 seconds away, insert a wait
            if diff > 15:
                # Wait 5 seconds after a swirl/cap/flip, 10 seconds after stir
                wait_time = p['start'] + (10 if p['action'] == 'stir' else 5)
                # Ensure we don't insert a wait if one already exists there
                exists = any(x['start'] == wait_time for x in parsed)
                if not exists:
                    new_phases.append(f"RecipePhase(startTimeSeconds: {wait_time}, action: PhaseAction.wait)")

    # Join new phases
    new_phases_str = ',\n        '.join(new_phases)
    # Rebuild phases array
    new_recipe_str = recipe_str[:phases_m.start(1)] + "\n        " + new_phases_str + ",\n      " + recipe_str[phases_m.end(1):]
    return new_recipe_str

new_text = re.sub(r'Recipe\([^)]+phases:\s*\[.*?\][^)]*\)', fix_recipe_phases, text, flags=re.DOTALL)

with open('lib/core/recipe.dart', 'w', encoding='utf-8') as f:
    f.write(new_text)

print("Smart injected wait phases!")
