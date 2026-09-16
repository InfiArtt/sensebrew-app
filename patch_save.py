import re

with open('lib/screens/custom_recipe_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

save_pattern = r'void _saveRecipe\(bool saveAsNew\) \{\n\s*final lang = Provider\.of<SettingsState>\(context, listen: false\)\.appLanguage;\n\s*final name = _nameController\.text\.isEmpty \? "Custom" : _nameController\.text;\n\s*final note = _noteController\.text;\n\s*final coffee = double\.tryParse\(_coffeeController\.text\) \?\? 15\.0;\n\s*final water = double\.tryParse\(_waterController\.text\) \?\? [0-9.]*;\n\s*final time = int\.tryParse\(_timeController\.text\) \?\? [0-9]*;'

save_repl = '''void _saveRecipe(bool saveAsNew) {
    final lang = Provider.of<SettingsState>(context, listen: false).appLanguage;
    String name = _nameController.text.isEmpty ? "Custom" : _nameController.text;
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
    
    final coffee = double.tryParse(_coffeeController.text) ?? 15.0;
    final water = double.tryParse(_waterController.text) ?? 250.0;
    final time = int.tryParse(_timeController.text) ?? 150;'''

content = re.sub(save_pattern, save_repl, content)

with open('lib/screens/custom_recipe_screen.dart', 'w', encoding='utf-8') as f:
    f.write(content)
