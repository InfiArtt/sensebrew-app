// Ported from lib/core/ai_service.dart.
//
// The assistant returns a whole recipe as JSON, which the app renders straight
// into its editor, so the prompt below is load-bearing: it is copied verbatim
// from the Dart build rather than reworded, because its exact wording is what
// makes the model emit bilingual fields and legal phase actions.
import { str } from './appStrings';
import {
  PHASE_ACTIONS,
  PhaseAction,
  Recipe,
  RecipePhase,
  makeRecipe,
} from './recipe';

export interface AiResponse {
  recipe: Recipe;
  chatMessage: string;
  detectedLang: string;
}

export type AiProvider = 'gemini' | 'groq';

const GROQ_TRANSCRIBE_URL = 'https://api.groq.com/openai/v1/audio/transcriptions';
const GROQ_CHAT_URL = 'https://api.groq.com/openai/v1/chat/completions';
const GROQ_CHAT_MODEL = 'openai/gpt-oss-120b';
const GROQ_WHISPER_MODEL = 'whisper-large-v3';
const GEMINI_MODEL = 'gemini-3.6-flash';

/**
 * Normalises a field the model may return either as a plain string or as an
 * {id, en} object into the app's "ID: ... || EN: ..." payload, which `str()`
 * splits back apart at display time.
 */
export function parseI18n(field: unknown): string {
  if (field === null || field === undefined) return '';

  if (typeof field === 'string') {
    // Already bilingual: leave it alone.
    if (field.includes('ID: ') && field.includes('|| EN: ')) return field;
    // The model ignored the object instruction; use the one string for both.
    const trimmed = field.trim();
    if (trimmed.length > 0) return `ID: ${trimmed} || EN: ${trimmed}`;
    return field;
  }

  if (typeof field === 'object') {
    const map = field as Record<string, unknown>;
    const idStr = map.id === undefined || map.id === null ? '' : String(map.id);
    const enStr = map.en === undefined || map.en === null ? '' : String(map.en);
    if (idStr === '' && enStr === '') return '';
    return `ID: ${idStr} || EN: ${enStr}`;
  }

  return String(field);
}

function buildSystemInstruction(
  lang: string,
  currentRecipe: Recipe | null | undefined
): string {
  let contextInfo: string;

  if (currentRecipe) {
    const phases = currentRecipe.phases
      .map((p) => `At ${p.startTimeSeconds}s: ${p.action} ${p.pourAmountMl}ml`)
      .join(', ');
    contextInfo =
      `\nThe user is currently editing a recipe: '${str(lang, currentRecipe.name)}'.` +
      `\nCurrent Method: ${currentRecipe.method}` +
      `\nCurrent Bean Type: ${currentRecipe.beanType}` +
      `\nCurrent Grind Size: ${currentRecipe.targetGrindSizeMicrons} microns.` +
      `\nCurrent Extra Ingredients: ${str(lang, currentRecipe.extraIngredients)}` +
      `\nCurrent Description: ${str(lang, currentRecipe.description)}` +
      `\nCurrent state: ${currentRecipe.coffeeGrams}g coffee, ${currentRecipe.totalWaterMl}ml water.` +
      `\nPhases: ${phases}` +
      `\nPlease modify this recipe based on the user's request. Keep everything else intact unless requested to change.`;
  } else {
    contextInfo = '\nPlease create a new pour-over coffee recipe based on the user\'s request.';
  }

  const appLangLabel = lang === 'en' ? 'English' : 'Indonesian';

  return `
You are a friendly, expert barista AI. ${contextInfo}
The app is currently set to ${appLangLabel}.
  1. "chatMessage": A friendly, conversational response explaining what you just did. You MUST respond in the SAME LANGUAGE the user used in their message. If the user writes in Indonesian, reply in Indonesian. If the user writes in English, reply in English. IMPORTANT: Use a very casual, warm, and enthusiastic tone, like a friendly barista talking to a friend (e.g., use words like "Siap!", "Oke deh", "Wah boleh banget!"). Keep it brief.
  2. "detectedLang": Either "id" or "en", representing the language you used in "chatMessage".
  3. "recipe": The actual modified or new recipe data.

  RULES for the recipe data:
  - ABSOLUTE RULE — NO EXCEPTIONS: For "name", "description", "extraIngredients", and ALL phase "instructionText", you MUST ALWAYS return a JSON OBJECT with BOTH "id" (Indonesian) and "en" (English) keys. NEVER return a plain string for these fields. Example: {"id": "Tuang air perlahan", "en": "Pour water slowly"}.
  - The "chatMessage" field is where you respond in the user's language as a plain string.
  - For "targetGrindSizeMicrons", output an integer. Use 400 (Sangat Halus/Espresso), 600 (Halus/Aeropress), 800 (Sedang/V60), 1000 (Agak Kasar/Chemex), 1200 (Kasar/French Press), or 1400 (Sangat Kasar/Cold Brew).
  - For "extraIngredients", write cleanly with metric units. DO NOT use acronyms like "sdm" or "SKM". If none, use {"id": "", "en": ""}.
  - At the very end of "description", ALWAYS add a new paragraph predicting the flavor profile in BOTH languages (inside the "id" and "en" keys respectively).
  - If you use physical actions like stir, swirl, cap, or flip, you MUST append a "wait" action exactly 5 seconds AFTER the physical action to give the user time to physically perform it. Do NOT put the wait action at the exact same startTimeSeconds.

The JSON must strictly follow this structure:
{
  "chatMessage": "Siap! Aku udah ubah ukuran gilingannya jadi lebih kasar buat nyesuain request kamu. Coba cek draftnya di bawah ya!",
  "recipe": {
    "name": {"id": "Resep Baru", "en": "New Recipe"},
    "description": {"id": "Penjelasan singkat.", "en": "Short explanation."},
    "coffeeGrams": 15,
    "targetGrindSizeMicrons": 800,
    "beanType": "Arabica",
    "extraIngredients": {"id": "15 ml susu kental manis", "en": "15 ml condensed milk"},
    "phases": [
      {
        "startTimeSeconds": 0,
        "pourAmountMl": 50,
        "action": "pourCircle",
        "instructionText": {"id": "Tuang 50 ml air", "en": "Pour 50 ml of water"}
      }
    ]
  }
}
Valid actions: pourCircle, pourCenter, wait, stir, swirl, cap, flip, press, openValve, closeValve.
`;
}

