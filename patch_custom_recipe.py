import re

with open('lib/screens/custom_recipe_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add hidden fields
content = re.sub(
    r'final List<Map<String, dynamic>> _mutablePhases = \[\];',
    'final List<Map<String, dynamic>> _mutablePhases = [];\n  String? _hiddenAiName;\n  String? _hiddenAiDesc;\n  String? _hiddenAiExtra;',
    content
)

# 2. Init hidden fields in initState
init_pattern = r'final r = widget\.initialRecipe!;\n\s*_nameController\.text = AppStrings\.str\(lang, r\.name\);\n\s*_noteController\.text = AppStrings\.str\(lang, r\.description\);\n\s*_extraIngredientsController\.text = AppStrings\.str\(lang, r\.extraIngredients\);'
init_repl = '''final r = widget.initialRecipe!;
      _hiddenAiName = r.name;
      _hiddenAiDesc = r.description;
      _hiddenAiExtra = r.extraIngredients;
      _nameController.text = AppStrings.str(lang, r.name);
      _noteController.text = AppStrings.str(lang, r.description);
      _extraIngredientsController.text = AppStrings.str(lang, r.extraIngredients);'''
content = re.sub(init_pattern, init_repl, content)

# 3. Update hidden fields in AI response
ai_pattern = r'if \(newRecipe != null && newRecipe is Recipe\) \{\n\s*setState\(\(\) \{\n\s*_nameController\.text = newRecipe\.name;\n\s*_noteController\.text = newRecipe\.description;\n\s*_coffeeController\.text = [^\n]+;\n\s*_waterController\.text = [^\n]+;\n\s*_timeController\.text = [^\n]+;'
ai_repl = '''if (newRecipe != null && newRecipe is Recipe) {
        setState(() {
          _hiddenAiName = newRecipe.name;
          _hiddenAiDesc = newRecipe.description;
          _hiddenAiExtra = newRecipe.extraIngredients;
          
          _nameController.text = AppStrings.str(lang, newRecipe.name);
          _noteController.text = AppStrings.str(lang, newRecipe.description);
          _extraIngredientsController.text = AppStrings.str(lang, newRecipe.extraIngredients);
          _coffeeController.text = newRecipe.coffeeGrams == newRecipe.coffeeGrams.toInt() ? newRecipe.coffeeGrams.toInt().toString() : newRecipe.coffeeGrams.toString();
          _waterController.text = newRecipe.totalWaterMl == newRecipe.totalWaterMl.toInt() ? newRecipe.totalWaterMl.toInt().toString() : newRecipe.totalWaterMl.toString();
          _timeController.text = newRecipe.totalDurationSeconds.toString();'''
content = re.sub(ai_pattern, ai_repl, content)

# 4. Use hidden fields in save
save_pattern = r'String name = _nameController\.text;\n\s*String note = _noteController\.text;\n\s*double coffee = double\.tryParse\(_coffeeController\.text\) \?\? 15\.0;\n\s*double water = double\.tryParse\(_waterController\.text\) \?\? 225\.0;\n\s*int time = int\.tryParse\(_timeController\.text\) \?\? 150;\n\s*String extra = _extraIngredientsController\.text;'
save_repl = '''final lang = Provider.of<SettingsState>(context, listen: false).appLanguage;
    String name = _nameController.text;
    if (_hiddenAiName != null && AppStrings.str(lang, _hiddenAiName!) == name) {
      name = _hiddenAiName!;
    }
    String note = _noteController.text;
    if (_hiddenAiDesc != null && AppStrings.str(lang, _hiddenAiDesc!) == note) {
      note = _hiddenAiDesc!;
    }
    String extra = _extraIngredientsController.text;
    if (_hiddenAiExtra != null && AppStrings.str(lang, _hiddenAiExtra!) == extra) {
      extra = _hiddenAiExtra!;
    }
    
    double coffee = double.tryParse(_coffeeController.text) ?? 15.0;
    double water = double.tryParse(_waterController.text) ?? 225.0;
    int time = int.tryParse(_timeController.text) ?? 150;'''
content = re.sub(save_pattern, save_repl, content)

with open('lib/screens/custom_recipe_screen.dart', 'w', encoding='utf-8') as f:
    f.write(content)
