// Ported from lib/screens/home_screen.dart.
import Icon, { type IconName } from '../components/Icon';
import type { NativeStackScreenProps } from '@react-navigation/native-stack';
import { useEffect } from 'react';
import { Pressable, ScrollView, StyleSheet, Text, View } from 'react-native';

import { str } from '../core/appStrings';
import { applySpeechSettings } from '../core/audio/speech';
import type { BrewMethod } from '../core/recipe';
import { useCalibration } from '../core/stores/calibrationStore';
import { useSettings } from '../core/stores/settingsStore';
import type { RootStackParamList } from '../navigation';
import { colors, fontSize } from '../theme';

type Props = NativeStackScreenProps<RootStackParamList, 'Home'>;

type MethodEntry = {
  method: BrewMethod;
  name: string;
  descKey: string;
  icon: IconName;
};

const METHODS: MethodEntry[] = [
  { method: 'v60', name: 'V60 / Pour-over', descKey: 'method_v60_desc', icon: 'filter-alt' },
  { method: 'frenchPress', name: 'French Press', descKey: 'method_fp_desc', icon: 'coffee' },
  { method: 'aeropress', name: 'Aeropress', descKey: 'method_ap_desc', icon: 'local-cafe' },
  { method: 'vietnamDrip', name: 'Vietnam Drip', descKey: 'method_vd_desc', icon: 'coffee-maker' },
  {
    method: 'cupping',
    name: 'SCA Cupping Protocol',
    descKey: 'method_cup_desc',
    icon: 'emoji-food-beverage',
  },
];

export default function HomeScreen({ navigation }: Props) {
  const settings = useSettings();
  const { isCalibrated, mlPerSecond } = useCalibration();
  const lang = settings.appLanguage;

  // Keep the speech layer in step with the settings screen, as the Flutter build
  // does by calling applySettings() on every rebuild of this screen.
  useEffect(() => {
    applySpeechSettings({
      language: settings.appLanguage,
      rate: settings.ttsSpeed,
      pitch: settings.ttsPitch,
      enabled: settings.isTtsEnabled,
      mode: settings.audioOutputMode,
      voice: settings.ttsVoiceName,
      voiceLocale: settings.ttsVoiceLocale,
    });
  }, [
    settings.appLanguage,
    settings.ttsSpeed,
    settings.ttsPitch,
    settings.isTtsEnabled,
    settings.audioOutputMode,
    settings.ttsVoiceName,
    settings.ttsVoiceLocale,
  ]);

  const flowRate = mlPerSecond.toFixed(1);
  const calibrationLabel = isCalibrated
    ? `${str(lang, 'calibrate_flow_rate')}. ${str(lang, 'calibrated_status', [flowRate])}`
    : `${str(lang, 'calibrate_flow_rate')}. ${str(lang, 'uncalibrated_status')}`;

  return (
    <View style={styles.screen}>
      <View style={styles.section}>
        <Pressable
          accessible
          accessibilityRole="button"
          accessibilityLabel={calibrationLabel}
          onPress={() => navigation.navigate('Calibration')}
          style={({ pressed }) => [
            styles.bigButton,
            { backgroundColor: isCalibrated ? colors.green : colors.red },
            pressed && styles.pressed,
          ]}
        >
          <Icon name="water-drop" size={24} color={colors.onPrimary} />
          {/*
            Hidden from the reader so the button is a single stop that reads
            "calibrate flow rate, <status>". Without this the inner text becomes
            a second stop saying the status again, which is what QA reported.
          */}
          <Text
            importantForAccessibility="no-hide-descendants"
            style={styles.bigButtonText}
          >
            {isCalibrated
              ? str(lang, 'calibrated_btn', [flowRate])
              : `${str(lang, 'calibrate_flow_rate')}\n${str(lang, 'uncalibrated_btn')}`}
          </Text>
        </Pressable>
      </View>

      <View style={styles.sectionHorizontal}>
        <Pressable
          accessible
          accessibilityRole="button"
          accessibilityLabel={str(lang, 'pour_calc_title')}
          onPress={() => navigation.navigate('PourCalculator')}
          style={({ pressed }) => [styles.calcButton, pressed && styles.pressed]}
        >
          <Icon name="calculate" size={24} color={colors.onPrimary} />
          <Text
            importantForAccessibility="no-hide-descendants"
            style={styles.calcButtonText}
          >
            {str(lang, 'pour_calc_title')}
          </Text>
        </Pressable>
      </View>

      <Text accessibilityRole="header" style={styles.sectionHeading}>
        {str(lang, 'home_select_method')}
      </Text>

      <ScrollView contentContainerStyle={styles.list}>
        {METHODS.map((entry) => {
          const desc = str(lang, entry.descKey);
          return (
            <Pressable
              key={entry.method}
              accessible
              // No role="button": a brewing method is an item in a list of
              // methods, and QA asked for the extra "button" to go.
              accessibilityLabel={`${entry.name}. ${desc}`}
              onPress={() =>
                navigation.navigate('MethodRecipes', {
                  method: entry.method,
                  methodName: entry.name,
                })
              }
              style={({ pressed }) => [styles.card, pressed && styles.pressed]}
            >
              <Icon name={entry.icon} size={40} color={colors.primary} />
              <View
                importantForAccessibility="no-hide-descendants"
                style={styles.cardBody}
              >
                <Text style={styles.cardTitle}>{entry.name}</Text>
                <Text style={styles.cardSubtitle}>{desc}</Text>
              </View>
            </Pressable>
          );
        })}
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  screen: {
    flex: 1,
    backgroundColor: colors.background,
  },
  section: {
    padding: 16,
  },
  sectionHorizontal: {
    paddingHorizontal: 16,
  },
  bigButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 8,
    paddingVertical: 24,
    paddingHorizontal: 32,
    borderRadius: 4,
  },
  bigButtonText: {
    color: colors.onPrimary,
    fontSize: fontSize.body,
    fontWeight: '500',
    textAlign: 'center',
  },
  calcButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 8,
    paddingVertical: 18,
    borderRadius: 4,
    backgroundColor: colors.teal,
  },
  calcButtonText: {
    color: colors.onPrimary,
    fontSize: fontSize.subheading,
    fontWeight: '500',
    textAlign: 'center',
  },
  sectionHeading: {
    fontSize: fontSize.subheading,
    fontWeight: 'bold',
    color: colors.text,
    paddingHorizontal: 16,
    paddingTop: 24,
    paddingBottom: 8,
  },
  list: {
    paddingBottom: 24,
  },
  card: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 16,
    backgroundColor: colors.card,
    borderRadius: 4,
    marginHorizontal: 16,
    marginBottom: 12,
    padding: 16,
    elevation: 1,
  },
  cardBody: {
    flex: 1,
  },
  cardTitle: {
    fontSize: fontSize.subheading,
    fontWeight: 'bold',
    color: colors.text,
  },
  cardSubtitle: {
    fontSize: 14,
    color: colors.textSecondary,
    marginTop: 2,
  },
  pressed: {
    opacity: 0.75,
  },
});