/** Strips the ```json fence some models wrap their output in. */
function stripCodeFence(raw: string): string {
  let text = raw.trim();
  if (text.startsWith('```json')) {
    text = text.slice(7);
    if (text.endsWith('```')) text = text.slice(0, -3);
  } else if (text.startsWith('```')) {
    text = text.slice(3);
    if (text.endsWith('```')) text = text.slice(0, -3);
  }
  return text;
}

/** Turns a base64 m4a voice note into text via Groq's Whisper endpoint. */
async function transcribeWithGroq(audioUri: string, apiKey: string): Promise<string> {
  const form = new FormData();
  form.append('model', GROQ_WHISPER_MODEL);
  form.append('response_format', 'json');
  // React Native's FormData takes a file descriptor object rather than raw
  // bytes, so Groq gets the recording's uri while Gemini gets the base64.
  form.append('file', {
    uri: audioUri,
    name: 'audio.m4a',
    type: 'audio/m4a',
  } as unknown as Blob);

  const response = await fetch(GROQ_TRANSCRIBE_URL, {
    method: 'POST',
    headers: { Authorization: `Bearer ${apiKey}` },
    body: form,
  });

  const text = await response.text();
  if (!response.ok) throw new Error(`WhisperError: ${response.status} - ${text}`);

  const data = JSON.parse(text);
  return data.text ?? '';
}

async function askGroq(
  systemInstruction: string,
  prompt: string,
  apiKey: string
): Promise<string> {
  const response = await fetch(GROQ_CHAT_URL, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${apiKey}`,
    },
    body: JSON.stringify({
      model: GROQ_CHAT_MODEL,
      messages: [
        { role: 'user', content: `${systemInstruction}\n\nUser request: ${prompt}` },
      ],
      response_format: { type: 'json_object' },
    }),
  });

  const body = await response.text();
  if (!response.ok) throw new Error(`ChatError: ${response.status} - ${body}`);

  return JSON.parse(body).choices[0].message.content as string;
}

async function askGemini(
  systemInstruction: string,
  prompt: string | null,
  audioBase64: string | null,
  apiKey: string
): Promise<string> {
  const parts: Record<string, unknown>[] = [{ text: systemInstruction }];
  if (prompt) parts.push({ text: `User request: ${prompt}` });
  if (audioBase64) {
    parts.push({ inlineData: { mimeType: 'audio/m4a', data: audioBase64 } });
  }

  const url =
    `https://generativelanguage.googleapis.com/v1beta/models/${GEMINI_MODEL}` +
    `:generateContent?key=${apiKey}`;

  const response = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      contents: [{ parts }],
      generationConfig: { responseMimeType: 'application/json' },
    }),
  });

  const body = await response.text();
  if (!response.ok) {
    throw new Error(`Failed to communicate with Gemini: ${response.status}\n${body}`);
  }

  const data = JSON.parse(body);
  const candidates = data.candidates;
  if (!Array.isArray(candidates) || candidates.length === 0) {
    throw new Error('Empty response from Gemini');
  }
  return candidates[0].content.parts[0].text as string;
}

