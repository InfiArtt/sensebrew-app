import re

with open('lib/screens/custom_recipe_screen.dart', 'r', encoding='utf-8') as f:
    text = f.read()

# Remove the case statement for pourFast
text = re.sub(r'\s*case PhaseAction\.pourFast:[^\n]+', '', text)

# Remove PhaseAction.pourFast from conditionals
text = text.replace(' || action == PhaseAction.pourFast', '')
text = text.replace(' || (phase[\'action\'] ?? PhaseAction.pourCircle) == PhaseAction.pourFast', '')

with open('lib/screens/custom_recipe_screen.dart', 'w', encoding='utf-8') as f:
    f.write(text)
print("Done fixing custom_recipe_screen.dart")
