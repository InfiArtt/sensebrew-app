import re

with open('lib/core/recipe.dart', 'r', encoding='utf-8') as f:
    text = f.read()

# Fix WAC 2023
pattern_wac = r'(name:\s*"WAC 2023 Champion Recipe"[^}]+?RecipePhase\(startTimeSeconds: 15, action: PhaseAction\.wait\),)(.*?)(RecipePhase\(startTimeSeconds: 120, pourAmountMl: 80, action: PhaseAction\.pourCenter\),)'
def repl_wac(m):
    return m.group(1) + '\n            RecipePhase(startTimeSeconds: 90, action: PhaseAction.press),\n            RecipePhase(startTimeSeconds: 115, action: PhaseAction.wait),\n            ' + m.group(3)
text = re.sub(pattern_wac, repl_wac, text, flags=re.DOTALL)

# Fix Jonathan Gagne
pattern_jonathan = r'(name:\s*"Jonathan Gagne Long Steep"[^}]+?RecipePhase\(startTimeSeconds: 0, pourAmountMl: 300, action: PhaseAction\.pourCenter\),)\s*RecipePhase\(startTimeSeconds: 540, action: PhaseAction\.wait\),'
def repl_jonathan(m):
    return m.group(1) + '\n            RecipePhase(startTimeSeconds: 540, action: PhaseAction.press),'
text = re.sub(pattern_jonathan, repl_jonathan, text, flags=re.DOTALL)

with open('lib/core/recipe.dart', 'w', encoding='utf-8') as f:
    f.write(text)
print("Fixed WAC 2023 and Jonathan Gagne")
