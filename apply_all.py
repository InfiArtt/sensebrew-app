import json

missing = {
  "ai_voice_note": "\\u{1F399}\\u{FE0F} [Voice Message]",
  "settings_title": "Settings",
  "settings_restore_title": "Restore Default Recipes",
  "settings_restore_sub": "Restore deleted built-in recipes",
  "theme_title": "App Theme",
  "recipe_label": "Recipe {0}. {1} grams of coffee. {2} milliliters of water.",
  "calib_title": "Brewing Equipment & Flow Rate Calibration',      'stop_metronome': 'Stop Metronome",
  "start_metronome": "Play Metronome",
  "save_calib": "SAVE CALIBRATION",
  "save_calib_label": "Save calibration results",
  "save_success": "Calibration saved successfully.",
  "pour_calc_title": "Pour Calculator",
  "pour_calc_desc": "Free pour assistant. Enter the amount of water (ml) you want to pour, and the app will calculate and guide the timing based on your kettle's calibration.",
  "pour_calc_target": "Pour Target (ml)",
  "pour_calc_est": "Estimated Time: {0} seconds",
  "pour_calc_start": "Start Pour",
  "pour_calc_stop": "Stop",
  "pour_calc_ready": "Get ready, pouring in",
  "reduce": "Reduce to {0} {1}",
  "add": "Increase to {0} {1}",
  "custom_title": "Create Custom Recipe",
  "recipe_name": "Recipe Name",
  "recipe_note": "Brewing Notes & Rules",
  "coffee_grams": "Coffee (grams)",
  "total_water": "Total Water (milliliters)",
  "total_time": "Total Time (seconds)",
  "phases_title": "Brewing Phases",
  "add_phase": "Add Phase",
  "delete_phase": "Delete Phase",
  "water_ml": "Water (ml)",
  "start_sec": "Start at Second",
  "action_pour_circle": "Spiral Pour",
  "action_pour_center": "Center Pour",
  "action_stir": "Stir",
  "action_wait": "Wait",
  "action_press": "Press",
  "action_pourFast": "Direct Pour",
  "action_openValve": "Open Valve",
  "action_closeValve": "Close Valve",
  "save_recipe": "Save Recipe",
  "save_overwrite": "Overwrite Existing",
  "save_as_new": "Save as New",
  "save_recipe_success": "Recipe saved successfully!",
  "brew_title": "Brewing Now",
  "brew_sec": "Second: {0}\\n{1}",
  "start_brew_btn": "START",
  "start_brew_label": "Start brewing",
  "cancel_brew_btn": "CANCEL",
  "cancel_brew_label": "Cancel brewing",
  "finish_brew_btn": "DONE",
  "finish_brew_label": "Finish brewing",
  "brew_complete": "Brewing Complete!",
  "brew_phases": "Brewing Phases:",
  "brew_phase_item_circle": "• Second {0}: Pour {1} ml ({2} rotations)",
  "brew_phase_item_center": "• Second {0}: Pour {1} ml ({2} seconds)",
  "brew_phase_item_stir": "• Second {0}: Stir",
  "brew_phase_item_press": "• Second {0}: Press",
  "brew_phase_item_wait": "• Second {0}: Wait",
  "pour_circle_instruction": "Pour {0} mili, {1} rotations.",
  "pour_center_instruction": "Center pour {0} mili for {1} seconds.",
  "stir_instruction": "Stir.",
  "press_instruction": "Press slowly.",
  "pour_fast_instruction": "Pour {0} mili of water.",
  "wait_instruction": "Wait...",
  "open_valve_instruction": "Open the valve.",
  "close_valve_instruction": "Close the valve.",
  "ai_title": "AI Assistant",
  "ai_recipe_label": "Generated Recipe",
  "ai_recipe_btn": "Use Recipe",
  "ai_prompt_label": "What kind of coffee do you want?",
  "ai_prompt_hint": "E.g: Sweet iced coffee using V60",
  "ai_generating": "Generating recipe...",
  "app_lang": "Language",
  "app_lang_label": "App Language",
  "app_lang_desc": "Select the language for the app",
  "tts_channel_changed": "Audio channel changed to {0}",
  "tts_voice_changed": "Voice changed to {0}",
  "tts_pitch_changed": "Voice pitch changed to {0}",
  "gemini_title": "Google Gemini API Key",
  "gemini_desc": "Enter your Gemini API key to use AI features.",
  "gemini_help_title": "How to get a Gemini API Key?",
  "desc_lance": "PERCOLATION method relying on 1 long pour. Pour very slowly and gently, letting the water rise slowly without disturbing the coffee bed at the bottom.",
  "desc_kurasu": "An all-rounder PERCOLATION method. Produces a very clean cup. Pour the remaining water right after the blooming water has fully drained.",
  "desc_april": "A recipe specifically for the April Pour-Over Brewer. Uses a coarse grind and a flat bed. Two circular pours and two center pours.",
  "desc_hoffmann": "James Hoffmann's ultimate V60 recipe. Uses a swirl during bloom and at the end. Medium-fine grind. Focuses on even extraction and high yield.",
  "desc_kasuya": "Tetsu Kasuya's 4:6 method. Coarse grind. Divides water into 40% (for sweetness/acidity balance) and 60% (for strength).",
  "desc_rao": "Scott Rao's method. Uses a single long pour after bloom, followed by a 'Rao Spin' to level the bed and prevent channeling.",
  "desc_osmotic": "Osmotic Flow method. Pour slowly only in the center to maintain the coffee dome. Maximizes sweetness and minimizes bitterness.",
  "desc_perger": "Matt Perger's V60 recipe. Fine grind. Uses a tap to level the bed before brewing. Two pours. High extraction yield.",
  "default": "Default",
  "close": "Close",
  "note": "Note",
  "note_label": "Add Note"
}

