import re
import os

with open('lib/core/ai_service.dart', 'r', encoding='utf-8') as f:
    text = f.read()

prompt = '''You are an expert barista. $contextInfo
Respond ONLY with a valid JSON object representing the recipe. Do not include any markdown formatting or extra text.
RULES:
- For "targetGrindSizeMicrons", use 400 (Sangat Halus/Espresso), 600 (Halus/Aeropress), 800 (Sedang/V60), 1000 (Agak Kasar/Chemex), 1200 (Kasar/French Press), or 1400 (Sangat Kasar/Cold Brew).
- For "extraIngredients", write cleanly with exact metric units (e.g. "15 ml susu kental manis", "100 gram es batu", "1 butir telur"). DO NOT use acronyms like "sdm" or "SKM". If none, leave blank string "".
- At the very end of "description", ALWAYS add a new paragraph starting exactly with "Estimasi Rasa: " that predicts the flavor profile (e.g. body, acidity, sweetness) that this recipe will produce.
- If you use physical actions like stir, swirl, cap, or flip, you MUST immediately append a "wait" action at the exact same startTimeSeconds if there is no immediate pour afterwards.

The JSON must strictly follow this structure:
{
  "name": "Recipe Name",
  "description": "Short explanation of what changed or why this recipe fits.\\n\\nEstimasi Rasa: Acidity cerah, body ringan, manis maksimal.",
  "coffeeGrams": 15,
  "targetGrindSizeMicrons": 800,
  "beanType": "Arabica",
  "extraIngredients": "15 ml susu kental manis, 100 gram es batu",
  "phases": [
    {
      "startTimeSeconds": 0,
      "pourAmountMl": 50,
      "action": "pourCircle"
    }
  ]
}
Valid actions: pourCircle, pourCenter, wait, stir, swirl, cap, flip, press, openValve, closeValve.
Valid beanTypes: Arabica, Robusta, Blend, Liberica, Excelsa, Bebas. If not specified by user, guess the most suitable one based on the recipe type.'''

text = re.sub(r'You are an expert barista.*?based on the recipe type\.\'\'\';', prompt + "\n''';", text, flags=re.DOTALL)

with open('lib/core/ai_service.dart', 'w', encoding='utf-8') as f:
    f.write(text)
print("Updated AI Prompt.")
