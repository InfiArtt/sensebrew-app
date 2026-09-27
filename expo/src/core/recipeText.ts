// Recipe wording shared by the screens, and the plain-text form a recipe is
// shared in.
//
// Kept free of React Native imports so scripts/check-brew-plan.js can run it.
import { str } from './appStrings';
import { getGrindCategoryName, type GrinderModel } from './grinderDatabase';
import { formatClock, trimNumber, type BrewMethod, type PhaseAction, type Recipe } from './recipe';

/** Method names as the home screen shows them; they are not translated. */
export const METHOD_NAMES: Record<BrewMethod, string> = {
  v60: 'V60 / Pour-over',
  frenchPress: 'French Press',
  aeropress: 'Aeropress',
  vietnamDrip: 'Vietnam Drip',
  cupping: 'SCA Cupping Protocol',
  coldBrew: 'Cold Brew',
};

/** The Dart table spells the two pour actions with underscores. */
const ACTION_STRING_KEY: Record<PhaseAction, string> = {
  pourCircle: 'action_pour_circle',
  pourCenter: 'action_pour_center',
  wait: 'action_wait',
  stir: 'action_stir',
  swirl: 'action_swirl',
  cap: 'action_cap',
  flip: 'action_flip',
  press: 'action_press',
  openValve: 'action_openValve',
  closeValve: 'action_closeValve',
};

export function actionLabel(lang: string, action: PhaseAction): string {
  return str(lang, ACTION_STRING_KEY[action]);
}

export function isPourAction(action: PhaseAction): boolean {
  return action === 'pourCircle' || action === 'pourCenter';
}

export function beanLabel(lang: string, bean: string): string {
  if (bean === 'Blend') return str(lang, 'custom_bean_blend');
  if (bean === 'Bebas') return str(lang, 'custom_bean_bebas');
  if (bean === 'Custom') return str(lang, 'custom_bean_custom');
  return bean;
}

/** "3 minutes 30 seconds", spelled out: a screen reader reads "3:30" as a time of day. */
export function durationText(lang: string, totalSeconds: number): string {
  const minutes = Math.floor(totalSeconds / 60);
  const seconds = totalSeconds % 60;
  const parts: string[] = [];
  if (minutes > 0) parts.push(str(lang, minutes === 1 ? 'share_minute' : 'share_minutes', [minutes]));
  if (seconds > 0 || minutes === 0) {
    parts.push(str(lang, seconds === 1 ? 'share_second' : 'share_seconds', [seconds]));
  }
  return parts.join(' ');
}

/**
 * A recipe as plain text for the share sheet (WhatsApp, Telegram, email...).
 *
 * Written for a screen reader on the receiving end: one fact per line, no
 * emoji (read out by name, "hot beverage"), no table. Pour steps give
 * millilitres rather than rotations, because rotations depend on the sender's
 * own calibrated pouring speed. The grinder setting is the sender's grinder;
 * the micron size next to the grind category lets anyone else convert it.
 */
export function recipeShareText(recipe: Recipe, lang: string, grinder: GrinderModel | null): string {
  const lines: string[] = [];

  lines.push(str(lang, 'share_heading', [str(lang, recipe.name)]));
  lines.push(str(lang, 'share_method', [METHOD_NAMES[recipe.method] ?? recipe.method]));
  lines.push(
    str(lang, 'share_amounts', [
      trimNumber(recipe.coffeeGrams),
      trimNumber(recipe.totalWaterMl),
      durationText(lang, recipe.totalDurationSeconds),
    ])
  );
  lines.push(
    str(lang, 'share_grind', [
      getGrindCategoryName(recipe.targetGrindSizeMicrons, lang),
      recipe.targetGrindSizeMicrons,
    ])
  );
  if (grinder) {
    lines.push(`${grinder.name}: ${grinder.getSetting(recipe.targetGrindSizeMicrons).trim()}`);
  }
  lines.push(`${str(lang, 'brew_bean')}: ${beanLabel(lang, recipe.beanType)}`);
  if (recipe.extraIngredients.length > 0) {
    lines.push(`${str(lang, 'brew_extra')}: ${str(lang, recipe.extraIngredients)}`);
  }

  lines.push('');
  lines.push(str(lang, 'share_steps'));
  for (const phase of recipe.phases) {
    const amount = isPourAction(phase.action) ? ` ${trimNumber(phase.pourAmountMl)} ml` : '';
    lines.push(`${formatClock(phase.startTimeSeconds)} ${actionLabel(lang, phase.action)}${amount}`);
  }

  const notes = recipe.description.length > 0 ? str(lang, recipe.description).trim() : '';
  if (notes.length > 0) {
    lines.push('');
    lines.push(str(lang, 'share_notes', [notes]));
  }

  lines.push('');
  lines.push(str(lang, 'share_footer'));
  return lines.join('\n');
}
