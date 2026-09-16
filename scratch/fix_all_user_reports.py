import re
import json

# 1. FIX TIMER STATE
with open('lib/core/timer_state.dart', 'r', encoding='utf-8') as f:
    ts = f.read()
ts = ts.replace('AndroidContentType.sonification', 'AndroidContentType.speech')
with open('lib/core/timer_state.dart', 'w', encoding='utf-8') as f:
    f.write(ts)


# 2. FIX SETTINGS SCREEN (API KEY VISIBILITY)
with open('lib/screens/settings_screen.dart', 'r', encoding='utf-8') as f:
    ss = f.read()

# We need to add state variables if they don't exist
if '_isGeminiObscured' not in ss:
    ss = ss.replace('class _SettingsScreenState extends State<SettingsScreen> {',
                    'class _SettingsScreenState extends State<SettingsScreen> {\n  bool _isGeminiObscured = true;\n  bool _isGroqObscured = true;')

# Add suffixIcon to Gemini
if 'suffixIcon' not in ss.split('controller: _geminiController')[1].split('obscureText')[0]:
    ss = re.sub(
        r"(controller: _geminiController,\s*decoration: const InputDecoration\()",
        r"\1\n                    suffixIcon: IconButton(icon: Icon(_isGeminiObscured ? Icons.visibility : Icons.visibility_off), onPressed: () { setState(() { _isGeminiObscured = !_isGeminiObscured; }); }),",
        ss
    )
    # Also remove the 'const' from decoration because suffixIcon uses variables
    ss = re.sub(r"decoration: const InputDecoration\(\s*labelText: 'Google Gemini API Key',", r"decoration: InputDecoration(\n                    labelText: 'Google Gemini API Key',", ss)
    ss = re.sub(r"(controller: _geminiController,[\s\S]*?)obscureText: true,", r"\1obscureText: _isGeminiObscured,", ss)

# Add suffixIcon to Groq
if 'suffixIcon' not in ss.split('controller: _groqController')[1].split('obscureText')[0]:
    ss = re.sub(
        r"(controller: _groqController,\s*decoration: const InputDecoration\()",
        r"\1\n                    suffixIcon: IconButton(icon: Icon(_isGroqObscured ? Icons.visibility : Icons.visibility_off), onPressed: () { setState(() { _isGroqObscured = !_isGroqObscured; }); }),",
        ss
    )
    ss = re.sub(r"decoration: const InputDecoration\(\s*labelText: 'Groq API Key',", r"decoration: InputDecoration(\n                    labelText: 'Groq API Key',", ss)
    ss = re.sub(r"(controller: _groqController,[\s\S]*?)obscureText: true,", r"\1obscureText: _isGroqObscured,", ss)

with open('lib/screens/settings_screen.dart', 'w', encoding='utf-8') as f:
    f.write(ss)


