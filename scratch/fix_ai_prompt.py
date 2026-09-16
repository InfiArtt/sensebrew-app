import re

with open('lib/core/ai_service.dart', 'r', encoding='utf-8') as f:
    text = f.read()

old_prompt = """The JSON must strictly follow this structure:
{
  "name": "Recipe Name",
  "description": "Short explanation of what changed or why this recipe fits.",
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
Valid actions: pourCircle, pourCenter, wait, stir, press.
Valid beanTypes: Arabica, Robusta, Blend, Liberica, Excelsa, Bebas. If not specified by user, guess the most suitable one based on the recipe type."""

new_prompt = """- At the very end of "description", ALWAYS add a new paragraph starting exactly with "Estimasi Rasa: " that predicts the flavor profile (e.g. body, acidity, sweetness) that this recipe will produce.
- If you use physical actions like stir, swirl, cap, or flip, you MUST immediately append a "wait" action at the exact same startTimeSeconds if there is no immediate pour afterwards.

The JSON must strictly follow this structure:
{
  "name": "Recipe Name",
  "description": "Short explanation of what changed or why this recipe fits.\\n\\nEstimasi Rasa: Acidity cerah, manis maksimal, body ringan.",
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
Valid beanTypes: Arabica, Robusta, Blend, Liberica, Excelsa, Bebas. If not specified by user, guess the most suitable one based on the recipe type."""

if old_prompt in text:
    text = text.replace(old_prompt, new_prompt)
    with open('lib/core/ai_service.dart', 'w', encoding='utf-8') as f:
        f.write(text)
    print("AI Prompt string replaced successfully.")
else:
    print("Could not find the old prompt string.")
