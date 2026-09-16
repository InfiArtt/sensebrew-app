import re

with open('lib/core/ai_service.dart', 'r', encoding='utf-8') as f:
    content = f.read()

new_phase = '''
        return RecipePhase(
          startTimeSeconds: (p['startTimeSeconds'] as num?)?.toInt() ?? 0,
          pourAmountMl: amount,
          action: action,
          instructionText: _parseI18n(p['instructionText']),
        );
'''
content = re.sub(r'return RecipePhase\([\s\S]*?instructionText: AppStrings\.str\(lang, \'pour\', \[amount\.toInt\(\)\.toString\(\)\]\),\n        \);', new_phase, content)

with open('lib/core/ai_service.dart', 'w', encoding='utf-8') as f:
    f.write(content)
