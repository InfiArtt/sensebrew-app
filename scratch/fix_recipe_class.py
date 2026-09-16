import re

with open('lib/core/recipe.dart', 'r', encoding='utf-8') as f:
    code = f.read()

code = code.replace('final int condensedMilkMl;', 'final String extraIngredients;')
code = code.replace('this.condensedMilkMl = 0,', 'this.extraIngredients = "",')
code = code.replace('int? condensedMilkMl,', 'String? extraIngredients,')
code = code.replace('condensedMilkMl: condensedMilkMl ?? this.condensedMilkMl,', 'extraIngredients: extraIngredients ?? this.extraIngredients,')
code = code.replace("'condensedMilkMl': condensedMilkMl,", "'extraIngredients': extraIngredients,")
code = code.replace("condensedMilkMl: json['condensedMilkMl'] ?? 0,", "extraIngredients: json['extraIngredients'] ?? '',")

with open('lib/core/recipe.dart', 'w', encoding='utf-8') as f:
    f.write(code)

print('Recipe class fixed.')
