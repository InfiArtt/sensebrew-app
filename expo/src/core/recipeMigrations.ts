// Brings stored copies of the built-in recipes up to date with the bundled data.
//
// On first launch the app copies every built-in recipe into storage and reads
// from that copy afterwards, so a correction to the bundled data never reaches a
// phone that already has the app installed. Renaming a built-in is worse: the
// merge on load sees the new name missing and adds it next to the old copy.
//
// A stored recipe is only replaced when its content is exactly what an earlier
// build bundled, checked against a fingerprint of that version. A recipe the
// user edited no longer matches and is left alone, even when a repair pass has
// flagged it built-in again because its name, dose and duration still match.
//
// Kept free of React Native imports so scripts/check-brew-plan.js can run it.
import type { Recipe } from './recipe';

/** Built-in recipes renamed by the data audit of September 2026, old name to new. */
export const RENAMED_RECIPES: Record<string, string> = {
  'Hario Switch (Tetsu Kasuya)': 'Inspired by Tetsu Kasuya (Hario Switch)',
  'Ryan Wibawa WBrC 2024': 'Inspired by Ryan Wibawa (WBrC 2024)',
  'Phin Coconut (Bac Xiu)': 'Coconut Phin (inspired by Bac Xiu)',
  'Slayer French Press (Skim Early)': 'Skim-Early French Press',
  'Tuomas Merikanto W.A.C': 'W.A.C Tuomas Merikanto (2021)',
};

/**
 * Fingerprints of the built-in recipes as bundled before the data audit, keyed
 * by their old name. Generated from the previous recipeDatabase.ts; only the
 * recipes the audit changed or renamed are listed.
 */
export const AUDIT_2026_09_FINGERPRINTS: Record<string, string> = {
  'April Pour-Over': '6db363a6',
  'Scott Rao V60': 'ce323a95',
  'Hario Switch (Tetsu Kasuya)': 'ac4329c4',
  'Lance Hedrick French Press': 'c07db23d',
  'Slayer French Press (Skim Early)': '543b88c1',
  'Tim Wendelboe French Press': 'c476ed79',
  'WAC 2023 Champion Recipe': '5f988c78',
  'Jonathan Gagne Long Steep': '93c50e8f',
  'SCA Cupping Protocol': '0f90e681',
  'James Hoffmann Home Cupping': '49c90865',
  'Cold Evaluation Cupping': '201ab461',
  'Ryan Wibawa WBrC 2024': '2372e018',
  'Kasuya Devil Recipe (Switch)': '3a592141',
  'W.A.C Carolina Ibarra (2018)': '315be865',
  'W.A.C Paulina Miczka (2017)': '3afb9a12',
  'Tuomas Merikanto W.A.C': '43ea28fd',
  'Phin Coconut (Bac Xiu)': '017c4dcd',
};

/** Everything the user can edit, so an edited copy never matches. */
export function recipeFingerprint(recipe: Recipe): string {
  const content = JSON.stringify([
    recipe.name,
    recipe.description,
    recipe.coffeeGrams,
    recipe.totalWaterMl,
    recipe.totalDurationSeconds,
    recipe.method,
    recipe.extraIngredients,
    recipe.targetGrindSizeMicrons,
    recipe.beanType,
    recipe.phases.map((p) => [p.startTimeSeconds, p.pourAmountMl, p.instructionText, p.action]),
  ]);
  // FNV-1a, 32 bit. Collisions only matter against an edited copy of the same
  // recipe, which is not something to guard against with a stronger hash.
  let hash = 0x811c9dc5;
  for (let i = 0; i < content.length; i++) {
    hash ^= content.charCodeAt(i);
    hash = Math.imul(hash, 0x01000193) >>> 0;
  }
  return hash.toString(16).padStart(8, '0');
}

export interface RefreshResult {
  recipes: Recipe[];
  deletedDefaults: string[];
  changed: boolean;
}

/**
 * Replaces every stored recipe that is an untouched copy of an audited
 * built-in with its corrected version, following renames. The id and the
 * favourite flag are the user's and are kept.
 */
export function applyAudit202609(
  stored: Recipe[],
  deletedDefaults: string[],
  database: Recipe[]
): RefreshResult {
  let changed = false;

  const recipes = stored.map((recipe) => {
    const oldFingerprint = AUDIT_2026_09_FINGERPRINTS[recipe.name];
    if (!oldFingerprint || recipeFingerprint(recipe) !== oldFingerprint) return recipe;

    const name = RENAMED_RECIPES[recipe.name] ?? recipe.name;
    const bundled = database.find((d) => d.name === name);
    if (!bundled) return recipe;

    changed = true;
    return { ...bundled, id: recipe.id, isFavorite: recipe.isFavorite, isBuiltIn: true };
  });

  // A built-in deleted under its old name stays deleted under the new one.
  const renamedDeleted = deletedDefaults.map((name) => RENAMED_RECIPES[name] ?? name);
  if (renamedDeleted.some((name, i) => name !== deletedDefaults[i])) changed = true;

  return { recipes, deletedDefaults: renamedDeleted, changed };
}
