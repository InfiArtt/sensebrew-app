import re

with open('lib/screens/brewing_screen.dart', 'r', encoding='utf-8') as f:
    bt = f.read()

# Add handling for swirl in brewing_screen.dart
bt = bt.replace(
    "} else if (phase.action == PhaseAction.stir) {\n        timerAudio.speak(AppStrings.str(lang, 'stir_instruction') ?? 'Aduk.');",
    "} else if (phase.action == PhaseAction.stir) {\n        timerAudio.speak(AppStrings.str(lang, 'stir_instruction') ?? 'Aduk dengan sendok.');\n      } else if (phase.action == PhaseAction.swirl) {\n        timerAudio.speak(lang == 'en' ? 'Swirl the dripper.' : 'Goyangkan atau putar perlahan alat seduh.');"
)

bt = bt.replace(
    "if (prevPhase.action == PhaseAction.stir || prevPhase.action == PhaseAction.press) {",
    "if (prevPhase.action == PhaseAction.stir || prevPhase.action == PhaseAction.swirl || prevPhase.action == PhaseAction.press) {"
)

bt = bt.replace(
    "} else if (phase.action == PhaseAction.stir) {\n          currentPhaseText = AppStrings.str(lang, 'stir_instruction') ?? 'Aduk.';",
    "} else if (phase.action == PhaseAction.stir) {\n          currentPhaseText = AppStrings.str(lang, 'stir_instruction') ?? 'Aduk dengan sendok.';\n        } else if (phase.action == PhaseAction.swirl) {\n          currentPhaseText = lang == 'en' ? 'Swirl the dripper.' : 'Goyangkan/Swirl alat seduh.';"
)

bt = bt.replace(
    "} else if (p.action == PhaseAction.stir) {\n                          itemText = lang == 'en' ? 'Stir' : 'Aduk';",
    "} else if (p.action == PhaseAction.stir) {\n                          itemText = lang == 'en' ? 'Stir' : 'Aduk';\n                        } else if (p.action == PhaseAction.swirl) {\n                          itemText = lang == 'en' ? 'Swirl' : 'Swirl/Goyang';"
)

with open('lib/screens/brewing_screen.dart', 'w', encoding='utf-8') as f:
    f.write(bt)

with open('lib/screens/custom_recipe_screen.dart', 'r', encoding='utf-8') as f:
    ct = f.read()

ct = ct.replace(
    "case PhaseAction.stir: return AppStrings.str(lang, 'action_stir');",
    "case PhaseAction.stir: return AppStrings.str(lang, 'action_stir');\n        case PhaseAction.swirl: return lang == 'en' ? 'Swirl Dripper' : 'Swirl/Goyang Dripper';"
)

with open('lib/screens/custom_recipe_screen.dart', 'w', encoding='utf-8') as f:
    f.write(ct)

print("Updated brewing_screen and custom_recipe_screen")
