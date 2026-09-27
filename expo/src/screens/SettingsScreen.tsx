// Ported from lib/screens/settings_screen.dart.
import Icon from '../components/Icon';
import VisualText from '../components/VisualText';
import type { NativeStackScreenProps } from '@react-navigation/native-stack';
import Slider from '@react-native-community/slider';
import * as Speech from 'expo-speech';
import { useEffect, useLayoutEffect, useState } from 'react';
import {
  AccessibilityInfo,
  Alert,
  Modal,
  Platform,
  Pressable,
  ScrollView,
  StyleSheet,
  Switch,
  Text,
  ToastAndroid,
  View,
} from 'react-native';

import LabeledInput from '../components/LabeledInput';
import SelectSheet, { SelectOption } from '../components/SelectSheet';
import { str } from '../core/appStrings';
import {
  applySpeechSettings,
  availableVoices,
  previewVoice,
  speak,
} from '../core/audio/speech';
import { useRecipes } from '../core/stores/recipeStore';
import { useSettings } from '../core/stores/settingsStore';
import type { RootStackParamList } from '../navigation';
import { colors, fontSize } from '../theme';

type Props = NativeStackScreenProps<RootStackParamList, 'Settings'>;

/** Which picker sheet is open, if any. */
type Sheet = 'language' | 'provider' | 'channel' | 'voice' | null;

function notify(message: string) {
  AccessibilityInfo.announceForAccessibility(message);
  if (Platform.OS === 'android') ToastAndroid.show(message, ToastAndroid.SHORT);
}

interface RowProps {
  title: string;
  subtitle?: string;
  children: React.ReactNode;
}

/**
 * A titled row around one control. The control must name itself with the title
 * ("AI Provider. Gemini"), so the title on screen is hidden from the screen
 * reader: read here as well, QA heard it twice. The subtitle is not repeated
 * anywhere and stays readable.
 */
function SettingRow({ title, subtitle, children }: RowProps) {
  return (
    <View style={styles.row}>
      <View style={styles.rowText}>
        <Text
          accessibilityElementsHidden
          importantForAccessibility="no-hide-descendants"
          style={styles.rowTitle}
        >
          {title}
        </Text>
        {subtitle !== undefined && <Text style={styles.rowSubtitle}>{subtitle}</Text>}
      </View>
      {children}
    </View>
  );
}

interface ToggleProps {
  title: string;
  subtitle: string;
  value: boolean;
  onValueChange: (value: boolean) => void;
}

function ToggleRow({ title, subtitle, value, onValueChange }: ToggleProps) {
  return (
    <Pressable
      accessible
      accessibilityRole="switch"
      accessibilityLabel={`${title}. ${subtitle}`}
      accessibilityState={{ checked: value }}
      onPress={() => onValueChange(!value)}
      style={({ pressed }) => [styles.row, pressed && styles.pressed]}
    >
      <View style={styles.rowText}>
        <VisualText style={styles.rowTitle}>{title}</VisualText>
        <VisualText style={styles.rowSubtitle}>{subtitle}</VisualText>
      </View>
      <Switch
        value={value}
        onValueChange={onValueChange}
        trackColor={{ true: colors.primary }}
        // The whole row is one switch to the screen reader; a second focusable
        // control inside it would be read twice.
        accessibilityElementsHidden
        importantForAccessibility="no-hide-descendants"
      />
    </Pressable>
  );
}

interface SliderRowProps {
  title: string;
  value: number;
  min: number;
  max: number;
  step: number;
  format: (value: number) => string;
  /** Live, while dragging — mirrors Flutter's Slider onChanged. */
  onChange: (value: number) => void;
  /** On release — mirrors onChangeEnd, which is where Flutter speaks. */
  onSettle: (value: number) => void;
}

/**
 * A slider, as in the Flutter build.
 *
 * This started out as a pair of +/- buttons on the theory that a slider is hard
 * to use without sight. QA corrected that: these are sliders in Flutter, and a
 * @react-native-community/slider is a real Android SeekBar, which screen readers
 * already know how to drive — they announce it as a slider and adjust it with
 * their own gestures. accessibilityValue gives it something friendlier to read
 * out than a raw number.
 */
