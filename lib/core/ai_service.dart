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
    double? mlPerSecond,
    double? secondsPerRotation,
  }) async {
    if (provider == 'gemini' && apiKey.trim().isEmpty) {
      throw Exception('API Key Gemini kosong. Silakan isi di Pengaturan (Settings).');
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

    // Build calibration info for the AI
    String calibrationInfo = "";
    if (mlPerSecond != null && mlPerSecond > 0 && secondsPerRotation != null) {
      final mlPerRotation = mlPerSecond * secondsPerRotation;
      calibrationInfo = """

USER'S CALIBRATION DATA (use this for calculations):
- Flow rate: ${mlPerSecond.toStringAsFixed(1)} ml/second
- Seconds per rotation (circular pour): ${secondsPerRotation.toStringAsFixed(1)} seconds
- ml per rotation: ${mlPerRotation.toStringAsFixed(1)} ml

HOW TO USE THIS DATA:
- For pourCircle: pourDuration = pourAmountMl / $mlPerSecond. Rotations = pourDuration / $secondsPerRotation. ALWAYS round rotations to the nearest 0.5 (e.g. 1, 1.5, 2, 2.5, 3). Never output values like 1.3 or 2.7 — round them to 1.5 and 3.0 respectively. Include rotation count in instructionText.
- For pourCenter: pourDuration = pourAmountMl / $mlPerSecond. Round duration to whole seconds. Include duration in instructionText.
- If the user says "I want X rotations": pourAmountMl = X * ${mlPerRotation.toStringAsFixed(1)}.
- If the user says "I want X seconds pour": pourAmountMl = X * $mlPerSecond.
- ALWAYS include the calculated rotation count or pour duration in EVERY pour phase's instructionText. Example: {"id": "Tuang 45 ml air memutar (3 putaran, 6 detik)", "en": "Pour 45 ml in circles (3 rotations, 6 seconds)"}.
""";
    } else {
      calibrationInfo = "\nNote: The user has NOT calibrated their equipment yet. Do not include rotation or time estimates in instructionText.\n";
    }

    String contextInfo = "";
    if (currentRecipe != null) {
      final currentPhasesSummary = currentRecipe.phases.map((e) => 'At ${e.startTimeSeconds}s: ${e.action.name} ${e.pourAmountMl}ml').join(', ');
      contextInfo = """

The user is currently editing an EXISTING recipe: '${AppStrings.str(lang, currentRecipe.name)}'.
Current Method: $methodName
Current Bean Type: ${currentRecipe.beanType}
Current Grind Size: ${currentRecipe.targetGrindSizeMicrons} microns
Current Extra Ingredients: ${AppStrings.str(lang, currentRecipe.extraIngredients)}
Current Description: ${AppStrings.str(lang, currentRecipe.description)}
Current Coffee: ${currentRecipe.coffeeGrams}g (DO NOT CHANGE unless explicitly requested)
Current Water: ${currentRecipe.totalWaterMl}ml (DO NOT CHANGE unless explicitly requested)
Current Phases: $currentPhasesSummary

EDITING MODE PRESERVATION RULE (HIGHEST PRIORITY - OVERRIDE ALL OTHER RULES):
You are EDITING an existing recipe. Follow these rules STRICTLY:
1. ONLY change what the user EXPLICITLY asks you to change. Nothing more, nothing less.
2. If the user asks to change a specific phase (e.g. "make the second pour longer" or "extend pour 2"), change ONLY that phase. Do NOT touch coffeeGrams, totalWaterMl, grind size, bean type, ratio, or unrelated phases.
3. If the user complains about taste (e.g. "too bitter", "too sour", "pahit"), you may adjust grind size or pour timing. But do NOT change coffeeGrams or the coffee-to-water ratio. Explain your grind/timing adjustment in chatMessage.
4. ONLY if the user says something like "change the entire recipe", "make a completely new recipe", or "start over", THEN you may change everything.
5. LOCKED VALUES (copy these EXACTLY into your output unless the user explicitly asks to change them): coffeeGrams=${currentRecipe.coffeeGrams}, totalWaterMl=${currentRecipe.totalWaterMl}, beanType="${currentRecipe.beanType}".
6. When splitting or merging pour phases, the TOTAL water (sum of all pourAmountMl) MUST remain exactly ${currentRecipe.totalWaterMl}ml.
7. When adjusting taste: change grind size or pour technique FIRST. Changing ratio is a LAST RESORT and requires explicit user permission.
""";
    } else {
      contextInfo = "\nPlease create a new $methodName coffee recipe based on the user's request. The brew method MUST be $methodName — do NOT switch to a different brewing method.";
    }

    final String appLangLabel = lang == 'en' ? 'English' : 'Indonesian';
    
    final systemInstruction = '''
You are a friendly, expert barista AI. $contextInfo
The app is currently set to $appLangLabel.
  1. "chatMessage": A friendly, conversational response explaining what you just did. You MUST respond in the SAME LANGUAGE the user used in their message. If the user writes in Indonesian, reply in Indonesian. If the user writes in English, reply in English. IMPORTANT: Use a very casual, warm, and enthusiastic tone, like a friendly barista talking to a friend (e.g., use words like "Siap!", "Oke deh", "Wah boleh banget!"). Keep it brief. When editing a recipe, briefly mention WHAT you changed and WHAT you kept the same (e.g. "Aku udah perpanjang tuangan kedua. Kopi dan air tetap sama ya!").
  2. "detectedLang": Either "id" or "en", representing the language you used in "chatMessage".
  3. "recipe": The actual modified or new recipe data.
  
  RULES for the recipe data:
  - ABSOLUTE RULE — NO EXCEPTIONS: For "name", "description", "extraIngredients", and ALL phase "instructionText", you MUST ALWAYS return a JSON OBJECT with BOTH "id" (Indonesian) and "en" (English) keys. NEVER return a plain string for these fields. Example: {"id": "Tuang air perlahan", "en": "Pour water slowly"}.
  - The "chatMessage" field is where you respond in the user's language as a plain string.
  - For "targetGrindSizeMicrons", output an integer. Use 400 (Espresso), 600 (Aeropress), 700 (Bright/Filter/Fruity), 800 (V60 Standard), 1000 (Chemex), 1200 (French Press), or 1400 (Cold Brew).
  - For "extraIngredients", write cleanly with metric units. DO NOT use acronyms like "sdm" or "SKM". If none, use {"id": "", "en": ""}.
  - At the very end of "description", ALWAYS add a new paragraph predicting the flavor profile in BOTH languages (inside the "id" and "en" keys respectively).
      - "coffeeGrams" must be at least 15g for a standard single serving. Never go below 12g unless explicitly requested.
    - TOTAL DURATION RULE: You MUST always update the root `totalDurationSeconds` field. It must be equal to the `startTimeSeconds` of the LAST phase plus 30 to 45 seconds for drawdown. NEVER leave `totalDurationSeconds` unadjusted if you pushed the last phase to a later time.
    - CRITICAL TIMING RULE: NEVER place two different actions at the exact same `startTimeSeconds`. Each phase MUST have a unique start time.
    - WAIT PHASE RULE (READ CAREFULLY): The app automatically tells the user to "Wait" right after they finish a `pourCircle` or `pourCenter`. Therefore, NEVER insert a `wait` phase between a pour and the next pour. The time gap is handled automatically. HOWEVER, if you instruct the user to do a PHYSICAL ACTION (stir, swirl, flip, cap) in the middle of a gap, you MUST insert a `wait` phase exactly 5 seconds AFTER that physical action. This is required so the app knows when to tell the user to stop stirring/swirling.
  - PRESERVATION RULE: When editing a recipe, the total water poured (sum of all pourAmountMl) MUST equal the original totalWaterMl unless the user explicitly asks to change the water amount or ratio. If you split or merge pours, the total MUST remain the same.
    - SCALING RULE: When the user asks to change the coffee dose or total water, you MUST scale EVERY pourAmountMl proportionally to maintain the EXACT ratio of the original recipe''s pours. For example, if original has 50ml and 70ml out of 300ml, and user scales down to 180ml total, new pours MUST be exactly 30ml and 42ml. DO NOT replace the pour structure with generic knowledge!

$methodSpecificGuide
$calibrationInfo

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
        "temperature": 0.1,
        "messages": [
          {
            "role": "system",
            "content": systemInstruction
          },
          {
            "role": "user",
            "content": "User request: " + finalPrompt
          }
        ],
        "response_format": {"type": "json_object"}
      });
    } else {
        final parts = <Map<String, dynamic>>[];
        if (prompt != null && prompt.isNotEmpty) {
          parts.add({"text": "User request: " + prompt});
        }
        
        if (audioBase64 != null && audioBase64.isNotEmpty) {
          parts.add({"inlineData": {"mimeType": "audio/m4a", "data": audioBase64}});
        }
        
        body = jsonEncode({
          "systemInstruction": {
            "parts": [{"text": systemInstruction}]
          },
          "contents": [{"role": "user", "parts": parts}],
          "generationConfig": {
            "responseMimeType": "application/json",
            "temperature": 0.1
          }
        });
      }

    http.Response? request;
    int retryCount = 0;
    
    final Map<String, String> headers = {
      'Content-Type': 'application/json',
    };
    
    Uri targetUrl;
    if (provider == 'gemini') {
      targetUrl = Uri.parse('https://generativelanguage.googleapis.com/v1beta/models/gemini-3.6-flash:generateContent?key=$cleanKey');
    } else {
      targetUrl = Uri.parse('https://divine-art-85f1.aswar-drummer.workers.dev/');
      headers['X-AI-Provider'] = provider;
    }

    while (retryCount < 3) {
      request = await http.post(targetUrl, body: body, headers: headers);
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
      // Print the actual response body to know why it failed
      throw Exception('Error ${request.statusCode}: ${request.body}');
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
        isKasuya46: currentRecipe?.isKasuya46 ?? false,
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
