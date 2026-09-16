import re

with open('lib/screens/custom_recipe_screen.dart', 'r', encoding='utf-8') as f:
    code = f.read()

# Change label from "Catatan Tambahan & Aturan Seduh" to "Deskripsi Resep"
code = code.replace("Catatan Tambahan & Aturan Seduh", "Deskripsi Resep")
code = code.replace("note_label", "recipe_description_label")

# The Dropdown for grind size and TextField for extra ingredients
# They should be inserted before the Phases section.
# We need new controllers.
# Wait, CustomRecipeScreen uses a StatefulWidget.

# Let's find _noteController and add _extraIngredientsController and _targetGrindSizeMicrons
target_vars = '''  late TextEditingController _noteController;'''
replacement_vars = '''  late TextEditingController _noteController;
  late TextEditingController _extraIngredientsController;
  int _targetGrindSizeMicrons = 800;
  final List<int> _grindSizeOptions = [500, 800, 1100];
  final List<String> _grindSizeLabels = ['Halus', 'Sedang', 'Kasar'];'''
code = code.replace(target_vars, replacement_vars)

target_init = '''    _noteController = TextEditingController(text: widget.recipe?.description ?? "");'''
replacement_init = '''    _noteController = TextEditingController(text: widget.recipe?.description ?? "");
    _extraIngredientsController = TextEditingController(text: widget.recipe?.extraIngredients ?? "");
    _targetGrindSizeMicrons = widget.recipe?.targetGrindSizeMicrons ?? 800;
    if (!_grindSizeOptions.contains(_targetGrindSizeMicrons)) {
       _targetGrindSizeMicrons = 800;
    }'''
code = code.replace(target_init, replacement_init)

target_dispose = '''    _noteController.dispose();'''
replacement_dispose = '''    _noteController.dispose();
    _extraIngredientsController.dispose();'''
code = code.replace(target_dispose, replacement_dispose)

target_save = '''      description: _noteController.text,'''
replacement_save = '''      description: _noteController.text,
      extraIngredients: _extraIngredientsController.text,
      targetGrindSizeMicrons: _targetGrindSizeMicrons,'''
code = code.replace(target_save, replacement_save)

target_ui = '''              _buildTextField(
                label: 'Catatan Tambahan & Aturan Seduh',
                controller: _noteController,
                keyboardType: TextInputType.multiline,
                maxLines: 3,
              ),
              const SizedBox(height: 16),
              const Text("Fase Tuangan", style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),'''

replacement_ui = '''              _buildTextField(
                label: 'Deskripsi Resep',
                controller: _noteController,
                keyboardType: TextInputType.multiline,
                maxLines: 3,
              ),
              const SizedBox(height: 16),
              const Text("Target Gilingan", style: TextStyle(fontWeight: FontWeight.bold)),
              const SizedBox(height: 8),
              DropdownButtonFormField<int>(
                value: _targetGrindSizeMicrons,
                decoration: const InputDecoration(border: OutlineInputBorder()),
                items: List.generate(_grindSizeOptions.length, (index) {
                  return DropdownMenuItem(
                    value: _grindSizeOptions[index],
                    child: Text(_grindSizeLabels[index]),
                  );
                }),
                onChanged: (val) {
                  if (val != null) {
                    setState(() {
                      _targetGrindSizeMicrons = val;
                    });
                  }
                },
              ),
              const SizedBox(height: 16),
              _buildTextField(
                label: 'Bahan Tambahan (Opsional)',
                controller: _extraIngredientsController,
                keyboardType: TextInputType.text,
              ),
              const SizedBox(height: 16),
              const Text("Fase Tuangan", style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),'''

code = code.replace(target_ui, replacement_ui)

with open('lib/screens/custom_recipe_screen.dart', 'w', encoding='utf-8') as f:
    f.write(code)

print("Custom Recipe Screen updated")
