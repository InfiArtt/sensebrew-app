import 'dart:convert';
import 'package:flutter/foundation.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'recipe.dart';

class RecipeRepository extends ChangeNotifier {
  List<Recipe> _recipes = [];
  List<String> _deletedDefaultRecipes = [];
  bool _isLoaded = false;

  bool get isLoaded => _isLoaded;
  List<Recipe> get recipes => _recipes;

  Future<void> loadRecipes() async {
    final prefs = await SharedPreferences.getInstance();
    final String? recipesJson = prefs.getString('saved_recipes');
    _deletedDefaultRecipes = prefs.getStringList('deleted_default_recipes') ?? [];

    if (recipesJson == null || recipesJson.isEmpty) {
      // First time launch: copy default database
      _recipes = List.from(recipeDatabase);
      await saveRecipes();
    } else {
      try {
        final List<dynamic> decodedList = jsonDecode(recipesJson);
        _recipes = decodedList.map((item) => Recipe.fromJson(item as Map<String, dynamic>)).toList();
        
        bool changed = false;

        // BUGFIX: Detect identical IDs and fix them (fixes the favorite bug)
        final idCounts = <String, int>{};
        for (var r in _recipes) {
          idCounts[r.id] = (idCounts[r.id] ?? 0) + 1;
        }
        for (int i = 0; i < _recipes.length; i++) {
          bool needsFix = false;
          String newId = _recipes[i].id;
          bool newIsBuiltIn = _recipes[i].isBuiltIn;

          if (idCounts[_recipes[i].id]! > 1) {
            newId = "${_recipes[i].name.replaceAll(' ', '_')}_${DateTime.now().microsecondsSinceEpoch}_$i";
            needsFix = true;
          }

          // BUGFIX: Correct corrupted isBuiltIn flags.
          // If a recipe is NOT built-in, BUT it has the exact same name, coffeeGrams, and totalWaterMl as a default recipe,
          // AND it doesn't have 'Custom' in its ID or name (actually, checking exact match with default is safest)
          if (!_recipes[i].isBuiltIn) {
            final defaultMatch = recipeDatabase.where((d) => d.name == _recipes[i].name && d.coffeeGrams == _recipes[i].coffeeGrams && d.totalDurationSeconds == _recipes[i].totalDurationSeconds).firstOrNull;
            if (defaultMatch != null) {
              newIsBuiltIn = true;
              needsFix = true;
            }
          }

          if (needsFix) {
            _recipes[i] = _recipes[i].copyWith(id: newId, isBuiltIn: newIsBuiltIn);
            changed = true;
          }
        }

        // DB MIGRATION: Update built-in recipes to use translation keys instead of hardcoded English descriptions
        final dbVersion = prefs.getInt('recipe_db_version') ?? 0;
        if (dbVersion < 1) {
          for (int i = 0; i < _recipes.length; i++) {
            if (_recipes[i].isBuiltIn) {
              final defaultMatch = recipeDatabase.where((d) => d.name == _recipes[i].name).firstOrNull;
              if (defaultMatch != null) {
                _recipes[i] = _recipes[i].copyWith(description: defaultMatch.description);
                changed = true;
              }
            }
          }
          await prefs.setInt('recipe_db_version', 1);
        }

        // Automatically merge missing default recipes (e.g. after an app update)
        for (var defaultRecipe in recipeDatabase) {
          if (!_recipes.any((r) => r.name == defaultRecipe.name) && !_deletedDefaultRecipes.contains(defaultRecipe.name)) {
            _recipes.add(defaultRecipe);
            changed = true;
          }
        }
        if (changed) {
          await saveRecipes();
        }
      } catch (e) {
        // If parsing fails, fallback to default database
        _recipes = List.from(recipeDatabase);
        await saveRecipes();
      }
    }
    _isLoaded = true;
    notifyListeners();
  }

  Future<void> saveRecipes() async {
    final prefs = await SharedPreferences.getInstance();
    final String encodedList = jsonEncode(_recipes.map((r) => r.toJson()).toList());
    await prefs.setString('saved_recipes', encodedList);
    notifyListeners();
  }

  Future<void> addRecipe(Recipe recipe) async {
    _recipes.insert(0, recipe);
    await saveRecipes();
  }

  Future<void> updateRecipe(Recipe updatedRecipe) async {
    final index = _recipes.indexWhere((r) => r.id == updatedRecipe.id);
    if (index != -1) {
      _recipes[index] = updatedRecipe;
      await saveRecipes();
    }
  }

  Future<void> deleteRecipe(String id) async {
    final index = _recipes.indexWhere((r) => r.id == id);
    if (index != -1) {
      final recipe = _recipes[index];
      // If the user is deleting a default recipe, remember it so we don't auto-merge it back later
      if (recipeDatabase.any((r) => r.name == recipe.name)) {
        if (!_deletedDefaultRecipes.contains(recipe.name)) {
          _deletedDefaultRecipes.add(recipe.name);
          final prefs = await SharedPreferences.getInstance();
          await prefs.setStringList('deleted_default_recipes', _deletedDefaultRecipes);
        }
      }
      _recipes.removeAt(index);
      await saveRecipes();
    }
  }

  Future<void> restoreDefaults() async {
    _deletedDefaultRecipes.clear();
    final prefs = await SharedPreferences.getInstance();
    await prefs.setStringList('deleted_default_recipes', []);

    // Add default recipes that are missing
    bool changed = false;
    for (var defaultRecipe in recipeDatabase) {
      if (!_recipes.any((r) => r.name == defaultRecipe.name)) {
        _recipes.add(defaultRecipe);
        changed = true;
      }
    }
    if (changed) {
      await saveRecipes();
    } else {
      notifyListeners();
    }
  }

  Future<void> toggleFavorite(String id) async {
    final index = _recipes.indexWhere((r) => r.id == id);
    if (index != -1) {
      _recipes[index].isFavorite = !_recipes[index].isFavorite;
      await saveRecipes();
    }
  }

  List<Recipe> getRecipesByMethod(BrewMethod method) {
    final filtered = _recipes.where((r) => r.method == method).toList();
    
    filtered.sort((a, b) {
      // 1. Favorites come first
      if (a.isFavorite && !b.isFavorite) return -1;
      if (!a.isFavorite && b.isFavorite) return 1;

      final isCustomA = !a.isBuiltIn;
      final isCustomB = !b.isBuiltIn;
      
      // 2. Custom recipes come before built-in
      if (isCustomA && !isCustomB) return -1;
      if (!isCustomA && isCustomB) return 1;
      
      // 3. Within the same category, sort alphabetically
      return a.name.compareTo(b.name);
    });
    
    return filtered;
  }
}
