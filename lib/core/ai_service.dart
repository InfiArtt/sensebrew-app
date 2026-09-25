import 'dart:convert';
import 'package:http/http.dart' as http;
import 'recipe.dart';
import 'app_strings.dart';
import '../main.dart'; // for navigatorKey context if needed

class AiResponse {
  final Recipe recipe;
  final String chatMessage;
  final String detectedLang;

  AiResponse({required this.recipe, required this.chatMessage, required this.detectedLang});
}

class AiService {

  static String parseI18n(dynamic field) {
    if (field == null) return '';
    if (field is String) {
      // If already in bilingual format, return as-is
      if (field.contains('ID: ') && field.contains('|| EN: ')) return field;
      // Plain string from AI — wrap as both languages (best effort)
      // This handles the case where AI ignores the JSON object instruction
      if (field.trim().isNotEmpty) {
        return 'ID: ' + field.trim() + ' || EN: ' + field.trim();
      }
      return field;
    }
    if (field is Map) {
      final idStr = field['id']?.toString() ?? '';
      final enStr = field['en']?.toString() ?? '';
      if (idStr.isEmpty && enStr.isEmpty) return '';
      return 'ID: ' + idStr + ' || EN: ' + enStr;
    }
    return field.toString();
  }

  static Future<AiResponse> generateRecipe({
    required String? prompt,
    required String provider,
    required String apiKey,
    required String lang,
    String? audioBase64,
    Recipe? currentRecipe,
    BrewMethod? targetMethod,
  }) async {
    if (apiKey.trim().isEmpty) {
      throw Exception('API Key kosong. Silakan isi di Pengaturan (Settings).');
    }

    final cleanKey = apiKey.trim();
    
    // Determine effective method: from currentRecipe, or targetMethod, or default V60
    final BrewMethod effectiveMethod = currentRecipe?.method ?? targetMethod ?? BrewMethod.v60;
    
    // Human-readable method names for the prompt
    final Map<BrewMethod, String> methodNames = {
      BrewMethod.v60: 'V60 Pour-Over',
      BrewMethod.frenchPress: 'French Press',
      BrewMethod.aeropress: 'Aeropress',
      BrewMethod.vietnamDrip: 'Vietnam Drip',
      BrewMethod.cupping: 'SCA Cupping',
    };
    final String methodName = methodNames[effectiveMethod] ?? 'V60 Pour-Over';

    String methodSpecificGuide = "";
    if (effectiveMethod == BrewMethod.v60) {
      methodSpecificGuide = """
  V60 POUR-OVER FLAVOR & TECHNIQUE GUIDE:
  - Fruity / Bright: grind=700, ratio=1:15. TECHNIQUE: Calculate total water. Bloom pourCircle with exactly 2x coffee weight at 0s. Subtract bloom water from total water, then split the remaining water equally into exactly 2 large fast pours at 35s and 70s. (Fewer, larger pours = shorter contact time = brighter acidity).
  - Balanced: grind=800, ratio=1:15. TECHNIQUE: Bloom 2.5x coffee weight at 0s. Split remaining water into 2 or 3 equal pours spaced 35s apart.
  - Chocolatey / Bold: grind=900, ratio=1:14. TECHNIQUE: Bloom 3x coffee weight at 0s. Split remaining water into 3 or 4 small pours spaced 30s apart. Add a "stir" action exactly 10s after the final pour starts.
  - Sweet / Caramel: grind=800, ratio=1:16. TECHNIQUE: bloom at 0s, wait 45s, then 2-3 slow pours spaced 40s apart.
""";
    } else if (effectiveMethod == BrewMethod.frenchPress) {
      methodSpecificGuide = """
  FRENCH PRESS TECHNIQUE GUIDE (IMMERSION):
  - Standard Grind: 1200 (Coarse), Ratio: 1:15.
  - Hoffmann Method (Default for Clean Cup): pourCenter ALL water at 0s. 'wait' at 15s. 'stir' (break crust) at 240s (4 mins). 'wait' at 245s (let grounds sink). 'press' at 540s (9 mins).
  - Traditional Method (Default for Bold): pourCenter ALL water at 0s. 'wait' at 15s. 'press' slowly at 240s (4 mins).
""";
    } else if (effectiveMethod == BrewMethod.aeropress) {
      methodSpecificGuide = """
  AEROPRESS TECHNIQUE GUIDE (IMMERSION + PRESSURE):
  - Standard Grind: 600, Ratio: 1:15.
  - Inverted Technique (For Bold/Full Body): pourCenter ALL water at 0s. 'stir' at 15s. 'wait' at 20s. 'flip' at 90s. 'wait' at 95s. 'press' slowly for 30s starting at 105s.
  - Standard / Upright Technique (For Clean/Bright): pourCenter ALL water at 0s. 'stir' at 15s. 'cap' at 20s (CRITICAL: this creates a vacuum to stop water dripping). 'wait' at 25s. 'press' slowly for 30s starting at 90s. Do NOT use 'flip'.
""";
    } else if (effectiveMethod == BrewMethod.vietnamDrip) {
      methodSpecificGuide = """
  VIETNAM DRIP TECHNIQUE GUIDE (SLOW DRIP):
  - Standard Grind: 800, Ratio: 1:10 (usually over condensed milk).
  - Technique: pourCenter a small bloom (20ml) at 0s. pourCenter remaining water at 30s. 'cap' the lid at 40s. 'wait' at 45s for 4-5 minutes as it drips.
""";
    } else if (effectiveMethod == BrewMethod.cupping) {
      methodSpecificGuide = """
  SCA CUPPING TECHNIQUE GUIDE (EVALUATION):
  - Standard Grind: 850, Ratio: strictly 8.25g per 150ml (1:18).
  - Technique: pourCenter ALL water at 0s. 'wait' at 15s. 'stir' (to break crust) 3 times at 240s (4 mins). 'wait' at 245s. Taste coffee starting at 600s (10 mins).
""";
    }

    String contextInfo = "";
    if (currentRecipe != null) {
      contextInfo = "\nThe user is currently editing a recipe: '${AppStrings.str(lang, currentRecipe.name)}'.\nCurrent Method: ${methodName}\nCurrent Bean Type: ${currentRecipe.beanType}\nCurrent Grind Size: ${currentRecipe.targetGrindSizeMicrons} microns.\nCurrent Extra Ingredients: ${AppStrings.str(lang, currentRecipe.extraIngredients)}\nCurrent Description: ${AppStrings.str(lang, currentRecipe.description)}\nCurrent state: ${currentRecipe.coffeeGrams}g coffee, ${currentRecipe.totalWaterMl}ml water.\nPhases: ${currentRecipe.phases.map((e) => 'At ${e.startTimeSeconds}s: ${e.action.name} ${e.pourAmountMl}ml').join(', ')}\nPlease modify this recipe based on the user's request. Keep everything else intact unless requested to change.";
    } else {
      contextInfo = "\nPlease create a new $methodName coffee recipe based on the user's request. The brew method MUST be $methodName — do NOT switch to a different brewing method.";
    }

    final String appLangLabel = lang == 'en' ? 'English' : 'Indonesian';
    
    final systemInstruction = '''
You are a friendly, expert barista AI. $contextInfo
The app is currently set to $appLangLabel.
  1. "chatMessage": A friendly, conversational response explaining what you just did. You MUST respond in the SAME LANGUAGE the user used in their message. If the user writes in Indonesian, reply in Indonesian. If the user writes in English, reply in English. IMPORTANT: Use a very casual, warm, and enthusiastic tone, like a friendly barista talking to a friend (e.g., use words like "Siap!", "Oke deh", "Wah boleh banget!"). Keep it brief.
  2. "detectedLang": Either "id" or "en", representing the language you used in "chatMessage".
  3. "recipe": The actual modified or new recipe data.
  
  RULES for the recipe data:
  - ABSOLUTE RULE — NO EXCEPTIONS: For "name", "description", "extraIngredients", and ALL phase "instructionText", you MUST ALWAYS return a JSON OBJECT with BOTH "id" (Indonesian) and "en" (English) keys. NEVER return a plain string for these fields. Example: {"id": "Tuang air perlahan", "en": "Pour water slowly"}.
  - The "chatMessage" field is where you respond in the user's language as a plain string.
  - For "targetGrindSizeMicrons", output an integer. Use 400 (Espresso), 600 (Aeropress), 700 (Bright/Filter/Fruity), 800 (V60 Standard), 1000 (Chemex), 1200 (French Press), or 1400 (Cold Brew).
  - For "extraIngredients", write cleanly with metric units. DO NOT use acronyms like "sdm" or "SKM". If none, use {"id": "", "en": ""}.
  - At the very end of "description", ALWAYS add a new paragraph predicting the flavor profile in BOTH languages (inside the "id" and "en" keys respectively).
  - If you use physical actions like stir, swirl, cap, or flip, you MUST append a "wait" action exactly 5 seconds AFTER the physical action to give the user time to physically perform it.
  - "coffeeGrams" must be at least 15g for a standard single serving. Never go below 12g unless explicitly requested.
  - CRITICAL TIMING RULE: NEVER place two different actions at the exact same `startTimeSeconds`. Each phase MUST have a unique start time. For example, if you pour water at 60s, and you want to stir afterwards, the stir action MUST be placed at a later time (e.g. 70s or 75s), NOT at 60s. Overlapping times will crash the app's timer.
  - CRITICAL BLOOM RULE: NEVER insert a "wait" phase between a bloom pour and the next pour. The time gap between phases IS the waiting period — the app's timer counts it automatically and announces a countdown before the next phase. Correct example: bloom pourCircle at 0s (45ml), then next pourCircle at 35s (no wait phase in between). WRONG example: bloom at 0s, wait at 5s, pour at 35s — this blocks the app countdown system.
  - "wait" action is ONLY allowed: (a) after physical actions like stir/swirl/cap/flip, OR (b) during French Press / long steep methods where a multi-minute rest is needed.

$methodSpecificGuide

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
''';

    String jsonStr = '';

    final url = Uri.parse('https://divine-art-85f1.aswar-drummer.workers.dev/');
    
    // We construct a unified request body for our proxy.
    // Our proxy currently acts differently based on provider:
    // If it's groq, the proxy expects Groq payload. If it's Gemini, it expects Gemini payload.
    // Wait, in our Cloudflare Worker, we just forward the body directly!
    // So Flutter MUST construct the exact body that the target AI server expects.

    String body = '';
    
    if (provider == 'groq') {
      String finalPrompt = prompt ?? "";
      if (audioBase64 != null && audioBase64.isNotEmpty) {
        // Use whisper via proxy
        final whisperReq = http.MultipartRequest('POST', url);
        whisperReq.headers['X-AI-Provider'] = 'groq';
        whisperReq.headers['X-AI-Action'] = 'transcribe';
        whisperReq.fields['model'] = 'whisper-large-v3';
        whisperReq.fields['response_format'] = 'json';
        whisperReq.files.add(http.MultipartFile.fromBytes('file', base64Decode(audioBase64), filename: 'audio.m4a'));
        
        final whisperRes = await whisperReq.send();
        final whisperBody = await whisperRes.stream.bytesToString();
        
        if (whisperRes.statusCode != 200) {
            throw Exception('WhisperError: ${whisperRes.statusCode} - $whisperBody');
        }
        
        final whisperData = jsonDecode(whisperBody);
        String transcribedText = whisperData['text'] ?? "";
        finalPrompt += "\n[Voice Transcription]: $transcribedText";
      }
      
      body = jsonEncode({
        "model": "openai/gpt-oss-120b",
        "messages": [
          {
            "role": "user",
            "content": systemInstruction + "\n\nUser request: " + finalPrompt
          }
        ],
        "response_format": {"type": "json_object"}
      });
    } else {
      final parts = <Map<String, dynamic>>[{"text": systemInstruction}];
      if (prompt != null && prompt.isNotEmpty) parts.add({"text": "User request: $prompt"});
      if (audioBase64 != null && audioBase64.isNotEmpty) {
        parts.add({"inlineData": {"mimeType": "audio/m4a", "data": audioBase64}});
      }
      body = jsonEncode({
        "contents": [{"parts": parts}],
        "generationConfig": {"responseMimeType": "application/json"}
      });
    }

    http.Response? request;
    int retryCount = 0;
    while (retryCount < 3) {
      request = await http.post(url, body: body, headers: {
        'Content-Type': 'application/json',
        'X-AI-Provider': provider
      });
      if (request.statusCode == 503 || request.statusCode == 500) {
        retryCount++;
        if (retryCount >= 3) break;
        await Future.delayed(const Duration(seconds: 2));
      } else {
        break;
      }
    }

    if (request!.statusCode != 200) {
      if (request.statusCode == 503 || request.statusCode == 500) {
        throw Exception(lang == 'en' ? 'Server is busy (Error 503). Please wait a moment and try again.' : 'Server sedang sibuk (Error 503). Silakan tunggu sebentar dan coba lagi.');
      }
      if (request.statusCode == 429) {
        throw Exception(lang == 'en' ? 'API Quota Exhausted.' : 'Kuota API harian habis.');
      }
      throw Exception('Failed to communicate with Proxy: ${request.statusCode}');
    }

    final responseData = jsonDecode(request.body);
    
    if (provider == 'groq') {
      jsonStr = responseData['choices'][0]['message']['content'] as String;
    } else {
      final candidates = responseData['candidates'] as List<dynamic>?;
      if (candidates == null || candidates.isEmpty) throw Exception('Empty response from AI');
      jsonStr = candidates[0]['content']['parts'][0]['text'] as String;
    }
    
    jsonStr = jsonStr.trim();
    if (jsonStr.startsWith('```json')) {
      jsonStr = jsonStr.substring(7);
      if (jsonStr.endsWith('```')) jsonStr = jsonStr.substring(0, jsonStr.length - 3);
    } else if (jsonStr.startsWith('```')) {
      jsonStr = jsonStr.substring(3);
      if (jsonStr.endsWith('```')) jsonStr = jsonStr.substring(0, jsonStr.length - 3);
    }

    final Map<String, dynamic> data = jsonDecode(jsonStr);
    
    final String chatMessage = data['chatMessage'] as String? ?? (lang == 'en' ? "Here is the draft!" : "Ini draf resepnya!");
    final String detectedLang = data['detectedLang'] as String? ?? lang;
    final Map<String, dynamic> recipeData = data['recipe'] as Map<String, dynamic>? ?? data; // Fallback if AI didn't nest it

    final List<dynamic> phasesData = (recipeData['phases'] as List<dynamic>?) ?? [];
    double totalWater = 0;
    
    final List<RecipePhase> phases = phasesData.map<RecipePhase>((p) {
      double amount = (p['pourAmountMl'] as num?)?.toDouble() ?? 0.0;
      totalWater += amount;
      String actionStr = p['action'] as String? ?? 'pourCircle';
      PhaseAction action = PhaseAction.values.firstWhere((e) => e.name == actionStr, orElse: () => PhaseAction.pourCircle);
      
      return RecipePhase(
        startTimeSeconds: (p['startTimeSeconds'] as num?)?.toInt() ?? 0,
        pourAmountMl: amount,
        action: action,
        instructionText: parseI18n(p['instructionText']),
      );
    }).toList();

    int totalDuration = phases.isNotEmpty ? phases.last.startTimeSeconds + 45 : 180;


      final Recipe generatedRecipe = Recipe(
        id: currentRecipe?.id, 
        name: parseI18n(recipeData['name']).isEmpty ? (currentRecipe?.name ?? 'AI Recipe') : parseI18n(recipeData['name']),
        description: parseI18n(recipeData['description']),
        coffeeGrams: (recipeData['coffeeGrams'] as num?)?.toDouble() ?? 15.0,
        totalWaterMl: totalWater,
        totalDurationSeconds: totalDuration,
        phases: phases,
        targetGrindSizeMicrons: (recipeData['targetGrindSizeMicrons'] as num?)?.toInt() ?? currentRecipe?.targetGrindSizeMicrons ?? 800,
        extraIngredients: parseI18n(recipeData['extraIngredients']),
        beanType: recipeData['beanType'] as String? ?? currentRecipe?.beanType ?? 'Arabica',
        method: effectiveMethod,
      );
      
      
    
    return AiResponse(recipe: generatedRecipe, chatMessage: chatMessage, detectedLang: detectedLang);
  }
}
