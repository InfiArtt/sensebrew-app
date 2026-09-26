// Translation lookup.
//
// The bulk of the table is generated from lib/core/app_strings.dart into
// generatedStrings.ts. EXTRA_STRINGS below covers the two cases that file cannot:
// text the Flutter screens wrote inline as `lang == 'en' ? ... : ...` instead of
// putting it in the table, and labels that only the Expo build's controls need.
// Those strings are copied from the Dart verbatim wherever an original exists.
import { GENERATED_STRINGS } from './generatedStrings';

export type Lang = 'id' | 'en';

const EXTRA_STRINGS: Record<string, Record<string, string>> = {
  id: {
    // Inline in settings_screen.dart's SwitchListTiles.
    'audio_metronome_title': 'Metronom Suara',
    'audio_metronome_desc': 'Mainkan suara detik di setiap ketukan',
    'visual_metronome_title': 'Metronom Visual',
    'visual_metronome_desc': 'Layar berkedip di setiap ketukan',
    'haptic_metronome_title': 'Getaran Metronom',
    'haptic_metronome_desc': 'Perangkat bergetar di setiap ketukan',
    // Inline in settings_screen.dart's Groq branch.
    'groq_network_warning':
        'Catatan: Server Groq terkadang memblokir jaringan Wi-Fi/Seluler Indonesia (Error 403). Jika AI gagal membalas, silakan gunakan VPN atau ganti jaringan internet Anda.',
    'groq_api_key_label': 'Groq API Key',
    // Inline in settings_screen.dart's voice picker.
    'tts_voice_none': 'Tidak ada suara untuk bahasa ini',
    'tts_voice_sample': 'Ini adalah contoh dari suara ini.',
    'preview_voice': 'Pratinjau suara',
    // Inline in pour_calculator_screen.dart.
    'pour_calc_uncalibrated': 'Harap kalibrasi teko Anda terlebih dahulu di layar Utama.',
    // New: the Expo pickers announce which row is already chosen.
    'selected_suffix': 'terpilih',
    'ai_no_key_hint': 'Isi API Key di menu Pengaturan dulu ya.',
  },
  en: {
    'audio_metronome_title': 'Audio Metronome',
    'audio_metronome_desc': 'Play tick sound on every beat',
    'visual_metronome_title': 'Visual Metronome',
    'visual_metronome_desc': 'Screen flashes on every beat',
    'haptic_metronome_title': 'Haptic Metronome',
    'haptic_metronome_desc': 'Vibrate device on every beat',
    'groq_network_warning':
        'Note: Groq may block certain Wi-Fi or mobile networks (Error 403). If the AI fails to respond, please use a VPN or switch networks.',
    'groq_api_key_label': 'Groq API Key',
    'tts_voice_none': 'No voice available for this language',
    'tts_voice_sample': 'This is a sample of this voice.',
    'preview_voice': 'Preview voice',
    'pour_calc_uncalibrated': 'Please calibrate your kettle first in the Home screen.',
    'selected_suffix': 'selected',
    'ai_no_key_hint': 'Please set your API Key in Settings first.',
  },
};

function lookup(lang: string, key: string): string | undefined {
  return EXTRA_STRINGS[lang]?.[key] ?? GENERATED_STRINGS[lang]?.[key];
}

/** Look up `key` for `lang`, falling back to Indonesian and then to the key. */
export function str(lang: string, key: string, args?: (string | number)[]): string {
  let text = lookup(lang, key) ?? lookup('id', key) ?? key;

  // Parse dual-language payloads like "ID: ... || EN: ..." (produced by the AI).
  if (text.includes('ID: ') && text.includes('|| EN: ')) {
    const parts = text.split('|| EN: ');
    text = lang === 'id' ? parts[0].replace(/ID: /g, '').trim() : parts[1].trim();
  }

  if (args) {
    args.forEach((arg, i) => {
      text = text.split(`{${i}}`).join(String(arg));
    });
  }
  return text;
}
