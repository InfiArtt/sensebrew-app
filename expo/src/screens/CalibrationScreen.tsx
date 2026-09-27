// Ported from lib/screens/calibration_screen.dart.
//
// This is the screen that drove the Flutter build to a custom Kotlin EditText
// (NativeTextFieldView.kt) because Flutter's own field fought with TalkBack's
// swipe navigation. The numeric fields here are components/TextField, which is
// that same plain EditText again.
//
// Each question is shown above its control but read only once, by the control:
// the heading is hidden from the screen reader, since the field's hint (or the
// grinder button's label) already says it.
import Icon from '../components/Icon';
import TextField from '../components/TextField';
import VisualText from '../components/VisualText';
import type { NativeStackScreenProps } from '@react-navigation/native-stack';
import { useLayoutEffect, useRef, useState } from 'react';
import {
  AccessibilityInfo,
  Platform,
  Pressable,
  ScrollView,
  StyleSheet,
  Text,
  ToastAndroid,
  View,
} from 'react-native';

import SelectSheet from '../components/SelectSheet';
import { str } from '../core/appStrings';
import { startMetronome, stopMetronome } from '../core/audio/metronome';
import { speak } from '../core/audio/speech';
import { grinderDatabase } from '../core/grinderDatabase';
import { useCalibration } from '../core/stores/calibrationStore';
import { useSettings } from '../core/stores/settingsStore';
import type { RootStackParamList } from '../navigation';
import { colors, fontSize } from '../theme';

type Props = NativeStackScreenProps<RootStackParamList, 'Calibration'>;

interface AdjusterProps {
  lang: string;
  value: number;
  unit: string;
  /**
   * The question this number answers ("How many ml...?"). It becomes the
   * field's hint, so the field names itself when reached, rather than being
   * announced as just "ml".
   */
  question: string;
  minVal: number;
  step: number;
  onChange: (value: number) => void;
}

/**
 * A number with a minus and a plus button.
 *
 * Each control is its own focusable node in reading order — minus, field, plus —
 * so a swipe lands on all three rather than skipping the field, which is what
 * went wrong in the Flutter build (MIGRATION_HANDOVER.md, issue 1). The unit
 * text beside the field is visual only: the buttons already say the unit, and
 * as a stop of its own it doubled the swipes through each group.
 *
 * The field is named by its hint; see components/LabeledInput.tsx for why not
 * accessibilityLabel or accessibilityLabelledBy.
 */
function Adjuster({ lang, value, unit, question, minVal, step, onChange }: AdjusterProps) {
  // Holds what the user is typing. The field selects its number on focus, so
  // typing overwrites it rather than editing around it — QA asked for exactly
  // that, since landing in a field that already reads "200" and typing "50"
  // otherwise gives you 20050 or 50200 depending on where the cursor sat.
  //
  // It is selected, not cleared: clearing on focus meant the screen reader,
  // which now gives the field focus as soon as it lands on it, announced only
  // the question and never the number.
  const [draft, setDraft] = useState<string | null>(null);

  return (
    <View style={styles.adjuster}>
      <Pressable
        accessibilityRole="button"
        accessibilityLabel={str(lang, 'reduce', [String(value - step), unit])}
        onPress={() => {
          if (value - step >= minVal) onChange(value - step);
        }}
        style={({ pressed }) => [styles.adjusterButton, pressed && styles.pressed]}
      >
        <Icon name="remove-circle" size={48} color={colors.red} />
      </Pressable>

      <TextField
        hint={question}
        keyboardType="number-pad"
        fontSize={fontSize.title}
        textAlign="center"
        style={styles.adjusterInput}
        value={draft ?? String(value)}
        onChangeText={setDraft}
        selectAllOnFocus
        onBlur={() => {
          const parsed = parseInt(draft ?? '', 10);
          if (Number.isFinite(parsed) && parsed >= minVal) onChange(parsed);
          // Dropping the draft falls back to the committed value, so leaving the
          // field empty restores the previous number instead of clearing it.
          setDraft(null);
        }}
      />

      <Text
        accessibilityElementsHidden
        importantForAccessibility="no-hide-descendants"
        style={styles.adjusterUnit}
      >
        {unit}
      </Text>

      <Pressable
        accessibilityRole="button"
        accessibilityLabel={str(lang, 'add', [String(value + step), unit])}
        onPress={() => onChange(value + step)}
        style={({ pressed }) => [styles.adjusterButton, pressed && styles.pressed]}
      >
        <Icon name="add-circle" size={48} color={colors.green} />
      </Pressable>
    </View>
  );
}

