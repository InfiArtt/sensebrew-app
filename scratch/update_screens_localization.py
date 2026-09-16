import re

def replace_in_file(filepath, replacements):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    for old_str, new_str in replacements:
        content = content.replace(old_str, new_str)
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

# 1. calibration_screen.dart
replace_in_file('lib/screens/calibration_screen.dart', [
    (
        "title: Text(lang == 'en' ? 'Calibration & Equipment' : 'Alat Seduh & Kalibrasi'),",
        "title: Text(AppStrings.str(lang, 'calib_header')),"
    ),
    (
        "lang == 'en' ? \n              \"Calibration Guide:\\n1. Prepare a kettle with water and a scale (or measuring cup).\\n2. Tap the 'Simulasi Metronom' button below.\\n3. Listen to the countdown: 3, 2, 1, START.\\n4. Pour exactly at the word START.\\n5. Count how many TICK sounds you hear until the scale reaches your target volume (or the cup is full).\\n6. Also count how many TICKs you need for one full spiral rotation.\\n7. Enter those TICK numbers in the form below.\" :\n              \"Panduan Kalibrasi:\\n1. Siapkan teko berisi air dan Timbangan (atau Gelas Takar).\\n2. Tekan tombol 'Simulasi Metronom' di bawah ini.\\n3. Dengarkan hitung mundur: 3, 2, 1, MULAI.\\n4. Tepat pada kata MULAI, mulailah menuang air.\\n5. Hitung berapa banyak TIK yang Anda dengar hingga air di timbangan mencapai target (atau hingga gelas takar penuh).\\n6. Hitung juga berapa TIK yang Anda butuhkan untuk memutar teko satu lingkaran penuh.\\n7. Masukkan jumlah TIK tersebut ke form di bawah.\"",
        "AppStrings.str(lang, 'calib_guide')"
    ),
    (
        "lang == 'en' ? 'Metronome Simulation' : 'Simulasi Metronom (Mainkan Hitung Mundur)'",
        "AppStrings.str(lang, 'calib_sim_btn')"
    ),
    (
        "lang == 'en' ? 'Select your Coffee Grinder:' : 'Pilih Grinder Kopimu:'",
        "AppStrings.str(lang, 'calib_grinder_select')"
    ),
    (
        "lang == 'en' ? 'Select Grinder' : 'Pilih Grinder'",
        "AppStrings.str(lang, 'calib_grinder_title')"
    ),
    (
        "lang == 'en' ? 'Manual Grinder' : 'Grinder Manual'",
        "AppStrings.str(lang, 'calib_grinder_manual')"
    ),
    (
        "lang == 'en' ? 'Electric Grinder' : 'Grinder Elektrik'",
        "AppStrings.str(lang, 'calib_grinder_electric')"
    ),
    (
        "lang == 'en' ? 'How many grams does your measuring spoon hold?' : 'Berapa gram kapasitas sendok takar kopimu?'",
        "AppStrings.str(lang, 'calib_spoon_q')"
    )
])