with open("full_id.json", "r", encoding="utf-8") as f:
    id_data = json.load(f)

# The keys in missing_keys.json also included desc_key_0 to 8 which I already provided in fix_dart3!
# Let me load all_trans from previous script to NOT override them if not needed.
# Actually, I can just apply the exact same logic as fix_dart3 but with missing merged into ll_trans.

with open("lib/core/app_strings.dart", "r", encoding="utf-8") as f:
    content = f.read()

import re
id_block_match = re.search(r"('id': \{)(.*?)(\n    \},)", content, re.DOTALL)
id_text = id_block_match.group(2)
en_block_match = re.search(r"('en': \{)(.*?)(\n    \},)", content, re.DOTALL)
en_text = en_block_match.group(2)

# Load existing translated_new.json
with open("translated_new.json", "r", encoding="utf-8") as f:
    trans_new = json.load(f)

ui_translations = {
    'header_favorites': '⭐ Favorites',
    'header_custom': '✨ Your Recipes',
    'header_builtin': '☕ Standard Recipes',
    'mark_favorite': 'Mark as favorite',
    'remove_favorite': 'Remove from favorites',
    'Ca Phe Sua Da (Kopi Susu Es)': 'Ca Phe Sua Da (Iced Milk Coffee)',
    'Ca Phe Den (Kopi Hitam)': 'Ca Phe Den (Black Coffee)',
    'Vietnam Drip Gula Aren': 'Vietnam Drip Palm Sugar',
    'Tradisional Vietnam Drip': 'Traditional Vietnam Drip',
    'brew_dose': 'Coffee Dose: {0} scoops',
    'brew_grind': 'Grind Size',
    'brew_bean': 'Coffee Bean Type',
    'brew_extra': 'Extra Ingredients',
    'brew_desc_title': 'Recipe Description:',
    'rotations_half': ' and a half',
    'custom_grind_400': 'Very Fine (Espresso)',
    'custom_grind_600': 'Fine (Aeropress)',
    'custom_grind_800': 'Medium (V60 / Kalita)',
    'custom_grind_1000': 'Medium Coarse (Chemex)',
    'custom_grind_1200': 'Coarse (French Press / Switch)',
    'custom_grind_1400': 'Very Coarse (Cold Brew)',
    'custom_bean_blend': 'Blend',
    'custom_bean_bebas': 'Any Bean',
    'custom_recipe_desc': 'Recipe Description',
    'custom_recipe_extra_hint': 'E.g: 15 ml condensed milk, 100 g ice cubes',
    'home_select_method': 'Select Brew Method:',
    'method_v60_desc': 'Pour-over brewing with spiral pours',
    'method_fp_desc': 'Immersion brewing without grounds',
    'method_ap_desc': 'Press brewing using air pressure',
    'method_vd_desc': 'Slow drip brewing (Milk Coffee)',
    'method_cup_desc': 'International coffee evaluation standard',
    'calib_guide': 'Calibration Guide:\\n1. Prepare a kettle with water and a scale or measuring cup.\\n2. Activate the Metronome Simulation button below.\\n3. After the start cue, pour water as usual.\\n4. Count how many TICK sounds you hear until the water reaches your target volume.\\n5. Try pouring in a circle, and count how many TICK sounds it takes to complete one full rotation.\\n6. Enter those numbers into the fields below!',
    'calib_header': 'Brewing Equipment & Flow Rate Calibration',
    'calib_q1': 'What is the volume/weight of your measuring cup or target in ml/grams?',
    'calib_q2': 'Turn on the metronome, then pour water. How many seconds (beats) does it take to reach the target?',
    'calib_q3': 'Typically, how many seconds do you need to complete 1 full circle rotation (spiral) when pouring?',
    'toggle_api_key': 'Show or hide API Key',
    'restore_success': 'Default recipes restored successfully!',
    'calib_grinder_select': 'Select Your Grinder:',
    'calib_grinder_title': 'Select Grinder',
    'calib_grinder_manual': 'Manual Grinder',
    'calib_grinder_electric': 'Electric Grinder',
    'calib_spoon_q': 'What is the capacity of your measuring scoop in grams?',
    'calib_sim_btn': 'Metronome Simulation (Play Countdown)',
    'action_swirl': 'Swirl gently',
    'action_cap': 'Attach Cap',
    'action_flip': 'Flip onto cup',
    'ai_chat_title': 'Design with AI',
    'app_title': 'SenseBrew',
    'settings_menu': 'App Settings Menu',
    'calibrate_flow_rate': 'Brewing Equipment & Flow Rate Calibration',
    'calibrated_status': 'Device ready. Flow rate: {0} ml per second',
    'uncalibrated_status': 'Flow rate not calibrated.',
    'calibrated_btn': '{0} ml/second',
    'uncalibrated_btn': '(Required)',
    'custom_recipe_btn': 'Custom\\nRecipe',
    'custom_recipe_label': 'Create a custom brew recipe.',
    'language_selector': 'Change Language',
    'theme_selector': 'Toggle Dark Mode',
    'pour_calculator_title': 'Pour Calculator',
    'calc_ratio_label': 'Water Ratio (1:X)',
    'calc_coffee_label': 'Coffee Dose (grams)',
    'calc_water_label': 'Total Water (ml)',
    'calc_result': 'Result',
    'calc_needs': 'You need {0} ml of water.',
    'calc_yield': 'You will get around {0} ml of coffee.',
    'ai_generate_btn': 'Generate Recipe with AI',
    'ai_hint': 'E.g: I want a sweet V60 recipe for 15g coffee.',
    'ai_loading': 'AI is thinking...',
    'ai_success': 'Recipe generated successfully!',
    'ai_error': 'Failed to connect to AI.',
    'ai_model_selector': 'AI Model',
    'ai_key_placeholder': 'Enter your Groq API Key',
    'ai_save_key': 'Save Key',
    'ai_key_saved': 'API Key saved!',
    'ai_error_no_key': 'API Key is empty. Please fill it in Settings first.',
    'ai_error_failed': 'Failed to create recipe: {0}',
    'edit_btn': 'Edit',
    'delete_btn': 'Delete',
    'brew_btn': 'Brew',
    'delete_confirm_title': 'Delete Recipe?',
    'delete_confirm_desc': 'Are you sure you want to delete the recipe {0}?',
    'tts_title': 'Voice & Language (TTS)',
    'tts_enable': 'Voice Instructions',
    'tts_enable_desc': 'Turn off if you only want to hear the metronome',
    'tts_channel': 'Audio Channel',
    'tts_channel_desc': "Select who will read the instructions",
    'tts_channel_app': 'TTS',
    'tts_channel_sr': 'Screen Reader',
    'tts_lang': 'Voice Language',
    'tts_speed': 'Voice Speed',
    'tts_pitch': 'Voice Pitch',
    'tts_voice': 'Voice Selection',
    'tts_voice_desc': "Available voices depend on your phone's engine",
    'tts_speed_changed': 'Speed changed to {0}',
    'grinder_clicks': 'clicks',
    'gemini_help_content': '1. Go to aistudio.google.com\\n2. Log in with your Google account.\\n3. Click "Get API key" > "Create API key".\\n4. Copy the code.\\n\\nNote: This service is free and does not require a credit card.',
    'groq_help_content': '1. Go to console.groq.com/keys\\n2. Log in with your account.\\n3. Click "Create API Key".\\n4. Copy the code (usually starts with gsk_).\\n\\nNote: This service is free and does not require a credit card.'
}