function SliderRow({
  title,
  value,
  min,
  max,
  step,
  format,
  onChange,
  onSettle,
}: SliderRowProps) {
  return (
    <View style={styles.sliderBlock}>
      {/* Visual only: the slider itself announces its title and value. */}
      <Text
        accessibilityElementsHidden
        importantForAccessibility="no-hide-descendants"
        style={styles.rowTitle}
      >
        {`${title}: ${format(value)}`}
      </Text>
      <Slider
        accessibilityLabel={title}
        accessibilityValue={{ text: format(value), min, max, now: value }}
        value={value}
        minimumValue={min}
        maximumValue={max}
        step={step}
        onValueChange={onChange}
        onSlidingComplete={onSettle}
        minimumTrackTintColor={colors.primary}
        maximumTrackTintColor={colors.divider}
        thumbTintColor={colors.primary}
        style={styles.slider}
      />
    </View>
  );
}

interface HelpSheetProps {
  visible: boolean;
  title: string;
  /** Rendered one element per line so each can be reached by swiping. */
  body: string;
  closeLabel: string;
  onClose: () => void;
}

/**
 * The API-key instructions.
 *
 * This was an Alert with the whole text in its message, which a screen reader can
 * only read as one long blob — QA asked for the steps to be separate stops. The
 * Flutter build split the same string on newlines into separate widgets; so does
 * this.
 */
function HelpSheet({ visible, title, body, closeLabel, onClose }: HelpSheetProps) {
  const lines = body.split('\n').filter((line) => line.trim().length > 0);

  return (
    <Modal visible={visible} transparent animationType="slide" onRequestClose={onClose}>
      <Pressable
        style={styles.scrim}
        accessibilityElementsHidden
        importantForAccessibility="no-hide-descendants"
        onPress={onClose}
      />
      <View accessibilityViewIsModal style={styles.helpSheet}>
        <Text accessibilityRole="header" style={styles.helpTitle}>
          {title}
        </Text>
        <ScrollView contentContainerStyle={styles.helpBody}>
          {lines.map((line, index) => (
            <Text key={index} accessible style={styles.helpLine}>
              {line.trim()}
            </Text>
          ))}
        </ScrollView>
        <Pressable
          accessibilityRole="button"
          accessibilityLabel={closeLabel}
          onPress={onClose}
          style={({ pressed }) => [styles.helpClose, pressed && styles.pressed]}
        >
          <VisualText style={styles.helpCloseText}>{closeLabel}</VisualText>
        </Pressable>
      </View>
    </Modal>
  );
}

