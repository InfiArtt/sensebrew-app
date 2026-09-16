import json
import re

with open("id_data.json", "r", encoding="utf-8") as f:
    id_data = json.load(f)

with open("translated_new.json", "r", encoding="utf-8") as f:
    trans_new = json.load(f)

trans_new["desc_key_5"] = "Classic Hario factory recipe. Very beginner-friendly. Pour slowly in a circular motion from the center outwards, then back to the center.\n\nFlavor Profile: Classic, medium body, prominent acidity, and strong brewing aroma."
trans_new["desc_key_6"] = "God Recipe by Tetsu Kasuya. Temperature 90°C. OPEN the valve at the start (percolation). At 65 seconds, CLOSE the valve (immersion). OPEN the valve again at the end. Produces a perfectly balanced extraction.\n\nFlavor Profile: Very sweet, a unique blend of V60 clarity and immersion body."
trans_new["desc_key_7"] = "Medium grind. Pour water first, then add the coffee grounds. Stir after a few moments, then let it steep.\n\nFlavor Profile: Full body, very balanced flavor, and minimal risk of over-extraction."
trans_new["desc_key_8"] = "Medium grind (does not need to be too coarse). Brew for 4 minutes, then stir the coffee crust on the surface. Skim the foam. Wait another 5-8 minutes before pouring, and DO NOT press the plunger to the bottom.\n\nFlavor Profile: Full body yet very clean without grounds, thick texture, and balanced flavor."

trans_new["desc_key_0"] = "Use water at 99°C and a medium-fine grind. Create a divot in the center of the coffee bed. Swirl the brewer during the bloom phase and after the final pour to ensure even extraction.\n\nEstimated Flavor Profile: Balanced extraction, optimal sweetness, and high clarity."
trans_new["desc_key_1"] = "Use a coarse grind and 90-92°C water. Allow the bed to dry completely before proceeding to the next pour. The first 40% of the water influences acidity and sweetness, and the remaining 60% controls the strength.\n\nFlavor Profile: Clean cup, bright acidity, with a light, tea-like body."
trans_new["desc_key_2"] = "Medium-fine grind. Water at 90-92°C. Pour water very slowly, only in a coin-sized area in the center. DO NOT let the water touch the filter paper. Keep the coffee dome intact.\n\nEstimated Flavor Profile: Very sweet (maximum sweetness), with a smooth and rich body, and muted acidity."
trans_new["desc_key_3"] = "Use a low temperature (around 90°C) and a coarse grind. Pour slowly in a circular motion without vigorous agitation. A flat-bed dripper is recommended.\n\nFlavor Profile: Very bright acidity, a clean cup, and prominent fruity notes."
trans_new["desc_key_4"] = "Make a divot in the center. Use a high temperature. Perform a 'Rao Spin' (swirl the dripper in a circular motion) after the bloom and at the end to level the coffee bed and prevent channeling.\n\nEstimated Taste: Balanced extraction (high extraction yield), sweet, minimal astringency."

with open("lib/core/app_strings.dart", "r", encoding="utf-8") as f:
    content = f.read()

en_block_match = re.search(r"('en': \{)(.*?)(\n    \},)", content, re.DOTALL)
if not en_block_match:
    print("EN block not found!")
    exit(1)

en_text = en_block_match.group(2)

id_block_match = re.search(r"('id': \{)(.*?)(\n    \},)", content, re.DOTALL)
id_text = id_block_match.group(2)

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
    'tts_speed_changed': 'Speed changed to {0}'
}

all_trans = {**ui_translations, **trans_new}

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

print("Restored and updated app_strings.dart!")
