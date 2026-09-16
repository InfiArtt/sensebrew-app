import re

with open('lib/core/recipe.dart', 'r', encoding='utf-8') as f:
    content = f.read()

pattern = r'(RecipePhase\(startTimeSeconds: (\d+), action: PhaseAction\.stir\),\s+)RecipePhase\(startTimeSeconds: (\d+), action: PhaseAction\.cap\),'

def repl(match):
    start1 = int(match.group(2))
    start2 = int(match.group(3))
    wait_start = start1 + 3
    return match.group(1) + f"RecipePhase(startTimeSeconds: {wait_start}, action: PhaseAction.wait),\n            RecipePhase(startTimeSeconds: {start2}, action: PhaseAction.cap),"

new_content = re.sub(pattern, repl, content)

with open('lib/core/recipe.dart', 'w', encoding='utf-8') as f:
    f.write(new_content)

print('Done')
