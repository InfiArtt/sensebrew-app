import re

with open('lib/screens/custom_recipe_screen.dart', 'r', encoding='utf-8') as f:
    code = f.read()

# Replace recipe_note label
code = code.replace(
    "ExcludeSemantics(child: Text(AppStrings.str(lang, 'recipe_note')",
    "ExcludeSemantics(child: Text('Deskripsi Resep'"
)
code = code.replace(
    "label: AppStrings.str(lang, 'recipe_note'),",
    "label: 'Deskripsi Resep',"
)

# Target for where to insert the new elements (right after note controller block)
target_insertion = '''            Semantics(
              label: 'Deskripsi Resep',
              child: TextField(
                controller: _noteController,
                decoration: const InputDecoration(border: OutlineInputBorder()),
                onChanged: (val) => setState(() {}),
              ),
            ),
            const SizedBox(height: 16),'''

new_ui = '''            Semantics(
              label: 'Deskripsi Resep',
              child: TextField(
                controller: _noteController,
                decoration: const InputDecoration(border: OutlineInputBorder()),
                onChanged: (val) => setState(() {}),
              ),
            ),
            const SizedBox(height: 16),
            
            ExcludeSemantics(child: Text('Target Gilingan', style: const TextStyle(fontWeight: FontWeight.bold))),
            const SizedBox(height: 8),
            Semantics(
              label: 'Target Gilingan',
              child: DropdownButtonFormField<int>(
                value: _targetGrindSizeMicrons,
                decoration: const InputDecoration(border: OutlineInputBorder()),
                items: const [
                  DropdownMenuItem(value: 400, child: Text('Sangat Halus (Espresso)')),
                  DropdownMenuItem(value: 600, child: Text('Halus (Aeropress)')),
                  DropdownMenuItem(value: 800, child: Text('Sedang (V60 / Kalita)')),
                  DropdownMenuItem(value: 1000, child: Text('Agak Kasar (Chemex)')),
                  DropdownMenuItem(value: 1200, child: Text('Kasar (French Press / Switch)')),
                  DropdownMenuItem(value: 1400, child: Text('Sangat Kasar (Cold Brew)')),
                ],
                onChanged: (val) {
                  if (val != null) setState(() { _targetGrindSizeMicrons = val; });
                },
              ),
            ),
            const SizedBox(height: 16),

            ExcludeSemantics(child: Text('Bahan Tambahan (Opsional)', style: const TextStyle(fontWeight: FontWeight.bold))),
            const SizedBox(height: 8),
            Semantics(
              label: 'Bahan Tambahan',
              child: TextField(
                controller: _extraIngredientsController,
                decoration: const InputDecoration(
                  border: OutlineInputBorder(),
                  hintText: 'Misal: 15 ml susu kental manis, 100 gram es batu',
                ),
                onChanged: (val) => setState(() {}),
              ),
            ),
            const SizedBox(height: 16),'''

if target_insertion in code:
    code = code.replace(target_insertion, new_ui)
else:
    print("Failed to find insertion point!")

with open('lib/screens/custom_recipe_screen.dart', 'w', encoding='utf-8') as f:
    f.write(code)

print('Custom UI injected!')
