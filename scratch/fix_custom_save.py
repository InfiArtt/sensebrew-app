import re

with open('lib/screens/custom_recipe_screen.dart', 'r', encoding='utf-8') as f:
    text = f.read()

bad_save = """    final recipe = Recipe(
      id: saveAsNew ? null : widget.initialRecipe?.id,
      name: name,
      description: note,
      coffeeGrams: coffee,
      totalWaterMl: water,
      totalDurationSeconds: time,
      phases: phases,
    );"""

good_save = """    final recipe = Recipe(
      id: saveAsNew ? null : widget.initialRecipe?.id,
      name: name,
      description: note,
      coffeeGrams: coffee,
      totalWaterMl: water,
      totalDurationSeconds: time,
      phases: phases,
      targetGrindSizeMicrons: _targetGrindSizeMicrons,
      beanType: _beanType,
      extraIngredients: _extraIngredientsController.text,
      method: widget.initialRecipe?.method ?? BrewMethod.v60,
    );"""

text = text.replace(bad_save, good_save)

# Also fix the currentDraft creation to preserve method!
bad_draft = """      currentDraft = Recipe(
        id: widget.initialRecipe?.id,
        name: _nameController.text,
        description: _noteController.text,
        coffeeGrams: coffee,
        totalWaterMl: water,
        totalDurationSeconds: time,
        phases: phases,
        targetGrindSizeMicrons: _targetGrindSizeMicrons,
        beanType: _beanType,
        extraIngredients: _extraIngredientsController.text,
      );"""

good_draft = """      currentDraft = Recipe(
        id: widget.initialRecipe?.id,
        name: _nameController.text,
        description: _noteController.text,
        coffeeGrams: coffee,
        totalWaterMl: water,
        totalDurationSeconds: time,
        phases: phases,
        targetGrindSizeMicrons: _targetGrindSizeMicrons,
        beanType: _beanType,
        extraIngredients: _extraIngredientsController.text,
        method: widget.initialRecipe?.method ?? BrewMethod.v60,
      );"""

text = text.replace(bad_draft, good_draft)

# Also fix receiving AI data
bad_receive = """        for (var p in newRecipe.phases) {
          _mutablePhases.add({'start': p.startTimeSeconds, 'amount': p.pourAmountMl, 'action': p.action});
        }
      });"""

good_receive = """        for (var p in newRecipe.phases) {
          _mutablePhases.add({'start': p.startTimeSeconds, 'amount': p.pourAmountMl, 'action': p.action});
        }
        _targetGrindSizeMicrons = newRecipe.targetGrindSizeMicrons;
        _beanType = newRecipe.beanType;
        _extraIngredientsController.text = newRecipe.extraIngredients;
      });"""

text = text.replace(bad_receive, good_receive)


with open('lib/screens/custom_recipe_screen.dart', 'w', encoding='utf-8') as f:
    f.write(text)

print("Fixed CustomRecipeScreen saving and state.")