export default function SettingsScreen({ navigation }: Props) {
  const settings = useSettings();
  const restoreDefaults = useRecipes((s) => s.restoreDefaults);
  const lang = settings.appLanguage;

  const [sheet, setSheet] = useState<Sheet>(null);
  const [helpOpen, setHelpOpen] = useState(false);
  const [voices, setVoices] = useState<Speech.Voice[]>([]);

  useLayoutEffect(() => {
    navigation.setOptions({ title: str(lang, 'settings_title') });
  }, [navigation, lang]);

  useEffect(() => {
    void availableVoices().then(setVoices);
  }, []);

  // Push every change straight into the speech layer, so the confirmation line
  // that follows is spoken with the setting the user just chose.
  const syncSpeech = () => {
    const s = useSettings.getState();
    applySpeechSettings({
      language: s.appLanguage,
      rate: s.ttsSpeed,
      pitch: s.ttsPitch,
      enabled: s.isTtsEnabled,
      mode: s.audioOutputMode,
      voice: s.ttsVoiceName,
      voiceLocale: s.ttsVoiceLocale,
    });
  };

  const languageOptions: SelectOption[] = [
    { value: 'en', label: 'English' },
    { value: 'id', label: 'Bahasa Indonesia' },
  ];

  const providerOptions: SelectOption[] = [
    { value: 'gemini', label: 'Google Gemini' },
    { value: 'groq', label: 'Groq (Ultra-Fast)' },
  ];

  const channelOptions: SelectOption[] = [
    { value: 'tts', label: str(lang, 'tts_channel_app') },
    { value: 'screen_reader', label: str(lang, 'tts_channel_sr') },
  ];

  const voiceOptions: SelectOption[] = voices
    .filter((v) => v.language?.toLowerCase().startsWith(lang))
    .map((v) => ({ value: v.identifier, label: v.name }));

  const round2 = (n: number) => Math.round(n * 100) / 100;
  const sheetProps = {
    selectedSuffix: str(lang, 'selected_suffix'),
  };

  const confirmRestore = () => {
    Alert.alert(
      str(lang, 'settings_restore_title'),
      str(lang, 'settings_restore_sub'),
      [
        { text: str(lang, 'cancel_brew_btn'), style: 'cancel' },
        {
          text: str(lang, 'settings_restore_title'),
          onPress: async () => {
            await restoreDefaults();
            notify(str(lang, 'restore_success'));
          },
        },
      ]
    );
  };

  return (
    <View style={styles.screen}>
      <ScrollView contentContainerStyle={styles.body}>
        <SettingRow title={str(lang, 'app_lang')} subtitle={str(lang, 'app_lang_desc')}>
          <Pressable
            accessibilityRole="button"
            accessibilityLabel={`${str(lang, 'app_lang_label')}. ${
              lang === 'en' ? 'English' : 'Indonesia'
            }`}
            onPress={() => setSheet('language')}
            style={({ pressed }) => [styles.valueButton, pressed && styles.pressed]}
          >
            <VisualText style={styles.valueButtonText}>
              {lang === 'en' ? 'English' : 'Indonesia'}
            </VisualText>
          </Pressable>
        </SettingRow>

        <View style={styles.divider} />

        <SettingRow title={str(lang, 'gemini_title')} subtitle={str(lang, 'gemini_desc')}>
          <Pressable
            accessibilityRole="button"
            accessibilityLabel={`${str(lang, 'gemini_title')}. ${
              settings.aiProvider === 'gemini' ? 'Gemini' : 'Groq'
            }`}
            onPress={() => setSheet('provider')}
            style={({ pressed }) => [styles.valueButton, pressed && styles.pressed]}
          >
            <VisualText style={styles.valueButtonText}>
              {settings.aiProvider === 'gemini' ? 'Gemini' : 'Groq'}
            </VisualText>
          </Pressable>
        </SettingRow>

        <View style={styles.section}>
          {settings.aiProvider === 'gemini' ? (
            <>
              <LabeledInput
                label={str(lang, 'gemini_api_key_label')}
                value={settings.geminiApiKey}
                onChangeText={(v) => void settings.setGeminiApiKey(v)}
                secret
                revealLabel={str(lang, 'show_api_key')}
                hideLabel={str(lang, 'hide_api_key')}
              />
              <Pressable
                accessibilityRole="button"
                accessibilityLabel={str(lang, 'gemini_help_title')}
                onPress={() => setHelpOpen(true)}
                style={({ pressed }) => [styles.helpButton, pressed && styles.pressed]}
              >
                <Icon name="help-outline" size={22} color={colors.primary} />
                <VisualText style={styles.helpButtonText}>{str(lang, 'gemini_help_title')}</VisualText>
              </Pressable>
            </>
          ) : (
            <>
              <LabeledInput
                label={str(lang, 'groq_api_key_label')}
                value={settings.groqApiKey}
                onChangeText={(v) => void settings.setGroqApiKey(v)}
                secret
                revealLabel={str(lang, 'show_api_key')}
                hideLabel={str(lang, 'hide_api_key')}
              />
              <View accessible style={styles.warningBox}>
                <Icon name="warning-amber" size={22} color="#FF9800" />
                <Text style={styles.warningText}>{str(lang, 'groq_network_warning')}</Text>
              </View>
            </>
          )}
        </View>

        <Text accessibilityRole="header" style={styles.sectionHeading}>
          {str(lang, 'tts_title')}
        </Text>

        <ToggleRow
          title={str(lang, 'tts_enable')}
          subtitle={str(lang, 'tts_enable_desc')}
          value={settings.isTtsEnabled}
          onValueChange={async (v) => {
            await settings.setTtsEnabled(v);
            syncSpeech();
          }}
        />

        <ToggleRow
          title={str(lang, 'audio_metronome_title')}
          subtitle={str(lang, 'audio_metronome_desc')}
          value={settings.audioMetronome}
          onValueChange={(v) => void settings.setAudioMetronome(v)}
        />

        <ToggleRow
          title={str(lang, 'visual_metronome_title')}
          subtitle={str(lang, 'visual_metronome_desc')}
          value={settings.visualMetronome}
          onValueChange={(v) => void settings.setVisualMetronome(v)}
        />

        <ToggleRow
          title={str(lang, 'haptic_metronome_title')}
          subtitle={str(lang, 'haptic_metronome_desc')}
          value={settings.hapticMetronome}
          onValueChange={(v) => void settings.setHapticMetronome(v)}
        />

        <SettingRow
          title={str(lang, 'tts_channel')}
          subtitle={str(lang, 'tts_channel_desc')}
        >
          <Pressable
            accessibilityRole="button"
            accessibilityLabel={`${str(lang, 'tts_channel')}. ${
              settings.audioOutputMode === 'tts'
                ? str(lang, 'tts_channel_app')
                : str(lang, 'tts_channel_sr')
            }`}
            onPress={() => setSheet('channel')}
            style={({ pressed }) => [styles.valueButton, pressed && styles.pressed]}
          >
            <VisualText style={styles.valueButtonText}>
              {settings.audioOutputMode === 'tts'
                ? str(lang, 'tts_channel_app')
                : str(lang, 'tts_channel_sr')}
            </VisualText>
          </Pressable>
        </SettingRow>

        <View style={styles.divider} />

        {settings.audioOutputMode === 'tts' && (
          <>
            <SliderRow
              title={str(lang, 'tts_speed')}
              value={settings.ttsSpeed}
              min={0.5}
              max={2}
              step={0.25}
              format={(v) => v.toFixed(2)}
              onChange={(v) => void settings.setTtsSpeed(round2(v))}
              onSettle={(v) => {
                syncSpeech();
                speak(str(lang, 'tts_speed_changed', [round2(v).toFixed(2)]));
              }}
            />

            <SliderRow
              title={str(lang, 'tts_pitch')}
              value={settings.ttsPitch}
              min={0.5}
              max={2}
              step={0.1}
              format={(v) => v.toFixed(1)}
              onChange={(v) => void settings.setTtsPitch(round2(v))}
              onSettle={() => {
                syncSpeech();
                speak(str(lang, 'tts_pitch_changed'));
              }}
            />

            <SettingRow title={str(lang, 'tts_voice')} subtitle={str(lang, 'tts_voice_desc')}>
              <Pressable
                accessibilityRole="button"
                accessibilityLabel={`${str(lang, 'tts_voice')}. ${
                  settings.ttsVoiceName ?? str(lang, 'default')
                }`}
                onPress={() => {
                  if (voiceOptions.length === 0) {
                    notify(str(lang, 'tts_voice_none'));
                    return;
                  }
                  setSheet('voice');
                }}
                style={({ pressed }) => [styles.valueButton, pressed && styles.pressed]}
              >
                <VisualText numberOfLines={1} style={styles.valueButtonText}>
                  {settings.ttsVoiceName ?? str(lang, 'default')}
                </VisualText>
              </Pressable>
            </SettingRow>
          </>
        )}

        <View style={styles.divider} />

        <Pressable
          accessibilityRole="button"
          accessibilityLabel={`${str(lang, 'settings_restore_title')}. ${str(
            lang,
            'settings_restore_sub'
          )}`}
          onPress={confirmRestore}
          style={({ pressed }) => [styles.row, pressed && styles.pressed]}
        >
          <View style={styles.rowText}>
            <VisualText style={[styles.rowTitle, { color: colors.red }]}>
              {str(lang, 'settings_restore_title')}
            </VisualText>
            <VisualText style={styles.rowSubtitle}>{str(lang, 'settings_restore_sub')}</VisualText>
          </View>
          <Icon name="restore" size={26} color={colors.red} />
        </Pressable>
      </ScrollView>

      <HelpSheet
        visible={helpOpen}
        title={str(lang, 'gemini_help_title')}
        body={str(lang, 'gemini_help_content')}
        closeLabel={str(lang, 'close')}
        onClose={() => setHelpOpen(false)}
      />

      <SelectSheet
        {...sheetProps}
        visible={sheet === 'language'}
        title={str(lang, 'app_lang_label')}
        options={languageOptions}
        currentValue={settings.appLanguage}
        onClose={() => setSheet(null)}
        onSelect={async (value) => {
          setSheet(null);
          await settings.setAppLanguage(value);
          syncSpeech();
        }}
      />

      <SelectSheet
        {...sheetProps}
        visible={sheet === 'provider'}
        title={str(lang, 'gemini_title')}
        options={providerOptions}
        currentValue={settings.aiProvider}
        onClose={() => setSheet(null)}
        onSelect={async (value) => {
          setSheet(null);
          await settings.setAiProvider(value === 'groq' ? 'groq' : 'gemini');
        }}
      />

      <SelectSheet
        {...sheetProps}
        visible={sheet === 'channel'}
        title={str(lang, 'tts_channel')}
        options={channelOptions}
        currentValue={settings.audioOutputMode}
        onClose={() => setSheet(null)}
        onSelect={async (value) => {
          setSheet(null);
          await settings.setAudioOutputMode(value === 'screen_reader' ? 'screen_reader' : 'tts');
          syncSpeech();
          speak(str(lang, 'tts_channel_changed'));
        }}
      />

      <SelectSheet
        {...sheetProps}
        visible={sheet === 'voice'}
        title={str(lang, 'tts_voice')}
        options={voiceOptions}
        currentValue={settings.ttsVoiceName ?? ''}
        previewLabel={str(lang, 'preview_voice')}
        onClose={() => setSheet(null)}
        onPreview={(value) => {
          previewVoice(str(lang, 'tts_voice_sample'), value);
        }}
        onSelect={async (value) => {
          setSheet(null);
          const voice = voices.find((v) => v.identifier === value);
          await settings.setTtsVoice(value, voice?.language ?? '');
          syncSpeech();
          speak(str(lang, 'tts_voice_changed'));
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
    paddingVertical: 16,
    paddingBottom: 48,
  },
  row: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
    paddingHorizontal: 16,
    paddingVertical: 14,
  },
  rowText: {
    flex: 1,
  },
  rowTitle: {
    fontSize: fontSize.subheading,
    color: colors.text,
  },
  rowSubtitle: {
    fontSize: 14,
    color: colors.textSecondary,
    marginTop: 2,
  },
  valueButton: {
    maxWidth: 140,
    backgroundColor: colors.primary,
    paddingHorizontal: 16,
    paddingVertical: 12,
    borderRadius: 4,
  },
  valueButtonText: {
    color: colors.onPrimary,
    fontSize: fontSize.body,
    fontWeight: '500',
  },
  divider: {
    height: 1,
    backgroundColor: colors.divider,
    marginVertical: 8,
  },
  section: {
    paddingHorizontal: 16,
    paddingTop: 8,
  },
  sectionHeading: {
    fontSize: fontSize.subheading,
    fontWeight: 'bold',
    color: colors.text,
    paddingHorizontal: 16,
    paddingTop: 16,
    paddingBottom: 8,
  },
  helpButton: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    paddingVertical: 12,
  },
  helpButtonText: {
    fontSize: fontSize.body,
    color: colors.primary,
    fontWeight: '500',
  },
  warningBox: {
    flexDirection: 'row',
    gap: 8,
    padding: 12,
    borderRadius: 8,
    borderWidth: 1,
    borderColor: '#FF9800',
    backgroundColor: 'rgba(255, 152, 0, 0.1)',
  },
  warningText: {
    flex: 1,
    fontSize: 13,
    color: '#E65100',
  },
  sliderBlock: {
    paddingHorizontal: 16,
    paddingVertical: 12,
  },
  slider: {
    width: '100%',
    height: 48,
  },
  scrim: {
    flex: 1,
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
  },
  helpSheet: {
    maxHeight: '80%',
    backgroundColor: colors.card,
    borderTopLeftRadius: 8,
    borderTopRightRadius: 8,
    paddingBottom: 16,
  },
  helpTitle: {
    fontSize: fontSize.heading,
    fontWeight: 'bold',
    color: colors.text,
    padding: 16,
  },
  helpBody: {
    paddingHorizontal: 16,
    paddingBottom: 16,
    gap: 12,
  },
  helpLine: {
    fontSize: fontSize.body,
    color: colors.text,
  },
  helpClose: {
    marginHorizontal: 16,
    backgroundColor: colors.primary,
    paddingVertical: 14,
    borderRadius: 4,
    alignItems: 'center',
  },
  helpCloseText: {
    color: colors.onPrimary,
    fontSize: fontSize.body,
    fontWeight: '500',
  },
  pressed: {
    opacity: 0.75,
  },
});
