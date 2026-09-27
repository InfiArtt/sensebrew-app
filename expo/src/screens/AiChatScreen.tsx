// Ported from lib/screens/ai_chat_screen.dart.
//
// The user describes a brew in text or speech and the assistant returns a whole
// recipe, previewed in the transcript and applied to the editor on request.
//
// Voice notes go through Whisper rather than on-device dictation, which is why
// this screen still works in Expo Go: `@react-native-voice/voice` would need a
// custom native build, but recording a file and uploading it does not.
import Icon from '../components/Icon';
import TextField from '../components/TextField';
import VisualText from '../components/VisualText';
import type { NativeStackScreenProps } from '@react-navigation/native-stack';
import { RecordingPresets, useAudioRecorder } from 'expo-audio';
import { useLayoutEffect, useRef, useState } from 'react';
import {
  AccessibilityInfo,
  ActivityIndicator,
  Pressable,
  ScrollView,
  StyleSheet,
  Text,
  View,
} from 'react-native';

import { str } from '../core/appStrings';
import { generateRecipe } from '../core/aiService';
import {
  disableRecordingMode,
  discardVoiceNote,
  enableRecordingMode,
  ensureMicPermission,
  readVoiceNote,
} from '../core/audio/recorder';
import type { Recipe } from '../core/recipe';
import { useAiDraft } from '../core/stores/aiDraftStore';
import { useSettings } from '../core/stores/settingsStore';
import type { RootStackParamList } from '../navigation';
import { colors, fontSize } from '../theme';

type Props = NativeStackScreenProps<RootStackParamList, 'AiChat'>;

interface Message {
  role: 'user' | 'ai';
  text: string;
  /** Marks the bubble that carries a recipe the user can apply. */
  isDraft?: boolean;
}

