// Ported from lib/screens/brewing_screen.dart.
//
// Two clocks run during a brew, exactly as in the Flutter build:
//
//   * The brew clock — a 50 ms interval measuring elapsed wall time, which
//     decides when phases begin and when each spoken cue fires. Elapsed time is
//     re-read every tick rather than accumulated, so a late interval callback
//     does not shift the rest of the brew.
//   * The metronome — the pre-rendered click track in src/core/audio/metronome.ts,
//     started per pour phase and stopped once the pour's seconds are up.
//
// They are deliberately independent: the brew clock may drift a few
// milliseconds without affecting the beat the user is pouring to.
import Icon from '../components/Icon';
import type { NativeStackScreenProps } from '@react-navigation/native-stack';
import { activateKeepAwakeAsync, deactivateKeepAwake } from 'expo-keep-awake';
import { useEffect, useLayoutEffect, useMemo, useRef, useState } from 'react';
import {
  AccessibilityInfo,
  findNodeHandle,
  Pressable,
  ScrollView,
  StyleSheet,
  Text,
  View,
} from 'react-native';

import { str } from '../core/appStrings';
import {
  playBell,
  startMetronome,
  stopMetronome,
} from '../core/audio/metronome';
import { speak, speakAndWait } from '../core/audio/speech';
import {
  activePhaseIndex,
  activePhaseText,
  buildDynamicRecipe,
  continuationCue,
  isPour,
  openingCue,
  phaseListText,
  pourDuration,
  prepareCue,
} from '../core/brewPlan';
import { getGrindCategoryName, grinderDatabase } from '../core/grinderDatabase';
import { formatClock, trimNumber } from '../core/recipe';
import { useCalibration } from '../core/stores/calibrationStore';
import { useSettings } from '../core/stores/settingsStore';
import type { RootStackParamList } from '../navigation';
import { colors, fontSize } from '../theme';

type Props = NativeStackScreenProps<RootStackParamList, 'Brewing'>;

/** Seconds of lead-in before the clock reaches 0, as in the Flutter build. */
const LEAD_IN_SECONDS = 4;
const TICK_MS = 50;

