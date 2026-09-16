import re

with open('lib/core/recipe.dart', 'r', encoding='utf-8') as f:
    content = f.read()

# For cupping recipes, insert beanType: 'Bebas',
# They look like:
# method: BrewMethod.cupping,
# targetGrindSizeMicrons: 850,
# Let's replace 'method: BrewMethod.cupping,' with 'method: BrewMethod.cupping, beanType: \'Bebas\','

content = content.replace(
    'method: BrewMethod.cupping,',
    "method: BrewMethod.cupping,\n      beanType: 'Bebas',"
)

with open('lib/core/recipe.dart', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated Cupping recipes to use Bebas beanType")