export default function AiChatScreen({ navigation, route }: Props) {
  const { initialRecipe } = route.params;
  const settings = useSettings();
  const putDraft = useAiDraft((s) => s.put);
  const lang = settings.appLanguage;

  const recorder = useAudioRecorder(RecordingPresets.HIGH_QUALITY);

  const [messages, setMessages] = useState<Message[]>(() => [
    {
      role: 'ai',
      text: initialRecipe
        ? str(lang, 'ai_greet_edit', [str(lang, initialRecipe.name)])
        : str(lang, 'ai_greet_new'),
    },
  ]);
  const [input, setInput] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const draftRef = useRef<Recipe | null>(initialRecipe ?? null);
  const scrollRef = useRef<ScrollView>(null);

  useLayoutEffect(() => {
    navigation.setOptions({ title: str(lang, 'ai_chat_title') });
  }, [navigation, lang]);

  const append = (message: Message) => {
    setMessages((current) => [...current, message]);
    // The transcript is the only record of what the assistant said, so keep the
    // newest bubble in view and announce it for anyone not watching the screen.
    requestAnimationFrame(() => scrollRef.current?.scrollToEnd({ animated: true }));
    if (message.role === 'ai') AccessibilityInfo.announceForAccessibility(message.text);
  };

  /** Builds the "Preview" block the Flutter build appends under the reply. */
  const buildPreview = (recipe: Recipe, chatMessage: string, previewLang: string): string => {
    const extra =
      recipe.extraIngredients.length === 0 ? '-' : str(previewLang, recipe.extraIngredients);
    const phasesList = recipe.phases
      .map((p) => `\n   - ${p.startTimeSeconds}s: ${str(previewLang, p.instructionText)}`)
      .join('');

    return (
      `${chatMessage}\n\n📋 Preview:\n` +
      `• ${str(previewLang, 'ai_coffee')}: ${recipe.coffeeGrams}g\n` +
      `• ${str(previewLang, 'ai_water')}: ${recipe.totalWaterMl}ml\n` +
      `• ${str(previewLang, 'ai_time')}: ${recipe.totalDurationSeconds}s\n` +
      `• ${str(previewLang, 'brew_grind')}: ${recipe.targetGrindSizeMicrons} µm\n` +
      `• ${str(previewLang, 'brew_extra')}: ${extra}\n` +
      `• ${str(previewLang, 'phases_title')}:${phasesList}`
    );
  };

  const processRequest = async (params: {
    prompt?: string;
    audioBase64?: string;
    audioUri?: string;
  }) => {
    setIsLoading(true);
    try {
      // Each provider authenticates with its own key; sending Gemini's key to
      // Groq is a guaranteed 401.
      const apiKey =
        settings.aiProvider === 'groq' ? settings.groqApiKey : settings.geminiApiKey;

      const response = await generateRecipe({
        provider: settings.aiProvider,
        apiKey,
        lang,
        prompt: params.prompt ?? null,
        audioBase64: params.audioBase64 ?? null,
        audioUri: params.audioUri ?? null,
        currentRecipe: draftRef.current,
      });

      draftRef.current = response.recipe;
      append({
        role: 'ai',
        text: buildPreview(response.recipe, response.chatMessage, response.detectedLang),
        isDraft: true,
      });
    } catch (e) {
      append({ role: 'ai', text: `${str(lang, 'ai_error_general')}\n${String(e)}` });
    } finally {
      setIsLoading(false);
    }
  };

  const sendText = async () => {
    const text = input.trim();
    if (text.length === 0) return;
    setInput('');
    append({ role: 'user', text });
    await processRequest({ prompt: text });
  };

  const startRecording = async () => {
    const granted = await ensureMicPermission();
    if (!granted) {
      append({ role: 'ai', text: str(lang, 'ai_error_general') });
      return;
    }

    await enableRecordingMode();
    await recorder.prepareToRecordAsync();
    recorder.record();
    setIsRecording(true);
  };

  const stopRecording = async () => {
    await recorder.stop();
    setIsRecording(false);
    await disableRecordingMode();

    const uri = recorder.uri;
    if (!uri) return;

    append({ role: 'user', text: str(lang, 'ai_voice_note') });

    const note = await readVoiceNote(uri);
    await processRequest({ audioBase64: note.base64, audioUri: note.uri });
    discardVoiceNote(uri);
  };

  const applyDraft = () => {
    if (!draftRef.current) return;
    putDraft(draftRef.current);
    navigation.goBack();
  };

  return (
    <View style={styles.screen}>
      <ScrollView ref={scrollRef} contentContainerStyle={styles.transcript}>
        {messages.map((message, index) => (
          <View
            key={index}
            style={[
              styles.bubbleRow,
              message.role === 'user' ? styles.bubbleRowUser : styles.bubbleRowAi,
            ]}
          >
            <View
              style={[
                styles.bubble,
                message.role === 'user' ? styles.bubbleUser : styles.bubbleAi,
              ]}
            >
              <Text accessible style={styles.bubbleText}>
                {message.text}
              </Text>

              {message.isDraft && (
                <Pressable
                  accessibilityRole="button"
                  accessibilityLabel={str(lang, 'ai_apply_btn')}
                  onPress={applyDraft}
                  style={({ pressed }) => [styles.applyButton, pressed && styles.pressed]}
                >
                  <VisualText style={styles.applyButtonText}>{str(lang, 'ai_apply_btn')}</VisualText>
                </Pressable>
              )}
            </View>
          </View>
        ))}

        {isLoading && (
          <View
            accessible
            accessibilityLabel={str(lang, 'ai_generating')}
            accessibilityLiveRegion="polite"
            style={styles.loading}
          >
            <ActivityIndicator size="large" color={colors.primary} />
            <VisualText style={styles.loadingText}>{str(lang, 'ai_generating')}</VisualText>
          </View>
        )}
      </ScrollView>

      <View style={styles.composer}>
        <TextField
          // Named by its hint alone; see components/TextField.tsx.
          hint={str(lang, 'ai_hint')}
          value={input}
          onChangeText={setInput}
          returnKey="send"
          onSubmitEditing={() => void sendText()}
          editable={!isLoading}
          style={styles.composerInput}
        />

        <Pressable
          accessibilityRole="button"
          accessibilityLabel={str(lang, 'ai_send_label')}
          accessibilityState={{ disabled: isLoading }}
          disabled={isLoading}
          onPress={() => void sendText()}
          style={({ pressed }) => [
            styles.sendButton,
            isLoading && styles.disabled,
            pressed && styles.pressed,
          ]}
        >
          <Icon name="send" size={26} color={colors.blue} />
        </Pressable>

        <Pressable
          accessibilityRole="button"
          accessibilityLabel={str(
            lang,
            isRecording ? 'ai_record_stop_label' : 'ai_record_start_label'
          )}
          accessibilityState={{ disabled: isLoading }}
          disabled={isLoading}
          onPress={() => void (isRecording ? stopRecording() : startRecording())}
          style={({ pressed }) => [
            styles.micButton,
            { backgroundColor: isRecording ? colors.red : '#9C27B0' },
            isLoading && styles.disabled,
            pressed && styles.pressed,
          ]}
        >
          <Icon
            name={isRecording ? 'stop' : 'mic'}
            size={26}
            color={colors.onPrimary}
          />
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
  transcript: {
    padding: 16,
  },
  bubbleRow: {
    flexDirection: 'row',
    marginBottom: 12,
  },
  bubbleRowUser: {
    justifyContent: 'flex-end',
  },
  bubbleRowAi: {
    justifyContent: 'flex-start',
  },
  bubble: {
    maxWidth: '88%',
    padding: 12,
    borderRadius: 12,
  },
  bubbleUser: {
    backgroundColor: '#BBDEFB', // blue.100
  },
  bubbleAi: {
    backgroundColor: colors.purple50,
  },
  bubbleText: {
    fontSize: fontSize.body,
    color: colors.text,
  },
  applyButton: {
    marginTop: 12,
    backgroundColor: colors.primary,
    paddingVertical: 14,
    paddingHorizontal: 16,
    borderRadius: 4,
    alignItems: 'center',
  },
  applyButtonText: {
    color: colors.onPrimary,
    fontSize: fontSize.body,
    fontWeight: '500',
  },
  loading: {
    alignItems: 'center',
    gap: 8,
    paddingVertical: 16,
  },
  loadingText: {
    fontSize: fontSize.body,
    color: colors.textSecondary,
  },
  composer: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
    paddingHorizontal: 8,
    paddingVertical: 8,
    backgroundColor: colors.card,
    borderTopWidth: 1,
    borderTopColor: colors.divider,
  },
  composerInput: {
    flex: 1,
    backgroundColor: colors.background,
    borderWidth: 1,
    borderColor: colors.divider,
    borderRadius: 4,
  },
  sendButton: {
    width: 52,
    height: 52,
    alignItems: 'center',
    justifyContent: 'center',
  },
  micButton: {
    width: 52,
    height: 52,
    alignItems: 'center',
    justifyContent: 'center',
    borderRadius: 4,
  },
  disabled: {
    opacity: 0.4,
  },
  pressed: {
    opacity: 0.75,
  },
});
