// Spoken guidance, ported from the TTS half of lib/core/timer_state.dart.
//
// Two output paths, as in the Flutter build: expo-speech (the app's own voice)
// or the screen reader, so a TalkBack user hears one voice instead of two
// talking over each other.
import { AccessibilityInfo } from 'react-native';
import * as Speech from 'expo-speech';

export type AudioOutputMode = 'tts' | 'screen_reader';

interface SpeechSettings {
  language: string; // 'id' or 'en'
  rate: number;
  pitch: number;
  enabled: boolean;
  mode: AudioOutputMode;
  voice: string | null;
  voiceLocale: string | null;
}

let settings: SpeechSettings = {
  language: 'id',
  rate: 1.25,
  pitch: 1.0,
  enabled: true,
  mode: 'tts',
  voice: null,
  voiceLocale: null,
};

function localeFor(language: string): string {
  return language === 'en' ? 'en-US' : 'id-ID';
}

/** The voice only applies when it belongs to the active language, as in Dart. */
function voiceFor(current: SpeechSettings): string | undefined {
  if (!current.voice || !current.voiceLocale) return undefined;
  const locale = current.voiceLocale.toLowerCase();
  const matches =
    (current.language === 'id' && locale.includes('id')) ||
    (current.language === 'en' && locale.includes('en'));
  return matches ? current.voice : undefined;
}

export function applySpeechSettings(next: SpeechSettings): void {
  settings = next;
}

/** Speaks, or announces via the screen reader, depending on the output mode. */
export function speak(text: string): void {
  if (!settings.enabled) return;

  if (settings.mode === 'screen_reader') {
    AccessibilityInfo.announceForAccessibility(text);
    return;
  }

  Speech.speak(text, {
    language: localeFor(settings.language),
    rate: settings.rate,
    pitch: settings.pitch,
    voice: voiceFor(settings),
  });
}

/**
 * Speaks and resolves when the voice has finished.
 *
 * The brew clock starts only after the "prepare to pour" line, so that the
 * countdown is not already running while the user is still being told what to
 * do. Screen-reader announcements report no completion, so they resolve at once
 * — the same behaviour as SemanticsService.announce in the Flutter build.
 */
export function speakAndWait(text: string): Promise<void> {
  if (!settings.enabled) return Promise.resolve();

  if (settings.mode === 'screen_reader') {
    AccessibilityInfo.announceForAccessibility(text);
    return Promise.resolve();
  }

  return new Promise((resolve) => {
    let settled = false;
    const finish = () => {
      if (settled) return;
      settled = true;
      resolve();
    };

    Speech.speak(text, {
      language: localeFor(settings.language),
      rate: settings.rate,
      pitch: settings.pitch,
      voice: voiceFor(settings),
      onDone: finish,
      onStopped: finish,
      onError: finish,
    });
  });
}

/** Plays a sample line, ignoring the enabled flag, for the settings screen. */
export function previewVoice(text: string, voice?: string): void {
  if (settings.mode === 'screen_reader') return;
  Speech.speak(text, {
    language: localeFor(settings.language),
    rate: settings.rate,
    pitch: settings.pitch,
    voice: voice ?? voiceFor(settings),
  });
}

export function stopSpeaking(): void {
  void Speech.stop();
}

export async function availableVoices(): Promise<Speech.Voice[]> {
  try {
    return await Speech.getAvailableVoicesAsync();
  } catch {
    return [];
  }
}
