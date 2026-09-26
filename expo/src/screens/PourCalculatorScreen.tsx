// Ported from lib/screens/pour_calculator_screen.dart.
//
// A standalone "pour N ml" drill: three-count in, then the metronome runs for
// the number of seconds that volume takes at the calibrated flow rate. Same
// two-clock arrangement as BrewingScreen — spoken cues off the wall clock, beats
// off the click track's own audio clock.
import Icon from '../components/Icon';
import type { NativeStackScreenProps } from '@react-navigation/native-stack';
import { activateKeepAwakeAsync, deactivateKeepAwake } from 'expo-keep-awake';
import { useEffect, useLayoutEffect, useRef, useState } from 'react';
import { Pressable, ScrollView, StyleSheet, Text, TextInput, View } from 'react-native';

import { str } from '../core/appStrings';
import { startMetronome, stopMetronome } from '../core/audio/metronome';
import { speak, speakAndWait } from '../core/audio/speech';
import { useCalibration } from '../core/stores/calibrationStore';
import { useSettings } from '../core/stores/settingsStore';
import type { RootStackParamList } from '../navigation';
import { colors, fontSize } from '../theme';

type Props = NativeStackScreenProps<RootStackParamList, 'PourCalculator'>;

const MIN_ML = 10;
const MAX_ML = 1000;
const STEP_ML = 10;
/** Seconds of "three, two, one, start" before the pour begins. */
const COUNT_IN_SECONDS = 4;
const TICK_MS = 50;

