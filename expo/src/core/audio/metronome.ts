// The metronome, replacing android/.../MetronomeEngine.kt.
//
// The Flutter build streams PCM from a Kotlin AudioTrack so ticks land on exact
// frame boundaries, then uses AudioTimestamp to fire each tick event at the
// moment that frame reaches the speaker. Expo Go cannot load a custom native
// module, so the guarantee moves into a file instead: a click track whose attacks
// sit on exact one-second frame offsets, after one second of leading silence
// (beat 1 at t=1.000s, matching Dart's Timer.periodic, which fires after the
// first interval rather than at zero).
//
// That file is rendered on the device from the 15 KB tick sample the first time
// the app runs and then cached — see clickTrack.ts for why it is not shipped
// pre-rendered.
//
// JavaScript therefore never decides when a click sounds — the native player
// does, from the file. JS only needs to know *which* beat is currently sounding,
// and it reads that from the player's own clock rather than from a JS timer, so
// nothing accumulates drift. Each beat event is scheduled one beat ahead against
// that clock and re-derived on every beat, so a late or early timer corrects
// itself instead of compounding.
import { Asset } from 'expo-asset';
import { AudioPlayer, createAudioPlayer, setAudioModeAsync } from 'expo-audio';
import { File, Paths } from 'expo-file-system';
import * as Haptics from 'expo-haptics';

import { CLICK_TRACK_BEATS, buildClickTrack } from './clickTrack';

const TICK_SAMPLE = require('../../../assets/audio/tick.wav');
const BELL = require('../../../assets/audio/bell.wav');

/** Cache filename. The beat count is in the name so a change invalidates it. */
const CLICK_TRACK_FILE = `click_${CLICK_TRACK_BEATS}beats_v1.wav`;

/** Beats contained in the click track; see clickTrack.ts. */
export const TRACK_BEATS = CLICK_TRACK_BEATS;

let clickPlayer: AudioPlayer | null = null;
let bellPlayer: AudioPlayer | null = null;

let beatTimer: ReturnType<typeof setTimeout> | null = null;
let lastEmittedBeat = 0;
let running = false;

interface StartOptions {
  /** Fired once per beat, with a 1-based beat number. */
  onBeat?: (beat: number) => void;
  /** Whether the click itself should be audible (Settings > audio metronome). */
  audible: boolean;
  /** Whether to buzz on each beat (Settings > haptic metronome). */
  haptics: boolean;
  /**
   * Shifts beat events relative to the audible click. Haptics, the flashing
   * background and spoken cues all ride on these events, so this is the one
   * knob for "the voice races the beat": positive values push them later.
   */
  offsetMs: number;
}

let options: StartOptions = { audible: true, haptics: true, offsetMs: 0 };

/**
 * Renders the click track into the cache directory if it is not there already,
 * and returns its uri.
 *
 * Only the first launch pays for this. The file is deterministic, so a cached
 * copy of the right size is as good as a fresh one.
 */
async function ensureClickTrack(): Promise<string> {
  const file = new File(Paths.cache, CLICK_TRACK_FILE);
  if (file.exists && file.size > 0) return file.uri;

  const asset = Asset.fromModule(TICK_SAMPLE);
  await asset.downloadAsync();
  if (!asset.localUri) throw new Error('tick sample has no local uri');

  const tickWav = await new File(asset.localUri).bytes();
  const { wav } = buildClickTrack(tickWav);

  // A half-written file would play as a truncated track, so build under a
  // temporary name and only then move it into place.
  const temp = new File(Paths.cache, `${CLICK_TRACK_FILE}.partial`);
  if (temp.exists) temp.delete();
  temp.create();
  temp.write(wav);
  temp.move(file);

  return file.uri;
}

/**
 * Loads the players and configures the audio session. Call once at startup:
 * creating a player is the slow part, and a pour phase cannot wait for it.
 */
export async function prepareAudio(): Promise<void> {
  if (clickPlayer) return;

  await setAudioModeAsync({
    playsInSilentMode: true,
    // The click and the spoken guide must be able to sound together; ducking or
    // interrupting would silence one of them mid-pour.
    interruptionMode: 'mixWithOthers',
    shouldPlayInBackground: false,
  });

  const clickTrackUri = await ensureClickTrack();
  clickPlayer = createAudioPlayer(clickTrackUri);
  bellPlayer = createAudioPlayer(BELL);
}

export function isRunning(): boolean {
  return running;
}

export function currentBeat(): number {
  return lastEmittedBeat;
}

/**
 * Schedules the next beat event against the player's clock.
 *
 * Reading currentTime each time means the schedule is anchored to the audio
 * output rather than to elapsed JS time, so a timer that fires 15 ms late does
 * not push every later beat 15 ms late too.
 */
function scheduleNextBeat(): void {
  const player = clickPlayer;
  if (!player || !running) return;

  const now = player.currentTime;
  const nextBeat = Math.max(lastEmittedBeat + 1, Math.floor(now) + 1);
  const waitMs = (nextBeat - now) * 1000 + options.offsetMs;

  beatTimer = setTimeout(() => {
    if (!running) return;

    lastEmittedBeat = nextBeat;
    if (options.haptics) {
      // Fire and forget: awaiting the vibration would delay the next schedule.
      void Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Heavy);
    }
    options.onBeat?.(nextBeat);

    if (nextBeat < TRACK_BEATS) scheduleNextBeat();
  }, Math.max(0, waitMs));
}

/** Starts the click track from beat 0. Safe to call while already running. */
export function startMetronome(opts: StartOptions): void {
  const player = clickPlayer;
  if (!player) {
    // prepareAudio() has not finished. Without the track there is no clock to
    // hang beats off, so stay silent rather than fall back to a drifting timer.
    return;
  }

  stopMetronome();

  options = opts;
  running = true;
  lastEmittedBeat = 0;

  player.volume = opts.audible ? 1 : 0;
  // seekTo is async, but beats are derived from the clock rather than from when
  // playback actually begins, so beat 1 still lands one second into the track.
  void player.seekTo(0);
  player.play();

  scheduleNextBeat();
}

export function stopMetronome(): void {
  running = false;
  if (beatTimer) {
    clearTimeout(beatTimer);
    beatTimer = null;
  }
  clickPlayer?.pause();
}

/** The end-of-brew chime. */
export function playBell(): void {
  if (!bellPlayer) return;
  void bellPlayer.seekTo(0);
  bellPlayer.play();
}

/** Releases the players. Only for a full teardown. */
export function releaseAudio(): void {
  stopMetronome();
  clickPlayer?.remove();
  bellPlayer?.remove();
  clickPlayer = null;
  bellPlayer = null;
}
