// Pure brewing calculations, extracted from lib/screens/brewing_screen.dart.
//
// Every pour's length depends on the user's measured flow rate, so a recipe's
// written phase times are only a starting point: they get pushed apart until no
// pour overlaps the next instruction. Keeping that arithmetic here, away from
// the timer and the widgets, makes it checkable against the Dart line by line.
import { str } from './appStrings';
import { PhaseAction, Recipe, RecipePhase } from './recipe';

export const POUR_ACTIONS: PhaseAction[] = ['pourCircle', 'pourCenter'];

export function isPour(action: PhaseAction): boolean {
  return action === 'pourCircle' || action === 'pourCenter';
}

/** How long a pour takes at the calibrated flow rate, in whole seconds. */
export function pourDuration(phase: RecipePhase, mlPerSecond: number): number {
  return Math.round(phase.pourAmountMl / mlPerSecond);
}

/**
 * Rotation count as spoken/shown, without the unit.
 *
 * Rounded to the nearest half turn, and a half is spelled out ("2 setengah")
 * rather than read as a decimal, which a screen reader would mangle.
 */
export function rotationsValueText(
  actionDuration: number,
  secondsPerRotation: number,
  lang: string
): string {
  const rotations = actionDuration / secondsPerRotation;
  const rounded = Math.round(rotations * 2) / 2;
  if (rounded % 1 === 0) return String(Math.trunc(rounded));

  const half = str(lang, 'rotations_half');
  return rounded.toFixed(1).split('.5').join(half).split('.0').join('');
}

/** Rotation count with its unit, e.g. "2 setengah putaran" / "3 rotations". */
export function rotationsText(
  actionDuration: number,
  secondsPerRotation: number,
  lang: string
): string {
  const unit = lang === 'en' ? 'rotations' : 'putaran';
  return `${rotationsValueText(actionDuration, secondsPerRotation, lang)} ${unit}`;
}

/**
 * Spreads a recipe's phases so no instruction arrives while the previous pour is
 * still running, and extends the total duration by however much was added.
 */
export function buildDynamicRecipe(recipe: Recipe, mlPerSecond: number): Recipe {
  const phases: RecipePhase[] = [];
  let timeShift = 0;
  let lastEndSecond = 0;

  recipe.phases.forEach((phase) => {
    let proposedStart = phase.startTimeSeconds + timeShift;

    if (proposedStart <= lastEndSecond && phases.length > 0) {
      const extraShift = lastEndSecond - proposedStart + 1; // 1s gap for safety
      timeShift += extraShift;
      proposedStart += extraShift;
    }

    phases.push({
      startTimeSeconds: proposedStart,
      pourAmountMl: phase.pourAmountMl,
      instructionText: phase.instructionText,
      action: phase.action,
    });

    lastEndSecond = isPour(phase.action)
      ? proposedStart + pourDuration(phase, mlPerSecond)
      : proposedStart + 2;
  });

  const totalDurationSeconds = Math.max(
    recipe.totalDurationSeconds + timeShift,
    lastEndSecond
  );

  return { ...recipe, phases, totalDurationSeconds };
}

interface PhaseTextParams {
  phase: RecipePhase;
  lang: string;
  mlPerSecond: number;
  secondsPerRotation: number;
}

/** The large instruction line shown while a phase is active. */
export function activePhaseText({
  phase,
  lang,
  mlPerSecond,
  secondsPerRotation,
}: PhaseTextParams): string {
  const amount = String(Math.round(phase.pourAmountMl));

  switch (phase.action) {
    case 'pourCircle': {
      const duration = pourDuration(phase, mlPerSecond);
      const rot = rotationsValueText(duration, secondsPerRotation, lang);
      return str(lang, 'pour_circle_instruction', [amount, rot]);
    }
    case 'pourCenter': {
      const duration = pourDuration(phase, mlPerSecond);
      return str(lang, 'pour_center_instruction', [amount, String(duration)]);
    }
    case 'stir':
      return str(lang, 'stir_instruction');
    case 'swirl':
      return str(lang, 'action_swirl');
    case 'cap':
      return str(lang, 'action_cap');
    case 'flip':
      return lang === 'en' ? 'Flip Aeropress' : 'Balikkan Alat';
    case 'press':
      return str(lang, 'press_instruction');
    case 'openValve':
      return str(lang, 'open_valve_instruction');
    case 'closeValve':
      return str(lang, 'close_valve_instruction');
    case 'wait':
    default:
      return str(lang, 'wait_instruction');
  }
}

