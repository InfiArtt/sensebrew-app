// Recipe model, ported from lib/core/recipe.dart.
//
// The Dart constructors carry default values, and the stored JSON relies on
// them, so the defaults live here in makeRecipe/makePhase rather than being
// baked into every entry of the generated seed table.
import { recipeSeeds } from './recipeDatabase';

export type BrewMethod =
  | 'v60'
  | 'frenchPress'
  | 'aeropress'
  | 'vietnamDrip'
  | 'cupping'
  | 'coldBrew';

export type PhaseAction =
  | 'pourCircle' // Pour with metronome per rotation
  | 'pourCenter' // Pour with metronome per second
  | 'wait' // Just wait, no metronome
  | 'stir'
  | 'swirl'
  | 'cap' // Attach cap/plunger
  | 'flip' // Flip Aeropress
  | 'press'
  | 'openValve'
  | 'closeValve';

export interface RecipePhase {
  startTimeSeconds: number;
  pourAmountMl: number;
  instructionText: string;
  action: PhaseAction;
}

export interface Recipe {
  id: string;
  name: string;
  description: string; // Either a translation key or free text
  coffeeGrams: number;
  totalWaterMl: number;
  phases: RecipePhase[];
  totalDurationSeconds: number;
  method: BrewMethod;
  extraIngredients: string;
  targetGrindSizeMicrons: number;
  beanType: string;
  isFavorite: boolean;
  isBuiltIn: boolean;
}

/** A phase as written in the generated seed table, before defaults. */
export type PhaseSeed = {
  startTimeSeconds: number;
  pourAmountMl?: number;
  instructionText?: string;
  action?: PhaseAction;
};

/** A recipe as written in the generated seed table, before defaults. */
export type RecipeSeed = {
  id?: string;
  name: string;
  description?: string;
  coffeeGrams: number;
  totalWaterMl: number;
  phases: PhaseSeed[];
  totalDurationSeconds: number;
  method?: BrewMethod;
  extraIngredients?: string;
  targetGrindSizeMicrons?: number;
  beanType?: string;
  isFavorite?: boolean;
  isBuiltIn?: boolean;
};

export const PHASE_ACTIONS: PhaseAction[] = [
  'pourCircle',
  'pourCenter',
  'wait',
  'stir',
  'swirl',
  'cap',
  'flip',
  'press',
  'openValve',
  'closeValve',
];

export const BREW_METHODS: BrewMethod[] = [
  'v60',
  'frenchPress',
  'aeropress',
  'vietnamDrip',
  'cupping',
  'coldBrew',
];

// Dart built ids from microsecondsSinceEpoch, which collided often enough that
// RecipeRepository needed a de-duplication pass on load. A counter removes the
// possibility instead of repairing it afterwards.
let idSequence = 0;

export function newRecipeId(name: string): string {
  idSequence += 1;
  return `${name.replace(/ /g, '_')}_${Date.now()}_${idSequence}`;
}

export function makePhase(seed: PhaseSeed): RecipePhase {
  return {
    startTimeSeconds: seed.startTimeSeconds,
    pourAmountMl: seed.pourAmountMl ?? 0,
    instructionText: seed.instructionText ?? '',
    action: seed.action ?? 'pourCircle',
  };
}

export function makeRecipe(seed: RecipeSeed): Recipe {
  return {
    id: seed.id ?? newRecipeId(seed.name),
    name: seed.name,
    description: seed.description ?? '',
    coffeeGrams: seed.coffeeGrams,
    totalWaterMl: seed.totalWaterMl,
    phases: seed.phases.map(makePhase),
    totalDurationSeconds: seed.totalDurationSeconds,
    method: seed.method ?? 'v60',
    extraIngredients: seed.extraIngredients ?? '',
    targetGrindSizeMicrons: seed.targetGrindSizeMicrons ?? 800, // medium
    beanType: seed.beanType ?? 'Arabica',
    isFavorite: seed.isFavorite ?? false,
    isBuiltIn: seed.isBuiltIn ?? false,
  };
}

/** Rebuilds a recipe from stored JSON, tolerating older/partial records. */
export function recipeFromJson(json: any): Recipe {
  const name = json?.name ?? '';
  const phases: PhaseSeed[] = Array.isArray(json?.phases)
    ? json.phases.map((p: any) => ({
        startTimeSeconds: p?.startTimeSeconds ?? 0,
        pourAmountMl: Number(p?.pourAmountMl ?? 0),
        instructionText: p?.instructionText ?? '',
        action: PHASE_ACTIONS.includes(p?.action) ? p.action : 'pourCircle',
      }))
    : [];

  return makeRecipe({
    id: json?.id ?? undefined,
    name,
    description: json?.description ?? '',
    coffeeGrams: Number(json?.coffeeGrams ?? 0),
    totalWaterMl: Number(json?.totalWaterMl ?? 0),
    phases,
    totalDurationSeconds: json?.totalDurationSeconds ?? 0,
    method: BREW_METHODS.includes(json?.method) ? json.method : 'v60',
    extraIngredients: json?.extraIngredients ?? '',
    targetGrindSizeMicrons: json?.targetGrindSizeMicrons ?? 800,
    beanType: json?.beanType ?? 'Arabica',
    isFavorite: json?.isFavorite ?? false,
    isBuiltIn:
      json?.isBuiltIn ?? recipeDatabase.some((r) => r.name === name),
  });
}

/** The bundled recipes, with Dart's constructor defaults applied. */
export const recipeDatabase: Recipe[] = recipeSeeds.map(makeRecipe);

/** Formats a number the way the Flutter UI does: drop a trailing ".0". */
export function trimNumber(value: number): string {
  return Number.isInteger(value) ? String(value) : value.toFixed(1).replace(/\.0$/, '');
}

/** "mm:ss" for a phase start time. */
export function formatClock(totalSeconds: number): string {
  const mins = Math.floor(totalSeconds / 60);
  const secs = totalSeconds % 60;
  return `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
}
