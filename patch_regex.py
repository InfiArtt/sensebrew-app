import re

with open('lib/core/ai_service.dart', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace RULES
content = re.sub(
    r'- CRITICAL: For "name", "description", "extraIngredients", and all phase "instructionText", you MUST provide translations in BOTH Indonesian and English using this exact delimiter format: "ID: \[Indonesian text\] \|\| EN: \[English text\]"\. Example: "ID: Gunakan gilingan kasar\. \|\| EN: Use a coarse grind\."',
    '- CRITICAL: For "name", "description", "extraIngredients", and all phase "instructionText", you MUST provide translations in BOTH Indonesian and English. You must return an object with "id" and "en" keys instead of a string.',
    content
)

content = re.sub(
    r'- For "extraIngredients", write cleanly with metric units\. DO NOT use acronyms like "sdm" or "SKM"\. If none, leave blank string ""\.',
    '- For "extraIngredients", write cleanly with metric units. DO NOT use acronyms like "sdm" or "SKM". If none, leave the id and en strings blank "".',
    content
)

# Replace JSON block
content = re.sub(
    r' "name": "ID: Resep Baru \|\| EN: New Recipe",',
    ' "name": {"id": "Resep Baru", "en": "New Recipe"},',
    content
)
content = re.sub(
    r' "description": "ID: Penjelasan singkat\.\\n\\nEstimasi Rasa: Acidity cerah\.\.\. \|\| EN: Short explanation\.\\n\\nFlavor Profile: Bright acidity\.\.\.",',
    ' "description": {"id": "Penjelasan singkat.\\n\\nEstimasi Rasa: Acidity cerah...", "en": "Short explanation.\\n\\nFlavor Profile: Bright acidity..."},',
    content
)
content = re.sub(
    r' "extraIngredients": "ID: 15 ml susu kental manis \|\| EN: 15 ml condensed milk",',
    ' "extraIngredients": {"id": "15 ml susu kental manis", "en": "15 ml condensed milk"},',
    content
)
content = re.sub(
    r' "instructionText": "ID: Tuang 50 ml air \|\| EN: Pour 50 ml of water"',
    ' "instructionText": {"id": "Tuang 50 ml air", "en": "Pour 50 ml of water"}',
    content
)

# Parse response in dart
old_parse = '''final Recipe generatedRecipe = Recipe(
        id: currentRecipe?.id, 
        name: recipeData['name'] as String? ?? (currentRecipe != null ? currentRecipe.name : 'AI Recipe'),
        description: recipeData['description'] as String? ?? '',
        coffeeGrams: (recipeData['coffeeGrams'] as num?)?.toDouble() ?? 15.0,
        totalWaterMl: totalWater,
        totalDurationSeconds: totalDuration,
        phases: phases,
        targetGrindSizeMicrons: (recipeData['targetGrindSizeMicrons'] as num?)?.toInt() ?? currentRecipe?.targetGrindSizeMicrons ?? 800,
        extraIngredients: recipeData['extraIngredients'] as String? ?? currentRecipe?.extraIngredients ?? '',
        beanType: recipeData['beanType'] as String? ?? currentRecipe?.beanType ?? 'Arabica',
        method: currentRecipe?.method ?? BrewMethod.v60,
      );'''

new_parse = '''
      String _parseI18n(dynamic field) {
        if (field == null) return '';
        if (field is String) return field;
        if (field is Map) {
          final idStr = field['id']?.toString() ?? '';
          final enStr = field['en']?.toString() ?? '';
          if (idStr.isEmpty && enStr.isEmpty) return '';
          return 'ID: ' + idStr + ' || EN: ' + enStr;
        }
        return field.toString();
      }

      final Recipe generatedRecipe = Recipe(
        id: currentRecipe?.id, 
        name: _parseI18n(recipeData['name']),
        description: _parseI18n(recipeData['description']),
        coffeeGrams: (recipeData['coffeeGrams'] as num?)?.toDouble() ?? 15.0,
        totalWaterMl: totalWater,
        totalDurationSeconds: totalDuration,
        phases: phases,
        targetGrindSizeMicrons: (recipeData['targetGrindSizeMicrons'] as num?)?.toInt() ?? currentRecipe?.targetGrindSizeMicrons ?? 800,
        extraIngredients: _parseI18n(recipeData['extraIngredients']),
        beanType: recipeData['beanType'] as String? ?? currentRecipe?.beanType ?? 'Arabica',
        method: currentRecipe?.method ?? BrewMethod.v60,
      );
      
      if (generatedRecipe.name.isEmpty) {
        generatedRecipe.name = currentRecipe?.name ?? 'AI Recipe';
      }
'''

content = content.replace(old_parse, new_parse)

old_phase_parse = '''        return RecipePhase(
          startTimeSeconds: (p['startTimeSeconds'] as num?)?.toInt() ?? 0,
          pourAmountMl: (p['pourAmountMl'] as num?)?.toDouble() ?? 0.0,
          action: pAction,
          instructionText: p['instructionText'] as String? ?? '',
        );'''

new_phase_parse = '''        return RecipePhase(
          startTimeSeconds: (p['startTimeSeconds'] as num?)?.toInt() ?? 0,
          pourAmountMl: (p['pourAmountMl'] as num?)?.toDouble() ?? 0.0,
          action: pAction,
          instructionText: _parseI18nPhase(p['instructionText']),
        );'''

content = content.replace(old_phase_parse, new_phase_parse)

old_phase_func = '''    final List<RecipePhase> phases = (recipeData['phases'] as List<dynamic>? ?? []).map((dynamic phaseData) {'''

new_phase_func = '''
      String _parseI18nPhase(dynamic field) {
        if (field == null) return '';
        if (field is String) return field;
        if (field is Map) {
          final idStr = field['id']?.toString() ?? '';
          final enStr = field['en']?.toString() ?? '';
          if (idStr.isEmpty && enStr.isEmpty) return '';
          return 'ID: ' + idStr + ' || EN: ' + enStr;
        }
        return field.toString();
      }

      final List<RecipePhase> phases = (recipeData['phases'] as List<dynamic>? ?? []).map((dynamic phaseData) {'''

content = content.replace(old_phase_func, new_phase_func)

with open('lib/core/ai_service.dart', 'w', encoding='utf-8') as f:
    f.write(content)