# The missing 0-8 from earlier
missing["desc_key_5"] = "Classic Hario factory recipe. Very beginner-friendly. Pour slowly in a circular motion from the center outwards, then back to the center.\n\nFlavor Profile: Classic, medium body, prominent acidity, and strong brewing aroma."
missing["desc_key_6"] = "God Recipe by Tetsu Kasuya. Temperature 90°C. OPEN the valve at the start (percolation). At 65 seconds, CLOSE the valve (immersion). OPEN the valve again at the end. Produces a perfectly balanced extraction.\n\nFlavor Profile: Very sweet, a unique blend of V60 clarity and immersion body."
missing["desc_key_7"] = "Medium grind. Pour water first, then add the coffee grounds. Stir after a few moments, then let it steep.\n\nFlavor Profile: Full body, very balanced flavor, and minimal risk of over-extraction."
missing["desc_key_8"] = "Medium grind (does not need to be too coarse). Brew for 4 minutes, then stir the coffee crust on the surface. Skim the foam. Wait another 5-8 minutes before pouring, and DO NOT press the plunger to the bottom.\n\nFlavor Profile: Full body yet very clean without grounds, thick texture, and balanced flavor."
missing["desc_key_0"] = "Use water at 99°C and a medium-fine grind. Create a divot in the center of the coffee bed. Swirl the brewer during the bloom phase and after the final pour to ensure even extraction.\n\nEstimated Flavor Profile: Balanced extraction, optimal sweetness, and high clarity."
missing["desc_key_1"] = "Use a coarse grind and 90-92°C water. Allow the bed to dry completely before proceeding to the next pour. The first 40% of the water influences acidity and sweetness, and the remaining 60% controls the strength.\n\nFlavor Profile: Clean cup, bright acidity, with a light, tea-like body."
missing["desc_key_2"] = "Medium-fine grind. Water at 90-92°C. Pour water very slowly, only in a coin-sized area in the center. DO NOT let the water touch the filter paper. Keep the coffee dome intact.\n\nEstimated Flavor Profile: Very sweet (maximum sweetness), with a smooth and rich body, and muted acidity."
missing["desc_key_3"] = "Use a low temperature (around 90°C) and a coarse grind. Pour slowly in a circular motion without vigorous agitation. A flat-bed dripper is recommended.\n\nFlavor Profile: Very bright acidity, a clean cup, and prominent fruity notes."
missing["desc_key_4"] = "Make a divot in the center. Use a high temperature. Perform a 'Rao Spin' (swirl the dripper in a circular motion) after the bloom and at the end to level the coffee bed and prevent channeling.\n\nEstimated Taste: Balanced extraction (high extraction yield), sweet, minimal astringency."

all_trans = {**ui_translations, **trans_new, **missing}

# Fix calib_title which had an error in my string map above
if 'calib_title' in all_trans and all_trans['calib_title'].startswith('Brewing Equipment'):
    all_trans['calib_title'] = "Brewing Equipment & Flow Rate Calibration"
all_trans['stop_metronome'] = "Stop Metronome"

output_lines = []
for line in id_text.split('\n'):
    m = re.search(r"^(\s*'([^']+)': ')(.*)(',)$", line)
    if m:
        prefix = m.group(1)
        key = m.group(2)
        suffix = m.group(4)
        if key in all_trans:
            val = all_trans[key]
            safe_val = val.replace("'", "\\'")
            safe_val = safe_val.replace('\n', '\\n')
            output_lines.append(f"{prefix}{safe_val}{suffix}")
        else:
            output_lines.append(line)
    else:
        output_lines.append(line)

new_en_text = '\n'.join(output_lines)
new_content = content.replace(en_text, new_en_text)

with open("lib/core/app_strings.dart", "w", encoding="utf-8") as f:
    f.write(new_content)

print("Applied final comprehensive UI translations to app_strings.dart")