export default function CalibrationScreen({ navigation }: Props) {
  const settings = useSettings();
  const calibration = useCalibration();
  const lang = settings.appLanguage;

  const [targetVolume, setTargetVolume] = useState(calibration.lastVolume);
  const [totalSeconds, setTotalSeconds] = useState(calibration.lastSeconds);
  const [secondsPerRotation, setSecondsPerRotation] = useState(
    Math.trunc(calibration.secondsPerRotation)
  );
  const [spoonCapacity, setSpoonCapacity] = useState(calibration.spoonCapacityGrams);
  const [grinderPickerOpen, setGrinderPickerOpen] = useState(false);
  const [playing, setPlaying] = useState(false);
  const [selectedGrinderId, setSelectedGrinderId] = useState(() =>
    grinderDatabase.some((g) => g.id === calibration.grinderId)
      ? calibration.grinderId
      : grinderDatabase[0].id
  );

  const countdownRef = useRef<ReturnType<typeof setInterval> | null>(null);

  useLayoutEffect(() => {
    navigation.setOptions({ title: str(lang, 'calib_header') });
  }, [navigation, lang]);

  const tickLabel = lang === 'en' ? 'TICKS' : 'TIK';
  const selectedGrinder =
    grinderDatabase.find((g) => g.id === selectedGrinderId) ?? grinderDatabase[0];

  const stopSimulation = () => {
    if (countdownRef.current) {
      clearInterval(countdownRef.current);
      countdownRef.current = null;
    }
    stopMetronome();
    setPlaying(false);
  };

  /** Counts "three, two, one, start" and then runs the beat to pour against. */
  const startSimulation = () => {
    setPlaying(true);
    let count = -3;

    countdownRef.current = setInterval(() => {
      if (count === -3) speak(lang === 'en' ? 'Three' : 'Tiga');
      else if (count === -2) speak(lang === 'en' ? 'Two' : 'Dua');
      else if (count === -1) speak(lang === 'en' ? 'One' : 'Satu');
      else if (count === 0) {
        speak(lang === 'en' ? 'Start' : 'Mulai');
        startMetronome({
          audible: settings.audioMetronome,
          haptics: settings.hapticMetronome,
          offsetMs: settings.announcementOffsetMs,
        });
        if (countdownRef.current) {
          clearInterval(countdownRef.current);
          countdownRef.current = null;
        }
      }
      count += 1;
    }, 1000);
  };

  const save = async () => {
    stopSimulation();
    await calibration.save({
      targetVolumeMl: targetVolume,
      totalSeconds,
      secondsPerRotation,
      spoonCapacity,
      grinderId: selectedGrinderId,
    });

    const message = str(lang, 'save_success');
    AccessibilityInfo.announceForAccessibility(message);
    if (Platform.OS === 'android') ToastAndroid.show(message, ToastAndroid.SHORT);
    navigation.goBack();
  };

  return (
    <View style={styles.screen}>
      <ScrollView contentContainerStyle={styles.body}>
        <View accessible style={styles.guideBox}>
          <Text style={styles.guideText}>{str(lang, 'calib_guide')}</Text>
        </View>

        <Pressable
          accessibilityRole="button"
          accessibilityLabel={playing ? str(lang, 'stop_metronome') : str(lang, 'calib_sim_btn')}
          onPress={() => (playing ? stopSimulation() : startSimulation())}
          style={({ pressed }) => [
            styles.simButton,
            { backgroundColor: playing ? '#FFCDD2' : '#BBDEFB' }, // red.100 / blue.100
            pressed && styles.pressed,
          ]}
        >
          <Icon
            name={playing ? 'stop' : 'play-arrow'}
            size={28}
            color={colors.text}
          />
          <VisualText style={styles.simButtonText}>
            {playing ? str(lang, 'stop_metronome') : str(lang, 'calib_sim_btn')}
          </VisualText>
        </Pressable>

        {/* Visual only: the control below says the same thing. */}
        <Text
          accessibilityElementsHidden
          importantForAccessibility="no-hide-descendants"
          style={styles.question}
        >
          {str(lang, 'calib_grinder_select')}
        </Text>
        <Pressable
          accessibilityRole="button"
          accessibilityLabel={`${str(lang, 'calib_grinder_select')}. ${selectedGrinder.name}`}
          onPress={() => setGrinderPickerOpen(true)}
          style={({ pressed }) => [styles.grinderCard, pressed && styles.pressed]}
        >
          <VisualText style={styles.grinderName}>{selectedGrinder.name}</VisualText>
          <Icon name="arrow-drop-down" size={30} color={colors.text} />
        </Pressable>

        {/* Visual only: the control below says the same thing. */}
        <Text
          accessibilityElementsHidden
          importantForAccessibility="no-hide-descendants"
          style={styles.question}
        >
          {str(lang, 'calib_spoon_q')}
        </Text>
        <Adjuster
          lang={lang}
          value={Math.trunc(spoonCapacity)}
          unit="gram"
          question={str(lang, 'calib_spoon_q')}
          minVal={1}
          step={1}
          onChange={(v) => setSpoonCapacity(v)}
        />

        {/* Visual only: the control below says the same thing. */}
        <Text
          accessibilityElementsHidden
          importantForAccessibility="no-hide-descendants"
          style={styles.question}
        >
          {str(lang, 'calib_q1')}
        </Text>
        <Adjuster
          lang={lang}
          value={targetVolume}
          unit="ml"
          question={str(lang, 'calib_q1')}
          minVal={10}
          step={10}
          onChange={setTargetVolume}
        />

        {/* Visual only: the control below says the same thing. */}
        <Text
          accessibilityElementsHidden
          importantForAccessibility="no-hide-descendants"
          style={styles.question}
        >
          {str(lang, 'calib_q2')}
        </Text>
        <Adjuster
          lang={lang}
          value={totalSeconds}
          unit={tickLabel}
          question={str(lang, 'calib_q2')}
          minVal={1}
          step={1}
          onChange={setTotalSeconds}
        />

        {/* Visual only: the control below says the same thing. */}
        <Text
          accessibilityElementsHidden
          importantForAccessibility="no-hide-descendants"
          style={styles.question}
        >
          {str(lang, 'calib_q3')}
        </Text>
        <Adjuster
          lang={lang}
          value={secondsPerRotation}
          unit={tickLabel}
          question={str(lang, 'calib_q3')}
          minVal={1}
          step={1}
          onChange={setSecondsPerRotation}
        />

        <Pressable
          accessibilityRole="button"
          accessibilityLabel={str(lang, 'save_calib_label')}
          onPress={() => void save()}
          style={({ pressed }) => [styles.saveButton, pressed && styles.pressed]}
        >
          <VisualText style={styles.saveText}>{str(lang, 'save_calib_label')}</VisualText>
        </Pressable>
      </ScrollView>

      {/*
        This picker used to be a hand-rolled Modal identical to SelectSheet. It is
        the shared component now, so the accessibility fixes QA asked for land here
        too instead of having to be made twice.
      */}
      <SelectSheet
        visible={grinderPickerOpen}
        title={str(lang, 'calib_grinder_title')}
        options={grinderDatabase.map((grinder) => ({
          value: grinder.id,
          label: grinder.name,
          detail: str(lang, grinder.isManual ? 'calib_grinder_manual' : 'calib_grinder_electric'),
        }))}
        currentValue={selectedGrinderId}
        selectedSuffix={str(lang, 'selected_suffix')}
        onClose={() => setGrinderPickerOpen(false)}
        onSelect={(value) => {
          setSelectedGrinderId(value);
          setGrinderPickerOpen(false);
        }}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  screen: {
    flex: 1,
    backgroundColor: colors.background,
  },
  body: {
    padding: 16,
    paddingBottom: 48,
  },
  guideBox: {
    padding: 16,
    borderRadius: 8,
    backgroundColor: colors.blue50,
    borderWidth: 1,
    borderColor: colors.blue200,
  },
  guideText: {
    fontSize: fontSize.subheading,
    color: colors.text,
  },
  simButton: {
    marginTop: 32,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 8,
    paddingVertical: 16,
    borderRadius: 4,
  },
  simButtonText: {
    fontSize: fontSize.subheading,
    color: colors.text,
    fontWeight: '500',
  },
  question: {
    marginTop: 24,
    marginBottom: 8,
    fontSize: fontSize.subheading,
    fontWeight: 'bold',
    color: colors.text,
  },
  grinderCard: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    backgroundColor: colors.card,
    borderRadius: 4,
    paddingVertical: 14,
    paddingHorizontal: 16,
    elevation: 1,
  },
  grinderName: {
    fontSize: fontSize.subheading,
    color: colors.text,
    flex: 1,
  },
  adjuster: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
  },
  adjusterButton: {
    width: 56,
    height: 56,
    alignItems: 'center',
    justifyContent: 'center',
  },
  adjusterInput: {
    flex: 1,
    backgroundColor: colors.card,
    borderWidth: 1,
    borderColor: colors.divider,
    borderRadius: 4,
  },
  adjusterUnit: {
    fontSize: fontSize.heading,
    fontWeight: 'bold',
    color: colors.text,
  },
  saveButton: {
    marginTop: 32,
    backgroundColor: colors.green,
    padding: 16,
    borderRadius: 4,
    alignItems: 'center',
  },
  saveText: {
    fontSize: fontSize.button,
    color: colors.onPrimary,
    fontWeight: '500',
  },
  pressed: {
    opacity: 0.75,
  },
});
