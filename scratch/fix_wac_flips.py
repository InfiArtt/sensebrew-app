import re

with open('lib/core/recipe.dart', 'r', encoding='utf-8') as f:
    text = f.read()

# Fix Carolina Ibarra
pattern_carolina = r'(name:\s*"W\.A\.C Carolina Ibarra \(2018\)"[^}]+?RecipePhase\(startTimeSeconds: 30, action: PhaseAction\.stir\),)(.*?)(RecipePhase\(startTimeSeconds: 60, action: PhaseAction\.press\),)'
def repl_carolina(m):
    return m.group(1) + '\n          RecipePhase(startTimeSeconds: 40, action: PhaseAction.cap),\n          RecipePhase(startTimeSeconds: 46, action: PhaseAction.wait),\n          RecipePhase(startTimeSeconds: 55, action: PhaseAction.flip),\n          ' + m.group(3)
text = re.sub(pattern_carolina, repl_carolina, text, flags=re.DOTALL)

# Fix Paulina Miczka
pattern_paulina = r'(name:\s*"W\.A\.C Paulina Miczka \(2017\)"[^}]+?RecipePhase\(startTimeSeconds: 35, action: PhaseAction\.stir\),)(.*?)(RecipePhase\(startTimeSeconds: 75, action: PhaseAction\.press\),)'
def repl_paulina(m):
    return m.group(1) + '\n          RecipePhase(startTimeSeconds: 45, action: PhaseAction.cap),\n          RecipePhase(startTimeSeconds: 51, action: PhaseAction.wait),\n          RecipePhase(startTimeSeconds: 70, action: PhaseAction.flip),\n          ' + m.group(3)
text = re.sub(pattern_paulina, repl_paulina, text, flags=re.DOTALL)

with open('lib/core/recipe.dart', 'w', encoding='utf-8') as f:
    f.write(text)

print("Fixed WAC 2018 and 2017 flip phases!")