export default function PourCalculatorScreen({ navigation }: Props) {
  const settings = useSettings();
  const { mlPerSecond, isCalibrated } = useCalibration();
  const lang = settings.appLanguage;

  const [targetMl, setTargetMl] = useState(50);
  const [draft, setDraft] = useState<string | null>(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [isCountdown, setIsCountdown] = useState(false);
  const [counter, setCounter] = useState(0);
  const [beat, setBeat] = useState(0);
  const [metronomeOn, setMetronomeOn] = useState(false);

  const timerRef = useRef<ReturnType<typeof setInterval> | null>(null);
  const playingRef = useRef(false);

  useLayoutEffect(() => {
    navigation.setOptions({ title: str(lang, 'pour_calc_title') });
  }, [navigation, lang]);

  const estTime = mlPerSecond > 0 ? Math.round(targetMl / mlPerSecond) : 0;

  const stopPour = () => {
    if (timerRef.current) {
      clearInterval(timerRef.current);
      timerRef.current = null;
    }
    playingRef.current = false;
    stopMetronome();
    setMetronomeOn(false);
    void deactivateKeepAwake();
    setIsPlaying(false);
    setIsCountdown(false);
    setCounter(0);
  };

  // Failsafe on leaving the screen mid-drill.
  useEffect(() => {
    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
      playingRef.current = false;
      stopMetronome();
      void deactivateKeepAwake();
    };
  }, []);

  const startPour = async () => {
    if (playingRef.current) {
      stopPour();
      return;
    }
    if (mlPerSecond <= 0) return;

    const duration = Math.max(1, Math.round(targetMl / mlPerSecond));

    void activateKeepAwakeAsync();
    playingRef.current = true;
    setIsPlaying(true);
    setIsCountdown(true);
    setCounter(3);

    await speakAndWait(str(lang, 'pour_calc_ready'));
    if (!playingRef.current) return;

    const startMs = Date.now();
    let lastSecond = -1;
    let countingIn = true;

    timerRef.current = setInterval(() => {
      if (!playingRef.current) return;

      // Elapsed time is re-read rather than counted up, so a late callback does
      // not shorten the pour.
      const second = Math.floor((Date.now() - startMs) / 1000);
      if (second <= lastSecond) return;
      lastSecond = second;

      if (countingIn) {
        const count = 3 - second;
        if (count > 0) {
          speak(String(count));
          setCounter(count);
        } else if (count === 0) {
          speak(lang === 'en' ? 'Start!' : 'Mulai!');
          countingIn = false;
          setIsCountdown(false);
          setCounter(duration);
          setBeat(0);
          setMetronomeOn(true);
          startMetronome({
            audible: settings.audioMetronome,
            haptics: settings.hapticMetronome,
            offsetMs: settings.announcementOffsetMs,
            onBeat: setBeat,
          });
        }
        return;
      }

      const remaining = duration - (second - COUNT_IN_SECONDS);
      if (remaining === 0) speak(str(lang, 'pour_calc_stop'));
      if (remaining > 0) {
        setCounter(remaining);
      } else {
        stopPour();
      }
    }, TICK_MS);
  };

  const adjust = (delta: number) => {
    if (playingRef.current) return;
    setTargetMl((current) => Math.min(MAX_ML, Math.max(MIN_ML, current + delta)));
  };

  const flashing = isPlaying && !isCountdown && metronomeOn && settings.visualMetronome;
  const backgroundColor = flashing
    ? beat % 2 === 0
      ? colors.beatFlash
      : colors.background
    : colors.background;

  const buttonLabel = isPlaying
    ? isCountdown
      ? String(counter)
      : `${counter} s`
    : str(lang, 'pour_calc_start');

  return (
    <View style={[styles.screen, { backgroundColor }]}>
      <ScrollView contentContainerStyle={styles.body}>
        <Text style={styles.intro}>{str(lang, 'pour_calc_desc')}</Text>

        {!isCalibrated ? (
          <View accessible style={styles.warningBox}>
            <Text style={styles.warningText}>{str(lang, 'pour_calc_uncalibrated')}</Text>
          </View>
        ) : (
          <>
            <Text accessibilityRole="header" style={styles.question}>
              {str(lang, 'pour_calc_target')}
            </Text>

            <View style={styles.adjuster}>
              <Pressable
                accessibilityRole="button"
                accessibilityLabel={str(lang, 'reduce', [String(targetMl - STEP_ML), 'ml'])}
                accessibilityState={{ disabled: isPlaying }}
                disabled={isPlaying}
                onPress={() => adjust(-STEP_ML)}
                style={({ pressed }) => [
                  styles.adjusterButton,
                  isPlaying && styles.disabled,
                  pressed && styles.pressed,
                ]}
              >
                <Icon name="remove-circle-outline" size={48} color={colors.primary} />
              </Pressable>

              <TextInput
                // Named by its hint, not accessibilityLabel or labelFor: see
                // components/LabeledInput.tsx.
                placeholder={str(lang, 'pour_calc_target')}
                placeholderTextColor={colors.textDisabled}
                keyboardType="number-pad"
                editable={!isPlaying}
                style={styles.adjusterInput}
                value={draft ?? String(targetMl)}
                onChangeText={setDraft}
                // Start empty so typing replaces the target instead of editing
                // around it.
                onFocus={() => setDraft('')}
                onBlur={() => {
                  const parsed = parseInt(draft ?? '', 10);
                  if (Number.isFinite(parsed)) {
                    setTargetMl(Math.min(MAX_ML, Math.max(MIN_ML, parsed)));
                  }
                  setDraft(null);
                }}
              />

              {/* Visual only: the buttons on either side already say "ml". */}
              <Text
                accessibilityElementsHidden
                importantForAccessibility="no-hide-descendants"
                style={styles.adjusterUnit}
              >
                ml
              </Text>

              <Pressable
                accessibilityRole="button"
                accessibilityLabel={str(lang, 'add', [String(targetMl + STEP_ML), 'ml'])}
                accessibilityState={{ disabled: isPlaying }}
                disabled={isPlaying}
                onPress={() => adjust(STEP_ML)}
                style={({ pressed }) => [
                  styles.adjusterButton,
                  isPlaying && styles.disabled,
                  pressed && styles.pressed,
                ]}
              >
                <Icon name="add-circle-outline" size={48} color={colors.primary} />
              </Pressable>
            </View>

            <Text accessibilityLiveRegion="polite" style={styles.estimate}>
              {str(lang, 'pour_calc_est', [String(estTime)])}
            </Text>

            <Pressable
              accessibilityRole="button"
              accessibilityLabel={
                isPlaying ? str(lang, 'stop_metronome') : str(lang, 'pour_calc_start')
              }
              onPress={() => void startPour()}
              style={({ pressed }) => [
                styles.playButton,
                { backgroundColor: isPlaying ? '#FFCDD2' : colors.beatFlash },
                pressed && styles.pressed,
              ]}
            >
              <Icon
                name={isPlaying ? 'stop' : 'play-arrow'}
                size={36}
                color={isPlaying ? '#B71C1C' : colors.primaryDark}
              />
              <Text
                style={[
                  styles.playButtonText,
                  { color: isPlaying ? '#B71C1C' : colors.primaryDark },
                ]}
              >
                {buttonLabel}
              </Text>
            </Pressable>
          </>
        )}
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  screen: {
    flex: 1,
  },
  body: {
    padding: 16,
    paddingBottom: 48,
  },
  intro: {
    fontSize: fontSize.body,
    color: colors.text,
  },
  warningBox: {
    marginTop: 24,
    padding: 16,
    backgroundColor: '#FFCDD2',
    borderRadius: 4,
  },
  warningText: {
    fontSize: fontSize.subheading,
    fontWeight: 'bold',
    color: '#B71C1C',
  },
  question: {
    marginTop: 24,
    marginBottom: 16,
    fontSize: fontSize.subheading,
    fontWeight: 'bold',
    color: colors.text,
    textAlign: 'center',
  },
  adjuster: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 12,
  },
  adjusterButton: {
    width: 56,
    height: 56,
    alignItems: 'center',
    justifyContent: 'center',
  },
  adjusterInput: {
    width: 120,
    fontSize: fontSize.title,
    textAlign: 'center',
    color: colors.text,
    backgroundColor: colors.card,
    borderWidth: 1,
    borderColor: colors.divider,
    borderRadius: 4,
    paddingVertical: 10,
  },
  adjusterUnit: {
    fontSize: fontSize.heading,
    fontWeight: 'bold',
    color: colors.text,
  },
  estimate: {
    marginTop: 32,
    fontSize: fontSize.clock,
    fontWeight: 'bold',
    color: colors.blueGrey,
    textAlign: 'center',
  },
  playButton: {
    marginTop: 32,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 8,
    paddingVertical: 24,
    borderRadius: 4,
  },
  playButtonText: {
    fontSize: fontSize.button,
    fontWeight: '500',
  },
  disabled: {
    opacity: 0.35,
  },
  pressed: {
    opacity: 0.75,
  },
});