/** One row of the phase list on the pre-brew screen. */
export function phaseListText({
  phase,
  lang,
  mlPerSecond,
  secondsPerRotation,
}: PhaseTextParams): string {
  const amount = phase.pourAmountMl;
  const amountStr = Number.isInteger(amount)
    ? String(amount)
    : amount.toFixed(1).replace(/\.0$/, '');

  switch (phase.action) {
    case 'pourCircle': {
      const duration = pourDuration(phase, mlPerSecond);
      const rot = rotationsValueText(duration, secondsPerRotation, lang);
      return lang === 'en'
        ? `Pour ${amountStr} ml (${rot} rotations)`
        : `Tuang ${amountStr} ml (${rot} putaran)`;
    }
    case 'pourCenter': {
      const duration = pourDuration(phase, mlPerSecond);
      return lang === 'en'
        ? `Center pour ${amountStr} ml (${duration} sec)`
        : `Tuang tengah ${amountStr} ml (${duration} detik)`;
    }
    case 'stir':
      return str(lang, 'action_stir');
    case 'swirl':
      return str(lang, 'action_swirl');
    case 'cap':
      return str(lang, 'action_cap');
    case 'flip':
      return lang === 'en' ? 'Flip Aeropress' : 'Balikkan Alat';
    case 'press':
      return lang === 'en' ? 'Press' : 'Tekan perlahan';
    case 'openValve':
      return lang === 'en' ? 'Open Valve/Switch' : 'Buka Keran/Switch';
    case 'closeValve':
      return lang === 'en' ? 'Close Valve/Switch' : 'Tutup Keran/Switch';
    case 'wait':
    default:
      return lang === 'en' ? 'Wait' : 'Tunggu...';
  }
}

/** "Prepare to pour, 2 setengah putaran." — the cue 5 seconds before a pour. */
export function prepareCue({
  phase,
  lang,
  mlPerSecond,
  secondsPerRotation,
}: PhaseTextParams): string {
  const duration = pourDuration(phase, mlPerSecond);

  if (phase.action === 'pourCircle') {
    const rot = rotationsText(duration, secondsPerRotation, lang);
    return lang === 'en' ? `Prepare to pour, ${rot}.` : `Siap, tuang ${rot}.`;
  }
  return lang === 'en'
    ? `Prepare for center pour, ${duration} seconds.`
    : `Siap, tuang tengah ${duration} detik.`;
}

/**
 * The same cue, in the slightly longer wording used once before the clock
 * starts. The Flutter build says "Siap-siap" there and "Siap" mid-brew.
 */
export function openingCue({
  phase,
  lang,
  mlPerSecond,
  secondsPerRotation,
}: PhaseTextParams): string {
  const duration = pourDuration(phase, mlPerSecond);

  if (phase.action === 'pourCircle') {
    const rot = rotationsText(duration, secondsPerRotation, lang);
    return lang === 'en' ? `Prepare to pour, ${rot}.` : `Siap-siap, tuang ${rot}.`;
  }
  return lang === 'en'
    ? `Prepare for center pour, ${duration} seconds.`
    : `Siap-siap, tuang tengah ${duration} detik.`;
}

/** "Lanjut tuang ..." when a pour follows straight on from the previous one. */
export function continuationCue({
  phase,
  lang,
  mlPerSecond,
  secondsPerRotation,
}: PhaseTextParams): string {
  const duration = pourDuration(phase, mlPerSecond);

  if (phase.action === 'pourCircle') {
    const rot = rotationsText(duration, secondsPerRotation, lang);
    return lang === 'en' ? `Continue, ${rot}.` : `Lanjut tuang ${rot}.`;
  }
  return lang === 'en'
    ? `Continue center pour, ${duration} seconds.`
    : `Lanjut tuang tengah, ${duration} detik.`;
}

/** Index of the latest phase that has started by `second`, or -1. */
export function activePhaseIndex(phases: RecipePhase[], second: number): number {
  let index = -1;
  phases.forEach((phase, i) => {
    if (second >= phase.startTimeSeconds) index = i;
  });
  return index;
}
