import re

with open("lib/screens/brewing_screen.dart", "r", encoding="utf-8") as f:
    text = f.read()

# _speakPhaseInstruction replacements
text = re.sub(
    r"timerAudio\.speak\([^;]*'Swirl the brewer\.'[^;]*\);",
    r"timerAudio.speak(AppStrings.str(lang, 'action_swirl'));",
    text
)
text = re.sub(
    r"timerAudio\.speak\([^;]*'Attach the cap\.'[^;]*\);",
    r"timerAudio.speak(AppStrings.str(lang, 'action_cap'));",
    text
)
text = re.sub(
    r"timerAudio\.speak\([^;]*'Flip the brewer\.'[^;]*\);",
    r"timerAudio.speak(AppStrings.str(lang, 'action_flip'));",
    text
)
text = re.sub(
    r"timerAudio\.speak\([^;]*'Stop and wait\.'[^;]*\);",
    r"timerAudio.speak(AppStrings.str(lang, 'action_wait'));",
    text
)
text = re.sub(
    r"timerAudio\.speak\(AppStrings\.str\(lang, 'stir_instruction'\)\s*\?\?\s*'[^']*'\);",
    r"timerAudio.speak(AppStrings.str(lang, 'stir_instruction'));",
    text
)

# _getPhaseText replacements
text = re.sub(
    r"currentPhaseText\s*=\s*lang\s*==\s*'en'\s*\?\s*'Swirl the brewer\.'\s*:\s*'[^']*';",
    r"currentPhaseText = AppStrings.str(lang, 'action_swirl');",
    text
)
text = re.sub(
    r"currentPhaseText\s*=\s*lang\s*==\s*'en'\s*\?\s*'Attach cap'\s*:\s*'[^']*';",
    r"currentPhaseText = AppStrings.str(lang, 'action_cap');",
    text
)
text = re.sub(
    r"currentPhaseText\s*=\s*lang\s*==\s*'en'\s*\?\s*'Flip brewer'\s*:\s*'[^']*';",
    r"currentPhaseText = AppStrings.str(lang, 'action_flip');",
    text
)
text = re.sub(
    r"currentPhaseText\s*=\s*AppStrings\.str\(lang, 'stir_instruction'\)\s*\?\?\s*'[^']*';",
    r"currentPhaseText = AppStrings.str(lang, 'stir_instruction');",
    text
)

# build ListView items replacements
text = re.sub(
    r"itemText\s*=\s*lang\s*==\s*'en'\s*\?\s*'Stir with spoon'\s*:\s*'[^']*';",
    r"itemText = AppStrings.str(lang, 'action_stir');",
    text
)
text = re.sub(
    r"itemText\s*=\s*lang\s*==\s*'en'\s*\?\s*'Swirl brewer'\s*:\s*'[^']*';",
    r"itemText = AppStrings.str(lang, 'action_swirl');",
    text
)
text = re.sub(
    r"itemText\s*=\s*lang\s*==\s*'en'\s*\?\s*'Attach cap'\s*:\s*'[^']*';",
    r"itemText = AppStrings.str(lang, 'action_cap');",
    text
)
text = re.sub(
    r"itemText\s*=\s*lang\s*==\s*'en'\s*\?\s*'Flip brewer'\s*:\s*'[^']*';",
    r"itemText = AppStrings.str(lang, 'action_flip');",
    text
)

with open("lib/screens/brewing_screen.dart", "w", encoding="utf-8") as f:
    f.write(text)
    
print("Successfully replaced hardcoded strings with AppStrings!")
