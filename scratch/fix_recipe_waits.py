import re

with open("lib/core/recipe.dart", "r", encoding="utf-8") as f:
    text = f.read()

# Fix WAC 2023 missing press and wrong wait
text = text.replace(
"""          RecipePhase(startTimeSeconds: 10, action: PhaseAction.swirl),
          RecipePhase(startTimeSeconds: 90, action: PhaseAction.wait),
          RecipePhase(startTimeSeconds: 120, pourAmountMl: 80, action: PhaseAction.pourCenter),
        ],""",
"""          RecipePhase(startTimeSeconds: 10, action: PhaseAction.swirl),
          RecipePhase(startTimeSeconds: 15, action: PhaseAction.wait),
          RecipePhase(startTimeSeconds: 120, pourAmountMl: 80, action: PhaseAction.pourCenter),
          RecipePhase(startTimeSeconds: 140, action: PhaseAction.wait),
          RecipePhase(startTimeSeconds: 150, action: PhaseAction.press),
        ],""")

# Fix Tim Wendelboe French Press
text = text.replace(
"""          RecipePhase(startTimeSeconds: 240, action: PhaseAction.stir),
      ),""",
"""          RecipePhase(startTimeSeconds: 240, action: PhaseAction.stir),
          RecipePhase(startTimeSeconds: 250, action: PhaseAction.wait),
          RecipePhase(startTimeSeconds: 570, action: PhaseAction.press),
        ],
      ),""")

# Fix Aeropress Espresso (Faux-Presso)
text = text.replace(
"""          RecipePhase(startTimeSeconds: 10, action: PhaseAction.swirl),
      ),""",
"""          RecipePhase(startTimeSeconds: 10, action: PhaseAction.swirl),
          RecipePhase(startTimeSeconds: 15, action: PhaseAction.wait),
          RecipePhase(startTimeSeconds: 60, action: PhaseAction.press),
        ],
      ),""")

# Fix Inverted Classic
text = text.replace(
"""        RecipePhase(startTimeSeconds: 90, action: PhaseAction.flip),
        RecipePhase(startTimeSeconds: 120, action: PhaseAction.press),""",
"""        RecipePhase(startTimeSeconds: 90, action: PhaseAction.flip),
        RecipePhase(startTimeSeconds: 95, action: PhaseAction.wait),
        RecipePhase(startTimeSeconds: 120, action: PhaseAction.press),""")

# Fix Aeropress Espresso Concentrate
text = text.replace(
"""        RecipePhase(startTimeSeconds: 70, action: PhaseAction.flip),
        RecipePhase(startTimeSeconds: 90, action: PhaseAction.press),""",
"""        RecipePhase(startTimeSeconds: 70, action: PhaseAction.flip),
        RecipePhase(startTimeSeconds: 75, action: PhaseAction.wait),
        RecipePhase(startTimeSeconds: 90, action: PhaseAction.press),""")

# Fix Tuomas Merikanto
text = text.replace(
"""        RecipePhase(startTimeSeconds: 10, action: PhaseAction.swirl),
        RecipePhase(startTimeSeconds: 45, pourAmountMl: 150, action: PhaseAction.pourCenter),""",
"""        RecipePhase(startTimeSeconds: 10, action: PhaseAction.swirl),
        RecipePhase(startTimeSeconds: 15, action: PhaseAction.wait),
        RecipePhase(startTimeSeconds: 45, pourAmountMl: 150, action: PhaseAction.pourCenter),""")

# Fix Aeropress Flow Control
text = text.replace(
"""        RecipePhase(startTimeSeconds: 30, action: PhaseAction.stir),
        RecipePhase(startTimeSeconds: 120, action: PhaseAction.press),""",
"""        RecipePhase(startTimeSeconds: 30, action: PhaseAction.stir),
        RecipePhase(startTimeSeconds: 40, action: PhaseAction.wait),
        RecipePhase(startTimeSeconds: 120, action: PhaseAction.press),""")

# Fix Aeropress Espresso Fake
text = text.replace(
"""        RecipePhase(startTimeSeconds: 20, action: PhaseAction.stir),
        RecipePhase(startTimeSeconds: 60, action: PhaseAction.press),""",
"""        RecipePhase(startTimeSeconds: 20, action: PhaseAction.stir),
        RecipePhase(startTimeSeconds: 30, action: PhaseAction.wait),
        RecipePhase(startTimeSeconds: 60, action: PhaseAction.press),""")

# Fix Aeropress Robusta Sweet
text = text.replace(
"""        RecipePhase(startTimeSeconds: 30, action: PhaseAction.stir),
        RecipePhase(startTimeSeconds: 90, action: PhaseAction.press),""",
"""        RecipePhase(startTimeSeconds: 30, action: PhaseAction.stir),
        RecipePhase(startTimeSeconds: 40, action: PhaseAction.wait),
        RecipePhase(startTimeSeconds: 90, action: PhaseAction.press),""")

# Fix W.A.C Carolina Ibarra (2018)
text = text.replace(
"""        RecipePhase(startTimeSeconds: 30, action: PhaseAction.stir),
        RecipePhase(startTimeSeconds: 60, action: PhaseAction.press),""",
"""        RecipePhase(startTimeSeconds: 30, action: PhaseAction.stir),
        RecipePhase(startTimeSeconds: 45, action: PhaseAction.wait),
        RecipePhase(startTimeSeconds: 60, action: PhaseAction.press),""")

# Fix W.A.C Paulina Miczka (2017)
text = text.replace(
"""        RecipePhase(startTimeSeconds: 35, action: PhaseAction.stir),
        RecipePhase(startTimeSeconds: 75, action: PhaseAction.press),""",
"""        RecipePhase(startTimeSeconds: 35, action: PhaseAction.stir),
        RecipePhase(startTimeSeconds: 45, action: PhaseAction.wait),
        RecipePhase(startTimeSeconds: 75, action: PhaseAction.press),""")

with open("lib/core/recipe.dart", "w", encoding="utf-8") as f:
    f.write(text)

print("Fixed missing waits and press actions in recipe.dart.")
