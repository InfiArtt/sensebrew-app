import re

with open('lib/core/recipe.dart', 'r', encoding='utf-8') as f:
    text = f.read()

# Find all phases lists
recipe_pattern = r'phases:\s*\[(.*?)\]\s*,'

def sort_phases(match):
    phases_str = match.group(1)
    
    # Extract individual phases
    phases = re.findall(r'RecipePhase\([^)]+\)', phases_str)
    
    # Sort them by startTimeSeconds
    def get_start_time(p):
        m = re.search(r'startTimeSeconds:\s*(\d+)', p)
        return int(m.group(1)) if m else 0
        
    sorted_phases = sorted(phases, key=get_start_time)
    
    # Reconstruct the phases block
    return 'phases: [\n        ' + ',\n        '.join(sorted_phases) + ',\n      ],'

new_text = re.sub(recipe_pattern, sort_phases, text, flags=re.DOTALL)

if new_text != text:
    with open('lib/core/recipe.dart', 'w', encoding='utf-8') as f:
        f.write(new_text)
    print("Sorted out of order phases!")
else:
    print("No out of order phases found.")
