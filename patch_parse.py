import re

with open('lib/core/ai_service.dart', 'r', encoding='utf-8') as f:
    content = f.read()

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

content = re.sub(r'final Recipe generatedRecipe = Recipe\([\s\S]*?\);\n', new_parse + '\n', content)

with open('lib/core/ai_service.dart', 'w', encoding='utf-8') as f:
    f.write(content)
