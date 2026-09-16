import re

with open('lib/core/recipe.dart', 'r', encoding='utf-8') as f:
    text = f.read()

recipes = re.split(r'Recipe\(', text)[1:]

for r in recipes:
    name_m = re.search(r'name:\s*"([^"]+)"', r)
    name = name_m.group(1) if name_m else "Unknown"
    
    phases_m = re.search(r'phases:\s*\[(.*?)\]', r, re.DOTALL)
    if not phases_m: continue
    
    phases_str = phases_m.group(1)
    phases = re.findall(r'RecipePhase\(([^)]+)\)', phases_str)
    
    parsed = []
    for p in phases:
        st_m = re.search(r'startTimeSeconds:\s*(\d+)', p)
        act_m = re.search(r'action:\s*PhaseAction\.(\w+)', p)
        if st_m and act_m:
            parsed.append({'start': int(st_m.group(1)), 'action': act_m.group(1), 'raw': p})
            
    for i in range(len(parsed)):
        p = parsed[i]
        if p['action'] in ['swirl', 'stir', 'cap', 'flip']:
            next_start = parsed[i+1]['start'] if i+1 < len(parsed) else None
            # Find total duration if no next phase
            if next_start is None:
                td_m = re.search(r'totalDurationSeconds:\s*(\d+)', r)
                next_start = int(td_m.group(1)) if td_m else p['start'] + 10
            
            diff = next_start - p['start']
            if diff > 20:
                print(f"[{name}] Warning: {p['action']} at {p['start']}s lasts for {diff}s! (Next phase at {next_start}s)")