export interface GenerateRecipeParams {
  prompt?: string | null;
  provider: AiProvider;
  /** The key for `provider`. Passing the wrong provider's key gets a 401. */
  apiKey: string;
  lang: string;
  /** Base64 m4a, for Gemini's inline audio. */
  audioBase64?: string | null;
  /** file:// uri of the same recording, for Groq's multipart upload. */
  audioUri?: string | null;
  currentRecipe?: Recipe | null;
}

export async function generateRecipe({
  prompt,
  provider,
  apiKey,
  lang,
  audioBase64,
  audioUri,
  currentRecipe,
}: GenerateRecipeParams): Promise<AiResponse> {
  if (apiKey.trim().length === 0) {
    throw new Error(str(lang, 'ai_error_no_key'));
  }

  const cleanKey = apiKey.trim();
  const systemInstruction = buildSystemInstruction(lang, currentRecipe);

  let jsonStr: string;

  if (provider === 'groq') {
    try {
      let finalPrompt = prompt ?? '';
      if (audioUri) {
        const transcript = await transcribeWithGroq(audioUri, cleanKey);
        finalPrompt += `\n[Voice Transcription]: ${transcript}`;
      }
      jsonStr = await askGroq(systemInstruction, finalPrompt, cleanKey);
    } catch (e) {
      throw new Error(`Koneksi Groq gagal. (${String(e)})`);
    }
  } else {
    jsonStr = await askGemini(
      systemInstruction,
      prompt ?? null,
      audioBase64 ?? null,
      cleanKey
    );
  }

  const data = JSON.parse(stripCodeFence(jsonStr));

  const chatMessage: string =
    typeof data.chatMessage === 'string'
      ? data.chatMessage
      : lang === 'en'
        ? 'Here is the draft!'
        : 'Ini draf resepnya!';
  const detectedLang: string =
    typeof data.detectedLang === 'string' ? data.detectedLang : lang;

  // Some models skip the "recipe" wrapper and return the fields at the top level.
  const recipeData = (data.recipe ?? data) as Record<string, any>;

  const rawPhases: any[] = Array.isArray(recipeData.phases) ? recipeData.phases : [];
  let totalWater = 0;

  const phases: RecipePhase[] = rawPhases.map((p) => {
    const amount = typeof p?.pourAmountMl === 'number' ? p.pourAmountMl : 0;
    totalWater += amount;
    const action: PhaseAction = PHASE_ACTIONS.includes(p?.action) ? p.action : 'pourCircle';
    return {
      startTimeSeconds: Math.trunc(Number(p?.startTimeSeconds ?? 0)),
      pourAmountMl: amount,
      action,
      instructionText: parseI18n(p?.instructionText),
    };
  });

  // The model gives phase start times but no overall length; allow 45s after the
  // last one for the final drawdown.
  const totalDurationSeconds =
    phases.length > 0 ? phases[phases.length - 1].startTimeSeconds + 45 : 180;

  const parsedName = parseI18n(recipeData.name);

  const recipe = makeRecipe({
    id: currentRecipe?.id,
    name: parsedName.length === 0 ? (currentRecipe?.name ?? 'AI Recipe') : parsedName,
    description: parseI18n(recipeData.description),
    coffeeGrams: typeof recipeData.coffeeGrams === 'number' ? recipeData.coffeeGrams : 15,
    totalWaterMl: totalWater,
    totalDurationSeconds,
    phases,
    targetGrindSizeMicrons:
      typeof recipeData.targetGrindSizeMicrons === 'number'
        ? Math.trunc(recipeData.targetGrindSizeMicrons)
        : (currentRecipe?.targetGrindSizeMicrons ?? 800),
    extraIngredients: parseI18n(recipeData.extraIngredients),
    beanType:
      typeof recipeData.beanType === 'string'
        ? recipeData.beanType
        : (currentRecipe?.beanType ?? 'Arabica'),
    method: currentRecipe?.method ?? 'v60',
  });

  return { recipe, chatMessage, detectedLang };
}
