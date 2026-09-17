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
  }) async {
    if (apiKey.trim().isEmpty) {
      throw Exception('API Key kosong. Silakan isi di Pengaturan (Settings).');
    }

    final cleanKey = apiKey.trim();
    
    String contextInfo = "";
    if (currentRecipe != null) {
      contextInfo = "\nThe user is currently editing a recipe: '${AppStrings.str(lang, currentRecipe.name)}'.\nCurrent Method: ${currentRecipe.method.name}\nCurrent Bean Type: ${currentRecipe.beanType}\nCurrent Grind Size: ${currentRecipe.targetGrindSizeMicrons} microns.\nCurrent Extra Ingredients: ${AppStrings.str(lang, currentRecipe.extraIngredients)}\nCurrent Description: ${AppStrings.str(lang, currentRecipe.description)}\nCurrent state: ${currentRecipe.coffeeGrams}g coffee, ${currentRecipe.totalWaterMl}ml water.\nPhases: ${currentRecipe.phases.map((e) => 'At ${e.startTimeSeconds}s: ${e.action.name} ${e.pourAmountMl}ml').join(', ')}\nPlease modify this recipe based on the user's request. Keep everything else intact unless requested to change.";
    } else {
      contextInfo = "\nPlease create a new pour-over coffee recipe based on the user's request.";
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
''';

    String jsonStr = '';

    if (provider == 'groq') {
      try {
        String finalPrompt = prompt ?? "";
        
        if (audioBase64 != null && audioBase64.isNotEmpty) {
          final whisperUrl = Uri.parse('https://api.groq.com/openai/v1/audio/transcriptions');
          var whisperReq = http.MultipartRequest('POST', whisperUrl);
          whisperReq.headers['Authorization'] = 'Bearer $cleanKey';
          whisperReq.headers['User-Agent'] = 'python-requests/2.31.0';
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

        final url = Uri.parse('https://api.groq.com/openai/v1/chat/completions');
        final body = jsonEncode({
          "model": "openai/gpt-oss-120b",
          "messages": [
            {
              "role": "user",
              "content": systemInstruction + "\n\nUser request: $finalPrompt"
            }
          ],
          "response_format": {"type": "json_object"}
        });

        final request = await http.post(url, body: body, headers: {
          'Content-Type': 'application/json', 
          'Authorization': 'Bearer $cleanKey',
          'User-Agent': 'python-requests/2.31.0'
        });
        if (request.statusCode != 200) throw Exception('ChatError: ${request.statusCode} - ${request.body}');

        final responseData = jsonDecode(request.body);
        jsonStr = responseData['choices'][0]['message']['content'] as String;

      } catch (e) {
        throw Exception('Koneksi Groq gagal. (${e.toString()})');
      }

    } else {
      final url = Uri.parse('https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=$cleanKey');
      final parts = <Map<String, dynamic>>[{"text": systemInstruction}];

      if (prompt != null && prompt.isNotEmpty) parts.add({"text": "User request: $prompt"});
      if (audioBase64 != null && audioBase64.isNotEmpty) {
        parts.add({"inlineData": {"mimeType": "audio/m4a", "data": audioBase64}});
      }

      final body = jsonEncode({
        "contents": [{"parts": parts}],
        "generationConfig": {"responseMimeType": "application/json"}
      });

      final request = await http.post(url, body: body, headers: {'Content-Type': 'application/json'});
      if (request.statusCode != 200) throw Exception('Failed to communicate with Gemini: ${request.statusCode}\n${request.body}');

      final responseData = jsonDecode(request.body);
      final candidates = responseData['candidates'] as List<dynamic>?;
      if (candidates == null || candidates.isEmpty) throw Exception('Empty response from Gemini');

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
        method: currentRecipe?.method ?? BrewMethod.v60,
      );
      
      
    
    return AiResponse(recipe: generatedRecipe, chatMessage: chatMessage, detectedLang: detectedLang);
  }
}
