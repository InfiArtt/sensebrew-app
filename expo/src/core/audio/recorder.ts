// Voice-note recording for the AI chat, replacing the `record` +
// `path_provider` pair used in lib/screens/ai_chat_screen.dart.
//
// The recording is sent two different ways depending on the provider: Gemini
// takes it inline as base64, Groq's Whisper endpoint takes a multipart upload
// that React Native builds from the file's uri. So both forms are returned.
import { AudioModule, setAudioModeAsync } from 'expo-audio';
import { File } from 'expo-file-system';

export interface VoiceNote {
  uri: string;
  base64: string;
}

/** Asks for the microphone, returning whether recording may proceed. */
export async function ensureMicPermission(): Promise<boolean> {
  const current = await AudioModule.getRecordingPermissionsAsync();
  if (current.granted) return true;
  const requested = await AudioModule.requestRecordingPermissionsAsync();
  return requested.granted;
}

/**
 * Puts the audio session into recording mode.
 *
 * The metronome configures the session for playback at startup, and Android
 * will not hand over the microphone until recording is explicitly allowed.
 */
export async function enableRecordingMode(): Promise<void> {
  await setAudioModeAsync({
    allowsRecording: true,
    playsInSilentMode: true,
    interruptionMode: 'mixWithOthers',
    shouldPlayInBackground: false,
  });
}

/** Restores the playback-only session the metronome expects. */
export async function disableRecordingMode(): Promise<void> {
  await setAudioModeAsync({
    allowsRecording: false,
    playsInSilentMode: true,
    interruptionMode: 'mixWithOthers',
    shouldPlayInBackground: false,
  });
}

/** Reads a finished recording, then deletes it — it is never needed twice. */
export async function readVoiceNote(uri: string): Promise<VoiceNote> {
  const file = new File(uri);
  const base64 = await file.base64();
  return { uri, base64 };
}

/** Best-effort cleanup; a leftover temp file is not worth failing a send over. */
export function discardVoiceNote(uri: string): void {
  try {
    new File(uri).delete();
  } catch {
    // The OS clears its own cache directory eventually.
  }
}
