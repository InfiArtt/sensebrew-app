// Ported from lib/core/recipe_repository.dart.
//
// The repair passes in load() are kept as-is: a device upgrading from the
// Flutter build still has records written by it, including the duplicate ids and
// corrupted isBuiltIn flags that those passes exist to fix.
import { create } from 'zustand';

import {
  BrewMethod,
  Recipe,
  newRecipeId,
  recipeDatabase,
  recipeFromJson,
} from '../recipe';
import { applyAudit202609 } from '../recipeMigrations';
import * as storage from '../storage';

const RECIPES_KEY = 'saved_recipes';
const DELETED_DEFAULTS_KEY = 'deleted_default_recipes';
const DB_VERSION_KEY = 'recipe_db_version';
const DB_VERSION = 2;

interface RecipeState {
  isLoaded: boolean;
  recipes: Recipe[];
  deletedDefaults: string[];

  load: () => Promise<void>;
  addRecipe: (recipe: Recipe) => Promise<void>;
  updateRecipe: (recipe: Recipe) => Promise<void>;
  deleteRecipe: (id: string) => Promise<void>;
  restoreDefaults: () => Promise<void>;
  toggleFavorite: (id: string) => Promise<void>;
  getRecipesByMethod: (method: BrewMethod) => Recipe[];
}

async function persist(recipes: Recipe[]): Promise<void> {
  await storage.setString(RECIPES_KEY, JSON.stringify(recipes));
}

export const useRecipes = create<RecipeState>((set, get) => ({
  isLoaded: false,
  recipes: [],
  deletedDefaults: [],

  load: async () => {
    const [raw, storedDeleted] = await Promise.all([
      storage.getStringOrNull(RECIPES_KEY),
      storage.getStringList(DELETED_DEFAULTS_KEY),
    ]);
    let deletedDefaults = storedDeleted;

    if (!raw) {
      // First launch: copy the bundled database, which needs no migration.
      const recipes = [...recipeDatabase];
      set({ recipes, deletedDefaults, isLoaded: true });
      await persist(recipes);
      await storage.setNumber(DB_VERSION_KEY, DB_VERSION);
      return;
    }

    let recipes: Recipe[];
    try {
      const decoded = JSON.parse(raw);
      if (!Array.isArray(decoded)) throw new Error('saved_recipes is not an array');
      recipes = decoded.map(recipeFromJson);
    } catch {
      // Unreadable store: fall back to the bundled database rather than
      // leaving the user with no recipes at all.
      const fallback = [...recipeDatabase];
      set({ recipes: fallback, deletedDefaults, isLoaded: true });
      await persist(fallback);
      return;
    }

    let changed = false;

    // Repair duplicate ids, which made favouriting one recipe light up another.
    const idCounts = new Map<string, number>();
    recipes.forEach((r) => idCounts.set(r.id, (idCounts.get(r.id) ?? 0) + 1));
    recipes = recipes.map((recipe) => {
      let next = recipe;
      if ((idCounts.get(recipe.id) ?? 0) > 1) {
        next = { ...next, id: newRecipeId(recipe.name) };
        changed = true;
      }
      // Repair isBuiltIn flags that were lost on an earlier save: a recipe
      // matching a bundled one on name, dose and duration is a bundled one.
      if (!next.isBuiltIn) {
        const isDefault = recipeDatabase.some(
          (d) =>
            d.name === next.name &&
            d.coffeeGrams === next.coffeeGrams &&
            d.totalDurationSeconds === next.totalDurationSeconds
        );
        if (isDefault) {
          next = { ...next, isBuiltIn: true };
          changed = true;
        }
      }
      return next;
    });

    const dbVersion = await storage.getNumber(DB_VERSION_KEY, 0);

    // Migration 1: built-in descriptions became translation keys, so replace
    // whatever English text an older build stored.
    if (dbVersion < 1) {
      recipes = recipes.map((recipe) => {
        if (!recipe.isBuiltIn) return recipe;
        const match = recipeDatabase.find((d) => d.name === recipe.name);
        if (!match) return recipe;
        changed = true;
        return { ...recipe, description: match.description };
      });
    }

    // Migration 2: the data audit corrected and renamed some built-ins.
    if (dbVersion < 2) {
      const audit = applyAudit202609(recipes, deletedDefaults, recipeDatabase);
      recipes = audit.recipes;
      if (audit.changed) changed = true;
      if (audit.deletedDefaults.join('\n') !== deletedDefaults.join('\n')) {
        deletedDefaults = audit.deletedDefaults;
        await storage.setStringList(DELETED_DEFAULTS_KEY, deletedDefaults);
      }
    }

    if (dbVersion < DB_VERSION) await storage.setNumber(DB_VERSION_KEY, DB_VERSION);

    // Merge in recipes added by an app update, unless the user deleted them.
    recipeDatabase.forEach((defaultRecipe) => {
      const present = recipes.some((r) => r.name === defaultRecipe.name);
      if (!present && !deletedDefaults.includes(defaultRecipe.name)) {
        recipes.push(defaultRecipe);
        changed = true;
      }
    });

    set({ recipes, deletedDefaults, isLoaded: true });
    if (changed) await persist(recipes);
  },

  addRecipe: async (recipe) => {
    const recipes = [recipe, ...get().recipes];
    set({ recipes });
    await persist(recipes);
  },

  updateRecipe: async (updated) => {
    const recipes = get().recipes.map((r) => (r.id === updated.id ? updated : r));
    set({ recipes });
    await persist(recipes);
  },

  deleteRecipe: async (id) => {
    const { recipes, deletedDefaults } = get();
    const recipe = recipes.find((r) => r.id === id);
    if (!recipe) return;

    let nextDeleted = deletedDefaults;
    // Remember deleted bundled recipes so the merge pass stops re-adding them.
    const isDefault = recipeDatabase.some((r) => r.name === recipe.name);
    if (isDefault && !deletedDefaults.includes(recipe.name)) {
      nextDeleted = [...deletedDefaults, recipe.name];
      await storage.setStringList(DELETED_DEFAULTS_KEY, nextDeleted);
    }

    const nextRecipes = recipes.filter((r) => r.id !== id);
    set({ recipes: nextRecipes, deletedDefaults: nextDeleted });
    await persist(nextRecipes);
  },

  restoreDefaults: async () => {
    await storage.setStringList(DELETED_DEFAULTS_KEY, []);

    const recipes = [...get().recipes];
    let changed = false;
    recipeDatabase.forEach((defaultRecipe) => {
      if (!recipes.some((r) => r.name === defaultRecipe.name)) {
        recipes.push(defaultRecipe);
        changed = true;
      }
    });

    set({ recipes, deletedDefaults: [] });
    if (changed) await persist(recipes);
  },

  toggleFavorite: async (id) => {
    const recipes = get().recipes.map((r) =>
      r.id === id ? { ...r, isFavorite: !r.isFavorite } : r
    );
    set({ recipes });
    await persist(recipes);
  },

  getRecipesByMethod: (method) => {
    return get()
      .recipes.filter((r) => r.method === method)
      .sort((a, b) => {
        // 1. Favourites first.
        if (a.isFavorite !== b.isFavorite) return a.isFavorite ? -1 : 1;
        // 2. Then the user's own recipes before the bundled ones.
        if (a.isBuiltIn !== b.isBuiltIn) return a.isBuiltIn ? 1 : -1;
        // 3. Then alphabetically.
        return a.name.localeCompare(b.name);
      });
  },
}));