export default function BrewingScreen({ navigation, route }: Props) {
  const { recipe } = route.params;

  const settings = useSettings();
  const calibration = useCalibration();
  const lang = settings.appLanguage;

  const [isBrewing, setIsBrewing] = useState(false);
  const [currentSecond, setCurrentSecond] = useState(0);
  const [phaseIndex, setPhaseIndex] = useState(-1);
  const [beat, setBeat] = useState(0);
  const [metronomeOn, setMetronomeOn] = useState(false);

  // Mirrors of the above for the interval callback, which must not close over
  // stale render values.
  const brewingRef = useRef(false);
  const phaseIndexRef = useRef(-1);
  const phaseStartRef = useRef(0);
  const timerRef = useRef<ReturnType<typeof setInterval> | null>(null);
  const cancelButtonRef = useRef<View>(null);

  const { mlPerSecond, secondsPerRotation, spoonCapacityGrams, grinderId } = calibration;

  // Computed once: re-spacing the phases mid-brew would move the goalposts.
  const activeRecipe = useMemo(
    () => buildDynamicRecipe(recipe, mlPerSecond),
    // eslint-disable-next-line react-hooks/exhaustive-deps
    []
  );

  useLayoutEffect(() => {
    navigation.setOptions({ title: str(lang, recipe.name) });
  }, [navigation, lang, recipe.name]);

  const stopBrewing = async ({ finished = false }: { finished?: boolean } = {}) => {
    if (timerRef.current) {
      clearInterval(timerRef.current);
      timerRef.current = null;
    }
    brewingRef.current = false;
    void deactivateKeepAwake();

    stopMetronome();
    setMetronomeOn(false);
    setIsBrewing(false);

    if (finished) {
      playBell();
      // Let the chime ring before the closing line, or they talk over each other.
      await new Promise((resolve) => setTimeout(resolve, 1000));
      speak(str(lang, 'brew_complete'));
    }
  };

  // Failsafe: leaving the screen mid-brew must not leave audio running or the
  // screen pinned awake.
  useEffect(() => {
    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
      brewingRef.current = false;
      stopMetronome();
      void deactivateKeepAwake();
    };
  }, []);

  /** Speaks a phase's cue and, for pours, starts the beat the user pours to. */
  const processPhase = (index: number) => {
    const phase = activeRecipe.phases[index];
    const textParams = { phase, lang, mlPerSecond, secondsPerRotation };
    let actionDuration = 0;

    if (isPour(phase.action)) {
      actionDuration = pourDuration(phase, mlPerSecond);

      // When the previous pour ended less than 5s ago the 3-2-1 countdown was
      // skipped, so say "keep going" rather than "start".
      let isContinuation = false;
      if (index > 0) {
        const prev = activeRecipe.phases[index - 1];
        if (isPour(prev.action)) {
          const prevEnd = prev.startTimeSeconds + pourDuration(prev, mlPerSecond);
          if (phase.startTimeSeconds - prevEnd < 5) isContinuation = true;
        }
      }

      speak(isContinuation ? continuationCue(textParams) : lang === 'en' ? 'Start!' : 'Mulai!');
    } else if (phase.action === 'stir') {
      speak(str(lang, 'stir_instruction'));
    } else if (phase.action === 'swirl') {
      speak(str(lang, 'action_swirl'));
    } else if (phase.action === 'cap') {
      speak(str(lang, 'action_cap'));
    } else if (phase.action === 'flip') {
      speak(
        lang === 'en'
          ? 'Carefully flip the Aeropress.'
          : 'Balikkan alat seduh dengan hati-hati.'
      );
    } else if (phase.action === 'press') {
      speak(str(lang, 'press_instruction'));
    } else if (phase.action === 'openValve') {
      speak(str(lang, 'open_valve_instruction'));
    } else if (phase.action === 'closeValve') {
      speak(str(lang, 'close_valve_instruction'));
    } else if (phase.action === 'wait') {
      // Only worth saying after an action the user has to finish; after a pour
      // the "Stop / Wait" lines have already been spoken.
      if (index > 0) {
        const prev = activeRecipe.phases[index - 1].action;
        if (['stir', 'swirl', 'press', 'cap', 'flip'].includes(prev)) {
          speak(str(lang, 'action_wait'));
        }
      }
    }

    if (!isPour(phase.action)) return;

    setBeat(0);
    setMetronomeOn(true);
    startMetronome({
      audible: settings.audioMetronome,
      haptics: settings.hapticMetronome,
      offsetMs: settings.announcementOffsetMs,
      onBeat: (currentBeat) => {
        if (phaseIndexRef.current !== index) {
          stopMetronome();
          setMetronomeOn(false);
          return;
        }
        setBeat(currentBeat);
        if (currentBeat >= actionDuration) {
          stopMetronome();
          setMetronomeOn(false);
        }
      },
    });
  };

  const startBrewing = async () => {
    void activateKeepAwakeAsync();

    brewingRef.current = true;
    phaseIndexRef.current = -1;
    phaseStartRef.current = 0;
    setIsBrewing(true);
    setCurrentSecond(-LEAD_IN_SECONDS);
    setPhaseIndex(-1);

    // Move the screen reader onto Cancel before any cue is spoken, so its focus
    // is somewhere meaningful instead of wherever the previous screen left it.
    requestAnimationFrame(() => {
      try {
        const tag = findNodeHandle(cancelButtonRef.current);
        if (tag) AccessibilityInfo.setAccessibilityFocus(tag);
      } catch {
        // Focus is a nicety; never let it break the brew.
      }
    });

    // The clock starts only once this line has finished, so the user is not
    // already three seconds behind when they hear what to do.
    const first = activeRecipe.phases[0];
    if (first && isPour(first.action)) {
      await speakAndWait(
        openingCue({ phase: first, lang, mlPerSecond, secondsPerRotation })
      );
    } else {
      await speakAndWait(' '); // warms the TTS engine so the first real cue is prompt
    }

    if (!brewingRef.current) return; // stopped while speaking

    const startMs = Date.now();
    let lastProjectedSecond = -5;
    let lastActualSecond = -5;

    // Reserved for dialling the voice ahead of the clock on slow TTS engines;
    // the Flutter build left it at zero and so do we.
    const ttsOffsetMs = 0;

    timerRef.current = setInterval(() => {
      if (!brewingRef.current) return;

      const elapsedMs = Date.now() - startMs;
      const projectedSec = Math.floor((elapsedMs + ttsOffsetMs) / 1000) - LEAD_IN_SECONDS;
      const actualSec = Math.floor(elapsedMs / 1000) - LEAD_IN_SECONDS;

      if (projectedSec > lastProjectedSecond) {
        lastProjectedSecond = projectedSec;
        const second = projectedSec;
        const phases = activeRecipe.phases;

        if (!(second > 0 && second >= activeRecipe.totalDurationSeconds)) {
          const activeIdx = activePhaseIndex(phases, second);

          if (activeIdx !== -1 && activeIdx !== phaseIndexRef.current) {
            phaseIndexRef.current = activeIdx;
            phaseStartRef.current = phases[activeIdx].startTimeSeconds;
            setPhaseIndex(activeIdx);
            processPhase(activeIdx);
          }

          // Count down into any pour starting within the next 5 seconds.
          for (let i = activeIdx + 1; i < phases.length; i++) {
            const phase = phases[i];
            const timeUntil = phase.startTimeSeconds - second;
            if (timeUntil <= 0 || timeUntil > 5 || !isPour(phase.action)) continue;

            // A countdown that would land on top of the pour still in progress
            // is noise, so skip it when the gap is under 6 seconds.
            let currentPhaseEnd = phaseStartRef.current;
            if (activeIdx !== -1) {
              const current = phases[activeIdx];
              if (isPour(current.action)) {
                currentPhaseEnd += pourDuration(current, mlPerSecond);
              }
            }
            const skipCountdown =
              activeIdx !== -1 && phase.startTimeSeconds - currentPhaseEnd < 6;
            if (skipCountdown) continue;

            if (timeUntil === 5) {
              speak(prepareCue({ phase, lang, mlPerSecond, secondsPerRotation }));
            } else if (timeUntil === 3) {
              speak(lang === 'en' ? 'Three.' : 'Tiga.');
            } else if (timeUntil === 2) {
              speak(lang === 'en' ? 'Two.' : 'Dua.');
            } else if (timeUntil === 1) {
              speak(lang === 'en' ? 'One.' : 'Satu.');
            }
          }

          // Progress markers spoken during a pour: rotation number for circular
          // pours, every tenth second for centre pours, then stop and wait.
          if (activeIdx !== -1) {
            const current = phases[activeIdx];
            const elapsedInPhase = second - current.startTimeSeconds;

            if (isPour(current.action)) {
              const actionDuration = pourDuration(current, mlPerSecond);

              if (elapsedInPhase > 0 && elapsedInPhase < actionDuration) {
                if (current.action === 'pourCircle') {
                  if (elapsedInPhase % secondsPerRotation === 0) {
                    speak(String(Math.trunc(elapsedInPhase / secondsPerRotation)));
                  }
                } else if (elapsedInPhase % 10 === 0) {
                  speak(String(elapsedInPhase));
                }
              } else if (elapsedInPhase === actionDuration) {
                speak(lang === 'en' ? 'Stop.' : 'Berhenti.');
              } else if (elapsedInPhase === actionDuration + 1) {
                speak(lang === 'en' ? 'Wait.' : 'Tunggu.');
              }
            }
          }
        }
      }

      if (actualSec > lastActualSecond) {
        lastActualSecond = actualSec;
        setCurrentSecond(actualSec);
        if (actualSec > 0 && actualSec >= activeRecipe.totalDurationSeconds) {
          void stopBrewing({ finished: true });
        }
      }
    }, TICK_MS);
  };

  // ---------------------------------------------------------------- rendering

  let currentPhaseText = '';
  if (isBrewing && phaseIndex >= 0 && phaseIndex < activeRecipe.phases.length) {
    const phase = activeRecipe.phases[phaseIndex];
    const params = { phase, lang, mlPerSecond, secondsPerRotation };

    if (isPour(phase.action)) {
      const endPourSecond = phase.startTimeSeconds + pourDuration(phase, mlPerSecond);
      currentPhaseText =
        currentSecond < endPourSecond
          ? activePhaseText(params)
          : str(lang, 'wait_instruction');
    } else {
      currentPhaseText = activePhaseText(params);
    }
  }

  const isFinished = currentSecond >= recipe.totalDurationSeconds;
  const flashing = isBrewing && metronomeOn && settings.visualMetronome;
  const backgroundColor = flashing
    ? beat % 2 === 0
      ? colors.beatFlash
      : colors.background
    : colors.background;

  if (isBrewing) {
    return (
      <View style={[styles.screen, styles.centered, { backgroundColor }]}>
        <View
          accessible
          accessibilityLiveRegion="polite"
          accessibilityLabel={str(lang, 'brew_sec', [String(currentSecond), currentPhaseText])}
          style={styles.centered}
        >
          <Text style={styles.timer}>{currentSecond}</Text>
          <Text style={styles.phaseText}>{currentPhaseText}</Text>
        </View>

        <View style={{ height: 48 }} />

        <Pressable
          ref={cancelButtonRef}
          accessibilityRole="button"
          accessibilityLabel={str(lang, 'cancel_brew_btn')}
          onPress={async () => {
            await stopBrewing();
            navigation.goBack();
          }}
          style={({ pressed }) => [styles.cancelButton, pressed && styles.pressed]}
        >
          <Text style={styles.cancelText}>{str(lang, 'cancel_brew_btn')}</Text>
        </Pressable>
      </View>
    );
  }

  const dose = trimNumber(recipe.coffeeGrams);
  const water = String(Math.round(recipe.totalWaterMl));
  const spoonCount = recipe.coffeeGrams / spoonCapacityGrams;
  const spoonStr = spoonCount.toFixed(1).replace(/\.0$/, '');
  const grinder =
    grinderDatabase.find((g) => g.id === grinderId) ?? grinderDatabase[0];
  // One entry per line rather than one block of text: QA needs to reach each
  // fact by swiping, so "grind category" and "this grinder's setting" cannot
  // share a Text, and the box around them must not merge them either.
  const brewFacts: string[] = [
    str(lang, 'brew_dose', [spoonStr]),
    `${str(lang, 'brew_grind')}: ${getGrindCategoryName(recipe.targetGrindSizeMicrons, lang)}`,
    `${grinder.name}: ${grinder.getSetting(recipe.targetGrindSizeMicrons)}`,
    `${str(lang, 'brew_bean')}: ${recipe.beanType}`,
  ];
  if (recipe.extraIngredients.length > 0) {
    brewFacts.push(`${str(lang, 'brew_extra')}: ${str(lang, recipe.extraIngredients)}`);
  }

  return (
    <View style={styles.screen}>
      <ScrollView contentContainerStyle={styles.detailBody}>
        <Text
          accessibilityRole="header"
          accessibilityLabel={str(lang, 'recipe_label', [
            str(lang, recipe.name),
            dose,
            water,
          ])}
          style={styles.recipeHeading}
        >
          {`${str(lang, recipe.name)}\n${dose}g ☕ | ${water}ml 💧`}
        </Text>

        <View style={styles.infoBox}>
          {brewFacts.map((fact, index) => (
            <Text
              key={index}
              accessible
              style={[styles.infoText, index >= 3 && { color: colors.primary }]}
            >
              {fact}
            </Text>
          ))}
        </View>

        {recipe.description.length > 0 && (
          <View style={styles.descBox}>
            <Text accessibilityRole="header" style={styles.descTitle}>
              {str(lang, 'brew_desc_title')}
            </Text>
            <Text accessible style={styles.descText}>
              {str(lang, recipe.description)}
            </Text>
          </View>
        )}

        <Text accessibilityRole="header" style={styles.phasesHeading}>
          {str(lang, 'brew_phases')}
        </Text>

        {activeRecipe.phases.map((phase, index) => {
          const timeStr = formatClock(phase.startTimeSeconds);
          const itemText = phaseListText({ phase, lang, mlPerSecond, secondsPerRotation });
          const reached = phaseIndex >= index;
          return (
            <View
              key={`${phase.startTimeSeconds}-${index}`}
              accessible
              accessibilityLabel={`${timeStr}: ${itemText}`}
              style={styles.phaseRow}
            >
              <Text
                style={[
                  styles.phaseClock,
                  { color: reached ? colors.blue : colors.textDisabled },
                ]}
              >
                {timeStr}
              </Text>
              <Text
                style={[
                  styles.phaseLabel,
                  { color: reached ? colors.text : colors.textDisabled },
                ]}
              >
                {itemText}
              </Text>
            </View>
          );
        })}
      </ScrollView>

      <View style={styles.footer}>
        <Pressable
          accessibilityRole="button"
          accessibilityLabel={str(lang, isFinished ? 'finish_brew_btn' : 'start_brew_btn')}
          onPress={() => {
            if (isFinished) {
              navigation.goBack();
            } else {
              void startBrewing();
            }
          }}
          style={({ pressed }) => [
            styles.startButton,
            { backgroundColor: isFinished ? colors.blue : colors.green },
            pressed && styles.pressed,
          ]}
        >
          <Icon
            name={isFinished ? 'check' : 'play-arrow'}
            size={28}
            color={colors.onPrimary}
          />
          <Text style={styles.startText}>
            {str(lang, isFinished ? 'finish_brew_btn' : 'start_brew_btn')}
          </Text>
        </Pressable>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  screen: {
    flex: 1,
    backgroundColor: colors.background,
  },
  centered: {
    alignItems: 'center',
    justifyContent: 'center',
  },
  timer: {
    fontSize: fontSize.timer,
    fontWeight: 'bold',
    color: colors.text,
  },
  phaseText: {
    fontSize: fontSize.phase,
    color: colors.blue,
    textAlign: 'center',
    paddingHorizontal: 16,
  },
  cancelButton: {
    backgroundColor: colors.red,
    paddingHorizontal: 48,
    paddingVertical: 24,
    borderRadius: 4,
  },
  cancelText: {
    fontSize: fontSize.button,
    color: colors.onPrimary,
    fontWeight: '500',
  },
  detailBody: {
    padding: 16,
    paddingBottom: 24,
  },
  recipeHeading: {
    fontSize: fontSize.title,
    fontWeight: 'bold',
    color: colors.text,
    textAlign: 'center',
  },
  infoBox: {
    marginTop: 16,
    padding: 12,
    borderRadius: 8,
    backgroundColor: colors.blue50,
    borderWidth: 1,
    borderColor: colors.blue200,
    gap: 4,
  },
  infoText: {
    fontSize: fontSize.body,
    fontWeight: '600',
    color: colors.text,
  },
  descBox: {
    marginTop: 16,
    padding: 12,
    borderRadius: 8,
    backgroundColor: colors.yellow100,
  },
  descTitle: {
    fontSize: fontSize.subheading,
    fontWeight: 'bold',
    color: colors.primary,
    marginBottom: 4,
  },
  descText: {
    fontSize: fontSize.body,
    fontStyle: 'italic',
    color: colors.text,
  },
  phasesHeading: {
    marginTop: 16,
    marginBottom: 8,
    fontSize: fontSize.heading,
    fontWeight: 'bold',
    color: colors.text,
  },
  phaseRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 16,
    paddingVertical: 8,
  },
  phaseClock: {
    fontSize: fontSize.clock,
    fontWeight: 'bold',
    minWidth: 64,
  },
  phaseLabel: {
    flex: 1,
    fontSize: fontSize.subheading,
  },
  footer: {
    padding: 16,
  },
  startButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 8,
    paddingHorizontal: 48,
    paddingVertical: 24,
    borderRadius: 4,
  },
  startText: {
    fontSize: fontSize.button,
    color: colors.onPrimary,
    fontWeight: '500',
  },
  pressed: {
    opacity: 0.75,
  },
});
