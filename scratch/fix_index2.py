with open('lib/screens/brewing_screen.dart', 'r', encoding='utf-8') as f:
    code = f.read()

code = code.replace('if (_isBrewing && _currentPhaseIndex < _activeRecipe.phases.length) {', 'if (_isBrewing && _currentPhaseIndex >= 0 && _currentPhaseIndex < _activeRecipe.phases.length) {')

with open('lib/screens/brewing_screen.dart', 'w', encoding='utf-8') as f:
    f.write(code)

print('Index fixed 2.')
