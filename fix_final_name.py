import re
with open('lib/core/ai_service.dart', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('name: parseI18n(recipeData[\'name\']),', 'name: parseI18n(recipeData[\'name\']).isEmpty ? (currentRecipe?.name ?? \'AI Recipe\') : parseI18n(recipeData[\'name\']),')
content = content.replace('if (generatedRecipe.name.isEmpty) {\n        generatedRecipe.name = currentRecipe?.name ?? \'AI Recipe\';\n      }\n', '')

with open('lib/core/ai_service.dart', 'w', encoding='utf-8') as f:
    f.write(content)
