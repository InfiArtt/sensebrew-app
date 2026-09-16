import 'package:flutter/material.dart';
import 'package:flutter/semantics.dart';
import 'package:provider/provider.dart';
import '../core/calibration_state.dart';
import '../core/timer_state.dart';
import '../core/recipe.dart';
import '../core/settings_state.dart';
import '../core/app_strings.dart';
import 'calibration_screen.dart';
import 'brewing_screen.dart';
import 'custom_recipe_screen.dart';
import '../core/recipe_repository.dart';

class MethodRecipeScreen extends StatefulWidget {
  final BrewMethod method;
  final String methodName;

  const MethodRecipeScreen({super.key, required this.method, required this.methodName});

  @override
  State<MethodRecipeScreen> createState() => _MethodRecipeScreenState();
}

class _MethodRecipeScreenState extends State<MethodRecipeScreen> {
  @override
  Widget build(BuildContext context) {
    final calibration = Provider.of<CalibrationState>(context);
    final settings = Provider.of<SettingsState>(context);
    final audio = Provider.of<TimerAudioState>(context, listen: false);
    final lang = settings.appLanguage;
    
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.methodName),
        excludeHeaderSemantics: true,
      ),
      body: Consumer<CalibrationState>(
        builder: (context, calibration, child) {
          final isCalibrated = calibration.isCalibrated;
          return Consumer<RecipeRepository>(
            builder: (context, repo, child) {
              final _recipes = repo.getRecipesByMethod(widget.method);
              
              final List<dynamic> listItems = [];
              bool hasFav = false;
              bool hasCustom = false;
              bool hasBuiltIn = false;

              for (var r in _recipes) {
                if (r.isFavorite) {
                  if (!hasFav) {
                    listItems.add('header_favorites');
                    hasFav = true;
                  }
                } else {
                  final isCustom = !r.isBuiltIn;
                  if (isCustom) {
                    if (!hasCustom) {
                      listItems.add('header_custom');
                      hasCustom = true;
                    }
                  } else {
                    if (!hasBuiltIn) {
                      listItems.add('header_builtin');
                      hasBuiltIn = true;
                    }
                  }
                }
                listItems.add(r);
              }

              return Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  Padding(
                    padding: const EdgeInsets.symmetric(horizontal: 16.0, vertical: 16.0),
                    child: Semantics(
                      label: AppStrings.str(lang, 'custom_recipe_label'),
                      button: true,
                      excludeSemantics: true,
                      child: ElevatedButton.icon(
                        icon: const Icon(Icons.add),
                        label: Text(AppStrings.str(lang, 'custom_recipe_btn'), textAlign: TextAlign.center),
                        style: ElevatedButton.styleFrom(
                          padding: const EdgeInsets.symmetric(vertical: 16, horizontal: 8),
                          backgroundColor: Colors.purple.shade50,
                          foregroundColor: Colors.purple.shade900,
                        ),
                        onPressed: () async {
                          final newRecipe = await Navigator.push(
                            context,
                            MaterialPageRoute(builder: (_) => CustomRecipeScreen()),
                          );
                          if (newRecipe != null && newRecipe is Recipe) {
                            final mappedRecipe = newRecipe.copyWith(method: widget.method);
                            await repo.addRecipe(mappedRecipe);
                            if (mounted) {
                              ScaffoldMessenger.of(context).showSnackBar(
                                SnackBar(content: Text(AppStrings.str(lang, 'save_recipe_success') ?? 'Resep disimpan!')),
                              );
                            }
                          }
                        },
                      ),
                    ),
                  ),
                  const SizedBox(height: 8),
                  Expanded(
                    child: ListView.builder(
                      itemCount: listItems.length,
                      itemBuilder: (context, index) {
                        final item = listItems[index];
                        
                        if (item is String) {
                          return Padding(
                            padding: const EdgeInsets.only(left: 20, top: 16, bottom: 8),
                            child: Text(
                              AppStrings.str(lang, item),
                              style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: Colors.blueGrey),
                            ),
                          );
                        }
                        
                        final recipe = item as Recipe;
                          return Card(
                          margin: const EdgeInsets.only(bottom: 8, left: 16, right: 16),
                          child: ListTile(
                            title: Semantics(
                              excludeSemantics: true,
                              label: AppStrings.str(lang, 'recipe_label', [AppStrings.str(lang, recipe.name), 
                                recipe.coffeeGrams == recipe.coffeeGrams.toInt() ? recipe.coffeeGrams.toInt().toString() : recipe.coffeeGrams.toStringAsFixed(1), 
                                recipe.totalWaterMl == recipe.totalWaterMl.toInt() ? recipe.totalWaterMl.toInt().toString() : recipe.totalWaterMl.toStringAsFixed(1)
                              ]),
                              child: Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  Text(AppStrings.str(lang, recipe.name), style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
                                  const SizedBox(height: 4),
                                  Text('${recipe.coffeeGrams == recipe.coffeeGrams.toInt() ? recipe.coffeeGrams.toInt() : recipe.coffeeGrams}g | ${recipe.totalWaterMl == recipe.totalWaterMl.toInt() ? recipe.totalWaterMl.toInt() : recipe.totalWaterMl}ml', style: TextStyle(color: Theme.of(context).textTheme.bodySmall?.color)),
                                ],
                              ),
                            ),
                            trailing: IconButton(
                              tooltip: AppStrings.str(lang, recipe.isFavorite ? 'remove_favorite' : 'mark_favorite'),
                              icon: Icon(
                                recipe.isFavorite ? Icons.star : Icons.star_border,
                                color: recipe.isFavorite ? Colors.amber : Colors.grey,
                                semanticLabel: AppStrings.str(lang, recipe.isFavorite ? 'remove_favorite' : 'mark_favorite'),
                              ),
                              onPressed: () {
                                repo.toggleFavorite(recipe.id);
                              },
                            ),
                          onTap: () async {
                            final action = await showModalBottomSheet<String>(
                              context: context,
                              builder: (ctx) {
                                return SafeArea(
                                  child: Padding(
                                    padding: const EdgeInsets.all(16.0),
                                    child: Column(
                                      mainAxisSize: MainAxisSize.min,
                                      crossAxisAlignment: CrossAxisAlignment.stretch,
                                      children: [
                                        Text(AppStrings.str(lang, recipe.name), style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
                                        const SizedBox(height: 16),
                                        ElevatedButton.icon(
                                          icon: const Icon(Icons.play_arrow),
                                          label: Text(AppStrings.str(lang, 'brew_btn') ?? 'Seduh'),
                                          style: ElevatedButton.styleFrom(
                                            backgroundColor: Colors.brown,
                                            foregroundColor: Colors.white,
                                            padding: const EdgeInsets.symmetric(vertical: 16),
                                          ),
                                          onPressed: () => Navigator.pop(ctx, 'brew'),
                                        ),
                                        const SizedBox(height: 8),
                                        OutlinedButton.icon(
                                          icon: const Icon(Icons.edit),
                                          label: Text(AppStrings.str(lang, 'edit_btn') ?? 'Edit'),
                                          onPressed: () => Navigator.pop(ctx, 'edit'),
                                        ),
                                        const SizedBox(height: 8),
                                        OutlinedButton.icon(
                                          icon: const Icon(Icons.delete, color: Colors.red),
                                          label: Text(AppStrings.str(lang, 'delete_btn') ?? 'Hapus', style: const TextStyle(color: Colors.red)),
                                          onPressed: () => Navigator.pop(ctx, 'delete'),
                                        ),
                                      ],
                                    ),
                                  ),
                                );
                              }
                            );

                            if (!mounted || action == null) return;

                            if (action == 'brew') {
                              if (!isCalibrated) {
                                final msg = AppStrings.str(lang, 'uncalibrated_status') ?? '';
                                SemanticsService.announce(msg, TextDirection.ltr);
                                ScaffoldMessenger.of(context).showSnackBar(
                                  SnackBar(content: Text(msg)),
                                );
                                return;
                              }
                              Navigator.push(
                                context,
                                MaterialPageRoute(
                                  builder: (_) => BrewingScreen(recipe: recipe),
                                ),
                              );
                            } else if (action == 'edit') {
                              final editedRecipe = await Navigator.push(
                                context,
                                MaterialPageRoute(builder: (_) => CustomRecipeScreen(initialRecipe: recipe)),
                              );
                              if (editedRecipe != null && editedRecipe is Recipe) {
                                // Now we handle edit directly since we don't know if the user clicked Save or Save As.
                                // Actually, CustomRecipeScreen will just return the Recipe.
                                // But since ID could be the same (overwrite) or different (save as),
                                // we can just tell repo to update it or add it.
                                // Wait, CustomRecipeScreen will be responsible for returning the recipe.
                                // If the ID is the same, we update. If it's different, it's a new recipe, we add.
                                if (editedRecipe.id == recipe.id) {
                                  await repo.updateRecipe(editedRecipe);
                                } else {
                                  await repo.addRecipe(editedRecipe);
                                }
                              }
                            } else if (action == 'delete') {
                              final confirmed = await showDialog<bool>(
                                context: context,
                                builder: (ctx2) => AlertDialog(
                                  title: Text(AppStrings.str(lang, 'delete_confirm_title') ?? 'Hapus Resep?'),
                                  content: Text((AppStrings.str(lang, 'delete_confirm_desc') ?? 'Apakah kamu yakin ingin menghapus resep {0}?').replaceAll('{0}', AppStrings.str(lang, recipe.name))),
                                  actions: [
                                    TextButton(
                                      onPressed: () => Navigator.pop(ctx2, false),
                                      child: Text(AppStrings.str(lang, 'cancel_brew_btn') ?? 'Batal'),
                                    ),
                                    ElevatedButton(
                                      style: ElevatedButton.styleFrom(backgroundColor: Colors.red, foregroundColor: Colors.white),
                                      onPressed: () => Navigator.pop(ctx2, true),
                                      child: Text(AppStrings.str(lang, 'delete_btn') ?? 'Hapus'),
                                    ),
                                  ],
                                ),
                              );

                              if (confirmed == true) {
                                await repo.deleteRecipe(recipe.id);
                              }
                            }
                          },
                        ),
                    );
                  },
                ),
              ),
            ],
          );
        },
      );
        },
      ),
    );
  }
}