# 2. ai_chat_screen.dart
replace_in_file('lib/screens/ai_chat_screen.dart', [
    (
        "import '../core/ai_service.dart';",
        "import '../core/ai_service.dart';\nimport '../core/app_strings.dart';"
    ),
    (
        """    _messages.add({
      'role': 'ai',
      'text': widget.initialRecipe != null 
          ? "Halo! Aku lihat kamu sedang mengedit resep '${widget.initialRecipe!.name}'. Ada yang mau diubah?"
          : "Halo! Mau meracik resep V60 seperti apa hari ini?",
    });""",
        """    final lang = Provider.of<SettingsState>(context, listen: false).appLanguage;
    _messages.add({
      'role': 'ai',
      'text': widget.initialRecipe != null 
          ? AppStrings.str(lang, 'ai_greet_edit', [widget.initialRecipe!.name])
          : AppStrings.str(lang, 'ai_greet_new'),
    });"""
    ),
    (
        "_messages.add({'role': 'user', 'text': '🎤 [Voice Note]'});",
        """final lang = Provider.of<SettingsState>(context, listen: false).appLanguage;
        _messages.add({'role': 'user', 'text': AppStrings.str(lang, 'ai_voice_note')});"""
    ),
    (
        "aiResponse.chatMessage + \"\\n\\n(Kopi: ${_currentDraft!.coffeeGrams}g, Air: ${_currentDraft!.totalWaterMl}ml, Waktu: ${_currentDraft!.totalDurationSeconds}s)\"",
        "aiResponse.chatMessage + \"\\n\\n(\" + AppStrings.str(lang, 'ai_coffee') + \": ${_currentDraft!.coffeeGrams}g, \" + AppStrings.str(lang, 'ai_water') + \": ${_currentDraft!.totalWaterMl}ml, \" + AppStrings.str(lang, 'ai_time') + \": ${_currentDraft!.totalDurationSeconds}s)\""
    ),
    (
        "_messages.add({'role': 'ai', 'text': \"Maaf, terjadi kesalahan saat memproses permintaanmu.\"});",
        "_messages.add({'role': 'ai', 'text': AppStrings.str(lang, 'ai_error_general')});"
    ),
    (
        "title: const Text('Rancang Bersama AI'),",
        "title: Text(AppStrings.str(Provider.of<SettingsState>(context).appLanguage, 'ai_chat_title')),"
    ),
    (
        "child: const Text(\"Terapkan ke Form\"),",
        "child: Text(AppStrings.str(Provider.of<SettingsState>(context, listen: false).appLanguage, 'ai_apply_btn')),"
    ),
    (
        "hintText: 'Ketik pesan...',",
        "hintText: AppStrings.str(Provider.of<SettingsState>(context).appLanguage, 'ai_hint'),"
    ),
    (
        "label: \"Kirim pesan teks\",",
        "label: AppStrings.str(Provider.of<SettingsState>(context).appLanguage, 'ai_send_label'),"
    ),
    (
        "label: _isRecording ? \"Hentikan rekaman\" : \"Mulai rekam suara\",",
        "label: _isRecording ? AppStrings.str(Provider.of<SettingsState>(context).appLanguage, 'ai_record_stop_label') : AppStrings.str(Provider.of<SettingsState>(context).appLanguage, 'ai_record_start_label'),"
    )
])

# 3. custom_recipe_screen.dart
replace_in_file('lib/screens/custom_recipe_screen.dart', [
    (
        "case PhaseAction.swirl: return lang == 'en' ? 'Swirl Brewer' : 'Swirl/Goyang Alat Seduh';",
        "case PhaseAction.swirl: return AppStrings.str(lang, 'action_swirl');"
    ),
    (
        "case PhaseAction.cap: return lang == 'en' ? 'Attach Cap' : 'Pasang Tutup';",
        "case PhaseAction.cap: return AppStrings.str(lang, 'action_cap');"
    ),
    (
        "case PhaseAction.flip: return lang == 'en' ? 'Flip Aeropress' : 'Balikkan Alat';",
        "case PhaseAction.flip: return AppStrings.str(lang, 'action_flip');"
    )
])

# 4. ai_service.dart
replace_in_file('lib/core/ai_service.dart', [
    (
        "1. \"chatMessage\": A friendly, conversational response to the user explaining what you just did (in Indonesian). Be casual, luwes, and warm (e.g. \"Tentu! Aku udah ganti gilingannya jadi lebih kasar nih...\").",
        "1. \"chatMessage\": A friendly, conversational response to the user explaining what you just did (in ${lang == 'en' ? 'English' : 'Indonesian'}). Be casual, luwes, and warm."
    ),
    (
        "final String chatMessage = data['chatMessage'] as String? ?? \"Ini draf resepnya!\";",
        "final String chatMessage = data['chatMessage'] as String? ?? (lang == 'en' ? \"Here is the draft!\" : \"Ini draf resepnya!\");"
    )
])

print("Updated screens with localization.")
