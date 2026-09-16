import re

# 1. Update recipe.dart enum
with open('lib/core/recipe.dart', 'r', encoding='utf-8') as f:
    r_text = f.read()

r_text = r_text.replace(
    "  swirl,      // Swirl instruction\n  press,",
    "  swirl,      // Swirl instruction\n  cap,        // Attach cap/plunger\n  flip,       // Flip Aeropress\n  press,"
)
with open('lib/core/recipe.dart', 'w', encoding='utf-8') as f:
    f.write(r_text)

# 2. Update brewing_screen.dart
with open('lib/screens/brewing_screen.dart', 'r', encoding='utf-8') as f:
    b_text = f.read()

# Audio
b_text = b_text.replace(
    "} else if (phase.action == PhaseAction.press) {",
    "} else if (phase.action == PhaseAction.cap) {\n      timerAudio.speak(lang == 'en' ? 'Attach the cap.' : 'Pasang tutup alat seduh.');\n    } else if (phase.action == PhaseAction.flip) {\n      timerAudio.speak(lang == 'en' ? 'Carefully flip the Aeropress.' : 'Balikkan alat seduh dengan hati-hati.');\n    } else if (phase.action == PhaseAction.press) {"
)
# Wait check
b_text = b_text.replace(
    "if (prevPhase.action == PhaseAction.stir || prevPhase.action == PhaseAction.swirl || prevPhase.action == PhaseAction.press) {",
    "if (prevPhase.action == PhaseAction.stir || prevPhase.action == PhaseAction.swirl || prevPhase.action == PhaseAction.press || prevPhase.action == PhaseAction.cap || prevPhase.action == PhaseAction.flip) {"
)
# currentPhaseText
b_text = b_text.replace(
    "} else if (phase.action == PhaseAction.press) {",
    "} else if (phase.action == PhaseAction.cap) {\n        currentPhaseText = lang == 'en' ? 'Attach cap' : 'Pasang Tutup';\n      } else if (phase.action == PhaseAction.flip) {\n        currentPhaseText = lang == 'en' ? 'Flip Aeropress' : 'Balikkan Alat';\n      } else if (phase.action == PhaseAction.press) {"
)
# itemText
b_text = b_text.replace(
    "} else if (p.action == PhaseAction.press) {",
    "} else if (p.action == PhaseAction.cap) {\n                        itemText = lang == 'en' ? 'Attach cap' : 'Pasang Tutup';\n                      } else if (p.action == PhaseAction.flip) {\n                        itemText = lang == 'en' ? 'Flip Aeropress' : 'Balikkan Alat';\n                      } else if (p.action == PhaseAction.press) {"
)

with open('lib/screens/brewing_screen.dart', 'w', encoding='utf-8') as f:
    f.write(b_text)

# 3. Update custom_recipe_screen.dart
with open('lib/screens/custom_recipe_screen.dart', 'r', encoding='utf-8') as f:
    c_text = f.read()

c_text = c_text.replace(
    "case PhaseAction.swirl: return lang == 'en' ? 'Swirl Brewer' : 'Swirl/Goyang Alat Seduh';",
    "case PhaseAction.swirl: return lang == 'en' ? 'Swirl Brewer' : 'Swirl/Goyang Alat Seduh';\n        case PhaseAction.cap: return lang == 'en' ? 'Attach Cap' : 'Pasang Tutup';\n        case PhaseAction.flip: return lang == 'en' ? 'Flip Aeropress' : 'Balikkan Alat';"
)

with open('lib/screens/custom_recipe_screen.dart', 'w', encoding='utf-8') as f:
    f.write(c_text)

print("UI and Enum updated with cap and flip.")
