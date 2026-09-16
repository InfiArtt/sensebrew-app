import re

with open('lib/core/recipe.dart', 'r', encoding='utf-8') as f:
    text = f.read()

def insert_phase(recipe_name, search_phase, new_phase):
    global text
    pattern = r'(name: "' + recipe_name + r'".*?' + search_phase.replace('(', r'\(').replace(')', r'\)') + r')'
    text = re.sub(pattern, r'\1\n      ' + new_phase + ',', text, flags=re.DOTALL)

# 1. James Hoffmann V60 (Add waits after swirl)
insert_phase("James Hoffmann Ultimate V60", "PhaseAction.swirl),", "RecipePhase(startTimeSeconds: 15, action: PhaseAction.wait)")
insert_phase("James Hoffmann Ultimate V60", "PhaseAction.swirl),", "RecipePhase(startTimeSeconds: 110, action: PhaseAction.wait)") # 2nd swirl is at 105s

# 2. Clever Dripper (Add wait after stir)
insert_phase("Clever Dripper / Full Immersion", "PhaseAction.stir),", "RecipePhase(startTimeSeconds: 40, action: PhaseAction.wait)")

# 4. Scott Rao V60 (Add wait after swirl)
insert_phase("Scott Rao V60", "startTimeSeconds: 5, action: PhaseAction.swirl),", "RecipePhase(startTimeSeconds: 10, action: PhaseAction.wait)")
insert_phase("Scott Rao V60", "startTimeSeconds: 90, action: PhaseAction.swirl),", "RecipePhase(startTimeSeconds: 95, action: PhaseAction.wait)")

# 5. Japanese Iced Coffee (Add extraIngredients)
text = text.replace(
    'name: "Japanese Iced Coffee (Fruity)",\n      description:',
    'name: "Japanese Iced Coffee (Fruity)",\n      description:'
) # wait, let's just use regex for both
text = re.sub(
    r'(name: "Japanese Iced Coffee \(Fruity\)".*?totalWaterMl: 150,)',
    r'\1\n      extraIngredients: "100 gram es batu",',
    text, flags=re.DOTALL
)
text = re.sub(
    r'(name: "Japanese Iced Coffee \(Sweet\)".*?totalWaterMl: 150,)',
    r'\1\n      extraIngredients: "100 gram es batu",',
    text, flags=re.DOTALL
)

# 6. Yoshua Tanu (Add wait after swirl)
insert_phase("Yoshua Tanu Fast Flow", "startTimeSeconds: 5, action: PhaseAction.swirl),", "RecipePhase(startTimeSeconds: 10, action: PhaseAction.wait)")
insert_phase("Yoshua Tanu Fast Flow", "startTimeSeconds: 80, action: PhaseAction.swirl),", "RecipePhase(startTimeSeconds: 85, action: PhaseAction.wait)")

# 7. Lance Hedrick French Press (Add stir and wait)
insert_phase("Lance Hedrick French Press", "startTimeSeconds: 0, pourAmountMl: 500, action: PhaseAction.pourCenter),", "RecipePhase(startTimeSeconds: 30, action: PhaseAction.stir),\n      RecipePhase(startTimeSeconds: 40, action: PhaseAction.wait)")

# 8. French Press Cold Water Bloom
match = re.search(r'(name: "French Press Cold Water Bloom".*?phases: \[)(.*?)(\],)', text, re.DOTALL)
if match:
    phases = match.group(2)
    phases = phases.replace('PhaseAction.pourCircle', 'PhaseAction.pourCenter')
    phases = phases.replace('PhaseAction.wait),', 'PhaseAction.press),') # Change wait at 300 to press
    text = text[:match.start()] + match.group(1) + phases + match.group(3) + text[match.end():]

# 9. Traditional French Press (Add wait after stir)
insert_phase("Traditional French Press", "PhaseAction.stir),", "RecipePhase(startTimeSeconds: 70, action: PhaseAction.wait)")

# 10. Cafe au Lait
text = re.sub(
    r'(name: "Cafe au Lait \(Strong French Press\)".*?totalWaterMl: \d+,)',
    r'\1\n      extraIngredients: "Susu panas secukupnya (ditambahkan di gelas)",',
    text, flags=re.DOTALL
)
insert_phase("Cafe au Lait (Strong French Press)", "PhaseAction.stir),", "RecipePhase(startTimeSeconds: 70, action: PhaseAction.wait)")

# 11. Tim Wendelboe French Press
match2 = re.search(r'(name: "Tim Wendelboe French Press".*?phases: \[)(.*?)(\],)', text, re.DOTALL)
if match2:
    phases2 = match2.group(2)
    phases2 = phases2.replace('PhaseAction.wait),', 'PhaseAction.press),') # Change 540s wait to press
    text = text[:match2.start()] + match2.group(1) + phases2 + match2.group(3) + text[match2.end():]
insert_phase("Tim Wendelboe French Press", "PhaseAction.stir),", "RecipePhase(startTimeSeconds: 250, action: PhaseAction.wait)")

# 13. Alan Adler Aeropress
text = re.sub(
    r'(name: "Alan Adler \(Original\)".*?)coffeeGrams: 15, totalWaterMl: 200,',
    r'\1coffeeGrams: 15, totalWaterMl: 60,\n      extraIngredients: "Air panas/es tambahan untuk mengencerkan (Bypass)",',
    text, flags=re.DOTALL
)
text = re.sub(
    r'(name: "Alan Adler \(Original\)".*?startTimeSeconds: 0, pourAmountMl: )200',
    r'\g<1>60',
    text, flags=re.DOTALL
)
insert_phase("Alan Adler (Original)", "PhaseAction.stir),", "RecipePhase(startTimeSeconds: 20, action: PhaseAction.wait)")

# 14. Fix James Hoffmann French press (Add wait after stir)
insert_phase("James Hoffmann French Press", "PhaseAction.stir),", "RecipePhase(startTimeSeconds: 250, action: PhaseAction.wait)")


with open('lib/core/recipe.dart', 'w', encoding='utf-8') as f:
    f.write(text)

print("Applied fixes to recipes!")
