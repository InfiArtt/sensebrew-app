// Builds the metronome click track from a single tick sample.
//
// The track used to be pre-rendered into assets/audio/click_60bpm.wav, but that
// file is 61 seconds of 16-bit PCM — 5.1 MB, and 95% of it silence, which no
// APK compression touches because aapt2 never compresses .wav. Generating it on
// the device from the 15 KB tick instead keeps the bytes identical and takes
// that 5.1 MB out of the download.
//
// This module is deliberately free of React Native imports so that
// scripts/check-brew-plan.js can run it on a desktop and assert, byte for byte,
// that every click still attacks on an exact second boundary.

/** Beats in the generated track. */
export const CLICK_TRACK_BEATS = 60;

/** |sample| at or below this counts as digital silence. */
const SILENCE_THRESHOLD = 100;

const WAV_HEADER_BYTES = 44;

export interface WavPcm {
  sampleRate: number;
  channels: number;
  bitsPerSample: number;
  /** Raw PCM payload, i.e. the contents of the `data` chunk. */
  samples: Uint8Array;
}

function ascii(bytes: Uint8Array, offset: number, length: number): string {
  let out = '';
  for (let i = 0; i < length; i++) out += String.fromCharCode(bytes[offset + i]);
  return out;
}

/**
 * Parses a RIFF/WAVE file by walking its chunks.
 *
 * The `data` chunk is located rather than assumed to start at byte 44: the tick
 * sample carries an `smpl` chunk in between. MetronomeEngine.kt in the Flutter
 * build searched for the same marker for the same reason.
 */
export function readWavPcm(bytes: Uint8Array): WavPcm {
  if (ascii(bytes, 0, 4) !== 'RIFF' || ascii(bytes, 8, 4) !== 'WAVE') {
    throw new Error('not a RIFF/WAVE file');
  }

  const view = new DataView(bytes.buffer, bytes.byteOffset, bytes.byteLength);
  let sampleRate = 0;
  let channels = 0;
  let bitsPerSample = 0;
  let samples: Uint8Array | null = null;

  let pos = 12;
  while (pos + 8 <= bytes.length) {
    const id = ascii(bytes, pos, 4);
    const size = view.getUint32(pos + 4, true);
    const body = pos + 8;

    if (id === 'fmt ') {
      channels = view.getUint16(body + 2, true);
      sampleRate = view.getUint32(body + 4, true);
      bitsPerSample = view.getUint16(body + 14, true);
    } else if (id === 'data') {
      samples = bytes.subarray(body, Math.min(body + size, bytes.length));
    }

    pos = body + size + (size % 2); // chunks are word-aligned
  }

  if (!samples) throw new Error('WAV has no data chunk');
  if (channels !== 1 || bitsPerSample !== 16) {
    throw new Error(`expected mono 16-bit PCM, got ${channels}ch/${bitsPerSample}-bit`);
  }

  return { sampleRate, channels, bitsPerSample, samples };
}

/** Index of the first audible sample, in samples (not bytes). */
export function findAttack(samples: Uint8Array): number {
  const view = new DataView(samples.buffer, samples.byteOffset, samples.byteLength);
  for (let i = 0; i + 1 < samples.length; i += 2) {
    if (Math.abs(view.getInt16(i, true)) > SILENCE_THRESHOLD) return i / 2;
  }
  return 0;
}

function writeHeader(target: Uint8Array, sampleRate: number, dataBytes: number): void {
  const view = new DataView(target.buffer, target.byteOffset, target.byteLength);
  const put = (offset: number, text: string) => {
    for (let i = 0; i < text.length; i++) target[offset + i] = text.charCodeAt(i);
  };

  put(0, 'RIFF');
  view.setUint32(4, 36 + dataBytes, true);
  put(8, 'WAVE');
  put(12, 'fmt ');
  view.setUint32(16, 16, true); // fmt chunk size
  view.setUint16(20, 1, true); // PCM
  view.setUint16(22, 1, true); // mono
  view.setUint32(24, sampleRate, true);
  view.setUint32(28, sampleRate * 2, true); // byte rate
  view.setUint16(32, 2, true); // block align
  view.setUint16(34, 16, true); // bits per sample
  put(36, 'data');
  view.setUint32(40, dataBytes, true);
}

export interface ClickTrackResult {
  wav: Uint8Array;
  sampleRate: number;
  /** Samples of lead-in silence trimmed from the tick, for reporting. */
  trimmedSamples: number;
}

/**
 * Renders `beats` clicks, one per second, preceded by one second of silence.
 *
 * The leading silence puts beat 1 at t=1.000s, matching Dart's Timer.periodic,
 * which fires after the first interval rather than at zero.
 *
 * The tick's own lead-in silence is trimmed so its attack lands exactly on the
 * beat. assets/audio/tick.wav carries 60.3 ms of it, which in the Flutter build
 * made every click sound that far behind the accessibility announcement it was
 * supposed to accompany.
 */
export function buildClickTrack(tickWav: Uint8Array, beats = CLICK_TRACK_BEATS): ClickTrackResult {
  const { sampleRate, samples } = readWavPcm(tickWav);

  const attack = findAttack(samples);
  const tick = samples.subarray(attack * 2);

  const periodBytes = sampleRate * 2; // one second, 16-bit mono
  const tickBytes = Math.min(tick.length, periodBytes);
  const dataBytes = periodBytes * (beats + 1); // +1 for the leading silence

  const wav = new Uint8Array(WAV_HEADER_BYTES + dataBytes);
  writeHeader(wav, sampleRate, dataBytes);

  for (let beat = 0; beat < beats; beat++) {
    // Beat N starts at second N, hence the +1 period offset.
    const at = WAV_HEADER_BYTES + periodBytes * (beat + 1);
    wav.set(tick.subarray(0, tickBytes), at);
  }

  return { wav, sampleRate, trimmedSamples: attack };
}

/**
 * Sample offset of beat `beat`'s attack within a generated track.
 * Used by the checks to prove the onsets land on exact second boundaries.
 */
export function expectedAttackSample(beat: number, sampleRate: number): number {
  return beat * sampleRate;
}
