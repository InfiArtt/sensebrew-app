import type { BrewMethod, Recipe } from './core/recipe';

/**
 * Screens carry a method through to the custom-recipe form. The Flutter build
 * once lost that parameter and treated a recipe started from the Cupping list as
 * a V60 one (MIGRATION_HANDOVER.md, issue 3), so `targetMethod` is required
 * rather than optional: forgetting it is a type error here.
 */
export type RootStackParamList = {
  Home: undefined;
  MethodRecipes: { method: BrewMethod; methodName: string };
  Brewing: { recipe: Recipe };
  Calibration: undefined;
  PourCalculator: undefined;
  Settings: undefined;
  CustomRecipe: { targetMethod: BrewMethod; initialRecipe?: Recipe };
  AiChat: { targetMethod: BrewMethod; initialRecipe?: Recipe };
};
