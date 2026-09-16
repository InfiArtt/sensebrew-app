import re

with open('lib/screens/brewing_screen.dart', 'r', encoding='utf-8') as f:
    code = f.read()

target = '''      String currentPhaseText = "";
      if (_isBrewing && _currentPhaseIndex < _activeRecipe.phases.length) {'''

replacement = '''      String currentPhaseText = "";
      if (_isBrewing && _currentPhaseIndex >= 0 && _currentPhaseIndex < _activeRecipe.phases.length) {'''

code = code.replace(target, replacement)

with open('lib/screens/brewing_screen.dart', 'w', encoding='utf-8') as f:
    f.write(code)

print('Index fixed.')