# 3. FIX ENGLISH UI STRINGS
en_dict = {
    "brew_dose": "Coffee Dose: {0} scoops",
    "brew_grind": "Grind Size",
    "brew_bean": "Coffee Bean Type",
    "brew_extra": "Extra Ingredients",
    "brew_desc_title": "Recipe Description:",
    "rotations_half": " and a half",
    "custom_grind_400": "Very Fine (Espresso)",
    "custom_grind_600": "Fine (Aeropress)",
    "custom_grind_800": "Medium (V60 / Kalita)",
    "custom_grind_1000": "Medium Coarse (Chemex)",
    "custom_grind_1200": "Coarse (French Press / Switch)",
    "custom_grind_1400": "Very Coarse (Cold Brew)",
    "custom_bean_blend": "Blend",
    "custom_bean_bebas": "Any Bean",
    "custom_recipe_desc": "Recipe Description",
    "custom_recipe_extra_hint": "E.g: 15 ml condensed milk, 100 g ice cubes",
    "home_select_method": "Select Brew Method:",
    "method_v60_desc": "Pour-over brewing with spiral pours",
    "method_fp_desc": "Immersion brewing without grounds",
    "method_ap_desc": "Press brewing using air pressure",
    "method_vd_desc": "Slow drip brewing (Milk Coffee)",
    "method_cup_desc": "International coffee evaluation standard",
    "calib_guide": "Calibration Guide:\n1. Prepare a kettle with water and a scale or measuring cup.\n2. Activate the Metronome Simulation button below.\n3. After the start cue, pour water as usual.\n4. Count how many TICK sounds you hear until the water reaches your target volume.\n5. Try pouring in a circle, and count how many TICK sounds it takes to complete one full rotation.\n6. Enter those numbers into the fields below!",
    "calib_header": "Brewing Device & Calibration",
    "calib_q1": "What was your target water volume in ml?",
    "calib_q2": "How many TICKs to reach that target volume?",
    "calib_q3": "How many TICKs for 1 circular pour rotation?",
    "calib_grinder_select": "Select Your Grinder:",
    "calib_grinder_title": "Select Grinder",
    "calib_grinder_manual": "Manual Grinder",
    "calib_grinder_electric": "Electric Grinder",
    "calib_spoon_q": "What is the capacity of your measuring scoop in grams?",
    "calib_sim_btn": "Metronome Simulation (Play Countdown)",
    "action_swirl": "Swirl Device",
    "action_cap": "Attach Cap",
    "action_flip": "Flip Device",
    "ai_chat_title": "Design with AI",
    "app_title": "SenseBrew",
    "settings_menu": "App Settings Menu",
    "calibrate_flow_rate": "Device Settings & Calibration",
    "calibrated_status": "Device ready. Flow rate: {0} ml per second",
    "uncalibrated_status": "Flow rate not calibrated.",
    "calibrated_btn": "{0} ml/second",
    "uncalibrated_btn": "(Required)",
    "custom_recipe_btn": "Custom\nRecipe",
    "custom_recipe_label": "Create custom brewing recipe",
    "recipe_label": "Recipe {0}, Coffee {1} grams, Water {2} ml",
    "calib_title": "Device Calibration",
    "stop_metronome": "Stop Metronome",
    "start_metronome": "Play Metronome",
    "save_calib": "SAVE CALIBRATION",
    "save_calib_label": "Save calibration results",
    "save_success": "Calibration successfully saved.",
    "reduce": "Reduce to {0} {1}",
    "add": "Increase to {0} {1}",
    "custom_title": "Create Custom Recipe",
    "recipe_name": "Recipe Name",
    "recipe_note": "Notes & Brewing Rules",
    "coffee_grams": "Coffee (grams)",
    "total_water": "Total Water (milliliters)",
    "total_time": "Total Time (seconds)",
    "phases_title": "Brewing Phases",
    "start_sec": "Start at Second",
    "water_ml": "Water Amount (milliliters)",
    "add_phase": "Add Phase",
    "delete_phase": "Delete Phase",
    "save_recipe": "SAVE RECIPE",
    "pour": "Pour {0}.",
    "save_recipe_success": "Custom recipe successfully saved.",
    "brew_sec": "Second: {0}\n{1}",
    "brew_title": "Recipe {0}\nCoffee: {1} grams\nWater: {2} ml",
    "note_label": "Notes and brewing rules: {0}",
    "note": "Note: {0}",
    "brew_phases": "Brewing Phases:",
    "brew_phase_item_circle": "• Second {0}: Pour {1} ml ({2} rotations)",
    "brew_phase_item_center": "• Second {0}: Pour {1} ml ({2} seconds)",
    "brew_phase_item_stir": "• Second {0}: Stir",
    "brew_phase_item_press": "• Second {0}: Press",
    "brew_phase_item_wait": "• Second {0}: Wait",
    "start_brew_btn": "START BREWING",
    "start_brew_label": "Start brewing process",
    "cancel_brew_btn": "Cancel",
    "pour_circle_instruction": "Pour {0} milliliters, {1} rotations.",
    "pour_center_instruction": "Pour in the center {0} milliliters for {1} seconds.",
    "stir_instruction": "Stir.",
    "press_instruction": "Press slowly.",
    "open_valve_instruction": "Open switch or valve.",
    "close_valve_instruction": "Close switch or valve.",
    "pour_fast_instruction": "Pour {0} milliliters of water.",
    "wait_instruction": "Wait...",
    "cancel_brew_label": "Cancel brewing",
    "finish_brew_btn": "FINISH",
    "finish_brew_label": "Finish, return to main menu",
    "brew_complete": "Brewing time is complete. Enjoy your coffee!",
    "action_pour_circle": "Circular Pour",
    "action_pour_center": "Center Pour",
    "action_stir": "Stir",
    "action_wait": "Wait",
    "action_press": "Press",
    "action_openValve": "Open Switch",
    "action_closeValve": "Close Switch",
    "action_pourFast": "Fast Pour",
    "stop_pour": "Stop.",
    "settings_title": "Settings",
    "app_lang": "App Language",
    "app_lang_label": "Select App Language",
    "app_lang_desc": "Change application interface language",
    "gemini_title": "AI Provider",
    "gemini_desc": "To use the \"Create Recipe with AI\" feature, copy your API Key from Google AI Studio or Groq Console, and paste it below:",
    "gemini_help_title": "How to Get API Key",
    "gemini_help_content": "1. Open aistudio.google.com\n2. Log in with Google account.\n3. Click \"Get API key\" > \"Create API key\".\n4. Copy the code.\n\nNote: This service is free without a credit card.",
    "groq_help_content": "1. Open console.groq.com/keys\n2. Log in with your account.\n3. Click \"Create API Key\".\n4. Copy the code (usually starts with gsk_).\n\nNote: This service is free without a credit card.",
    "close": "Close",
    "ai_recipe_btn": "AI\nRecipe",
    "ai_recipe_label": "Create recipe automatically with AI",
    "ai_title": "Create Recipe with AI",
    "ai_prompt_label": "Describe your coffee or preferences",
    "ai_prompt_hint": "Example: Gayo Coffee, I like sweet fruity flavors and not too sour...",
    "ai_generate_btn": "CREATE RECIPE NOW",
    "ai_generating": "Thinking of the best recipe...",
    "ai_error_no_key": "API Key is empty. Please fill it in Settings first.",
    "ai_error_failed": "Failed to create recipe: {0}",
    "edit_btn": "Edit",
    "delete_btn": "Delete",
    "brew_btn": "Brew",
    "delete_confirm_title": "Delete Recipe?",
    "delete_confirm_desc": "Are you sure you want to delete the recipe {0}?",
    "tts_title": "Voice & Language (TTS)",
    "tts_enable": "Voice Instructions",
    "tts_enable_desc": "Turn off if you only want to hear the metronome",
    "tts_channel": "Audio Channel",
    "tts_channel_desc": "Select who will read the instructions",
    "tts_channel_app": "TTS",
    "tts_channel_sr": "Screen Reader",
    "tts_lang": "Voice Language",
    "tts_speed": "Voice Speed",
    "tts_pitch": "Voice Pitch",
    "tts_voice": "Voice Selection",
    "tts_voice_desc": "Available voices depend on your phone's engine",
    "tts_speed_changed": "Speed changed to {0}",
    "tts_pitch_changed": "Voice pitch changed",
    "tts_voice_changed": "Voice type changed",
    "tts_channel_changed": "Voice channel successfully changed",
    "default": "Default",
    "ai_greet_edit": "Hello! I see you are editing recipe '{0}'. What would you like to change?",
    "ai_greet_new": "Hello! What kind of coffee recipe would you like to brew today?",
    "ai_error_general": "Sorry, an error occurred while processing your request.",
    "ai_hint": "Type a message...",
    "ai_voice_note": "🎙️ [Voice Message]",
    "ai_apply_btn": "Apply to Form",
    "ai_send_label": "Send text message",
    "ai_record_start_label": "Start recording voice",
    "ai_record_stop_label": "Stop recording"
}

with open('lib/core/app_strings.dart', 'r', encoding='utf-8') as f:
    text = f.read()

# I will replace the incorrect indonesian keys in the EN block with the english ones
# The EN block is the last one.
parts = text.split('  static String str')
en_block = parts[0]

for k, v in en_dict.items():
    # Find "'k': '...'" and replace the value
    escaped_v = v.replace('\n', '\\n').replace("'", "\\'")
    
    # We must only replace in the EN block, which is the last portion of en_block.
    # The ID block is before the EN block.
    # We can split en_block by "'en': {"
    en_parts = en_block.split("'en': {")
    
    # Replace in en_parts[1]
    # We use regex to replace the exact key
    pattern = r"'" + k + r"':\s*'.*?'"
    replacement = f"'{k}': '{escaped_v}'"
    en_parts[1] = re.sub(pattern, replacement, en_parts[1])
    
    en_block = en_parts[0] + "'en': {" + en_parts[1]

new_text = en_block + '  static String str' + parts[1]

with open('lib/core/app_strings.dart', 'w', encoding='utf-8') as f:
    f.write(new_text)

print("ALL FIXED")
