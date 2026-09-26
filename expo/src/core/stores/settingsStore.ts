// Ported from lib/core/settings_state.dart (Provider/ChangeNotifier -> Zustand).
import { getLocales } from 'expo-localization';
import { create } from 'zustand';

import * as storage from '../storage';

export type AudioOutputMode = 'tts' | 'screen_reader';
export type AiProvider = 'gemini' | 'groq';

interface SettingsState {
  hydrated: boolean;

  geminiApiKey: string;
  groqApiKey: string;
  aiProvider: AiProvider;
  appLanguage: string; // 'id' or 'en'
  ttsSpeed: number;
  ttsPitch: number;
  ttsVolume: number;
  ttsVoiceName: string | null;
  ttsVoiceLocale: string | null;
  isTtsEnabled: boolean;
  audioOutputMode: AudioOutputMode;
  visualMetronome: boolean;
  hapticMetronome: boolean;
  audioMetronome: boolean;

  /**
   * Milliseconds to delay a spoken cue relative to the metronome beat it
   * belongs to. Positive values push the voice later. See
   * src/core/audio/metronome.ts for why this knob exists.
   */
  announcementOffsetMs: number;

  hydrate: () => Promise<void>;
  setGeminiApiKey: (key: string) => Promise<void>;
  setGroqApiKey: (key: string) => Promise<void>;
  setAiProvider: (provider: AiProvider) => Promise<void>;
  setAppLanguage: (lang: string) => Promise<void>;
  setTtsSpeed: (speed: number) => Promise<void>;
  setTtsPitch: (pitch: number) => Promise<void>;
  setTtsVolume: (volume: number) => Promise<void>;
  setTtsVoice: (name: string, locale: string) => Promise<void>;
  setTtsEnabled: (enabled: boolean) => Promise<void>;
  setAudioOutputMode: (mode: AudioOutputMode) => Promise<void>;
  setVisualMetronome: (enabled: boolean) => Promise<void>;
  setHapticMetronome: (enabled: boolean) => Promise<void>;
  setAudioMetronome: (enabled: boolean) => Promise<void>;
  setAnnouncementOffsetMs: (ms: number) => Promise<void>;
}

/** 'en' when the device is English, otherwise Indonesian, as in Dart. */
function detectLanguage(): string {
  const tag = getLocales()[0]?.languageTag ?? 'id-ID';
  return tag.toLowerCase().startsWith('en') ? 'en' : 'id';
}

export const useSettings = create<SettingsState>((set, get) => ({
  hydrated: false,

  geminiApiKey: '',
  groqApiKey: '',
  aiProvider: 'gemini',
  appLanguage: 'id',
  ttsSpeed: 1.25,
  ttsPitch: 1.0,
  ttsVolume: 1.0,
  ttsVoiceName: null,
  ttsVoiceLocale: null,
  isTtsEnabled: true,
  audioOutputMode: 'tts',
  visualMetronome: true,
  hapticMetronome: true,
  audioMetronome: true,
  announcementOffsetMs: 0,

  hydrate: async () => {
    if (get().hydrated) return;

    const [
      geminiApiKey,
      groqApiKey,
      aiProvider,
      savedLanguage,
      ttsSpeed,
      ttsPitch,
      // Dart wrote this under the key 'ttsVolume' but only ever read 'tts_volume',
      // so the slider silently reset on every launch. Read and write one key.
      ttsVolume,
      ttsVoiceName,
      ttsVoiceLocale,
      isTtsEnabled,
      audioOutputMode,
      visualMetronome,
      hapticMetronome,
      audioMetronome,
      announcementOffsetMs,
    ] = await Promise.all([
      storage.getString('gemini_api_key', ''),
      storage.getString('groq_api_key', ''),
      storage.getString('ai_provider', 'gemini'),
      storage.getStringOrNull('app_language'),
      storage.getNumber('tts_speed', 1.25),
      storage.getNumber('tts_pitch', 1.0),
      storage.getNumber('tts_volume', 1.0),
      storage.getStringOrNull('tts_voice_name'),
      storage.getStringOrNull('tts_voice_locale'),
      storage.getBool('is_tts_enabled', true),
      storage.getString('audio_output_mode', 'tts'),
      storage.getBool('visual_metronome', true),
      storage.getBool('haptic_metronome', true),
      storage.getBool('audio_metronome', true),
      storage.getNumber('announcement_offset_ms', 0),
    ]);

    set({
      hydrated: true,
      geminiApiKey,
      groqApiKey,
      aiProvider: aiProvider === 'groq' ? 'groq' : 'gemini',
      appLanguage: savedLanguage ?? detectLanguage(),
      ttsSpeed,
      ttsPitch,
      ttsVolume,
      ttsVoiceName,
      ttsVoiceLocale,
      isTtsEnabled,
      audioOutputMode: audioOutputMode === 'screen_reader' ? 'screen_reader' : 'tts',
      visualMetronome,
      hapticMetronome,
      audioMetronome,
      announcementOffsetMs,
    });
  },

  setGeminiApiKey: async (key) => {
    set({ geminiApiKey: key });
    await storage.setString('gemini_api_key', key);
  },

  setGroqApiKey: async (key) => {
    set({ groqApiKey: key });
    await storage.setString('groq_api_key', key);
  },

  setAiProvider: async (provider) => {
    set({ aiProvider: provider });
    await storage.setString('ai_provider', provider);
  },

  setAppLanguage: async (lang) => {
    // Switching language drops the saved voice, which belongs to the old locale.
    set({ appLanguage: lang, ttsVoiceName: null, ttsVoiceLocale: null });
    await storage.setString('app_language', lang);
    await storage.remove('tts_voice_name');
    await storage.remove('tts_voice_locale');
  },

  setTtsSpeed: async (speed) => {
    set({ ttsSpeed: speed });
    await storage.setNumber('tts_speed', speed);
  },

  setTtsPitch: async (pitch) => {
    set({ ttsPitch: pitch });
    await storage.setNumber('tts_pitch', pitch);
  },

  setTtsVolume: async (volume) => {
    set({ ttsVolume: volume });
    await storage.setNumber('tts_volume', volume);
  },

  setTtsVoice: async (name, locale) => {
    set({ ttsVoiceName: name, ttsVoiceLocale: locale });
    await storage.setString('tts_voice_name', name);
    await storage.setString('tts_voice_locale', locale);
  },

  setTtsEnabled: async (enabled) => {
    set({ isTtsEnabled: enabled });
    await storage.setBool('is_tts_enabled', enabled);
  },

  setAudioOutputMode: async (mode) => {
    set({ audioOutputMode: mode });
    await storage.setString('audio_output_mode', mode);
  },

  setVisualMetronome: async (enabled) => {
    set({ visualMetronome: enabled });
    await storage.setBool('visual_metronome', enabled);
  },

  setHapticMetronome: async (enabled) => {
    set({ hapticMetronome: enabled });
    await storage.setBool('haptic_metronome', enabled);
  },

  setAudioMetronome: async (enabled) => {
    set({ audioMetronome: enabled });
    await storage.setBool('audio_metronome', enabled);
  },

  setAnnouncementOffsetMs: async (ms) => {
    set({ announcementOffsetMs: ms });
    await storage.setNumber('announcement_offset_ms', ms);
  },
}));
