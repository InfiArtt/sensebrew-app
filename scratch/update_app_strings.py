import re

with open('lib/core/app_strings.dart', 'r', encoding='utf-8') as f:
    content = f.read()

id_keys = """
      'calib_guide': 'Panduan Kalibrasi:\\n1. Siapkan teko kopi (berisi air) dan timbangan atau gelas takar.\\n2. Aktifkan tombol \\'Simulasi Metronom\\' di bawah.\\n3. Setelah aba-aba \\'Mulai\\', mulailah menuang air seperti biasa.\\n4. Hitung ada berapa bunyi \\'TIK\\' yang terdengar sampai air mencapai target ml yang kamu mau.\\n5. Coba tuang sambil memutar teko (tuang melingkar), lalu hitung butuh berapa \\'TIK\\' untuk menyelesaikan 1 putaran penuh.\\n6. Masukkan angka-angka tadi ke dalam kolom di bawah!',
      'calib_header': 'Alat Seduh & Kalibrasi',
      'calib_q1': 'Berapa ml air target tuanganmu tadi?',
      'calib_q2': 'Butuh berapa TIK untuk mencapai target ml itu?',
      'calib_q3': 'Butuh berapa TIK untuk 1 putaran tuang melingkar?',
      'calib_grinder_select': 'Pilih Grinder Kopimu:',
      'calib_grinder_title': 'Pilih Grinder',
      'calib_grinder_manual': 'Grinder Manual',
      'calib_grinder_electric': 'Grinder Elektrik',
      'calib_spoon_q': 'Berapa gram kapasitas sendok takar kopimu?',
      'calib_sim_btn': 'Simulasi Metronom (Mainkan Hitung Mundur)',
      
      'ai_greet_edit': "Halo! Aku lihat kamu sedang mengedit resep '{0}'. Ada yang mau diubah?",
      'ai_greet_new': "Halo! Mau meracik resep seduhan seperti apa hari ini?",
      'ai_error_general': "Maaf, terjadi kesalahan saat memproses permintaanmu.",
      'ai_hint': "Ketik pesan...",
      'ai_voice_note': "🎤 [Pesan Suara]",
      'ai_apply_btn': "Terapkan ke Form",
      'ai_send_label': "Kirim pesan teks",
      'ai_record_start_label': "Mulai rekam suara",
      'ai_record_stop_label': "Hentikan rekaman",
      'ai_coffee': "Kopi",
      'ai_water': "Air",
      'ai_time': "Waktu",
      
      'tts_preview_btn': "Coba Dengarkan Suara",
      'tts_preview_text': "Ini adalah contoh suara dari pengaturan saat ini.",
      
      'action_swirl': 'Swirl / Goyang Alat',
      'action_cap': 'Pasang Tutup',
      'action_flip': 'Balikkan Alat',
      
      'ai_chat_title': 'Rancang Bersama AI',
"""

en_keys = """
      'calib_guide': 'Calibration Guide:\\n1. Prepare a coffee kettle (with water) and a scale or measuring cup.\\n2. Activate the \\'Metronome Simulation\\' button below.\\n3. After the \\'Start\\' cue, begin pouring water normally.\\n4. Count how many \\'TICK\\' sounds you hear until the water reaches your target ml.\\n5. Try pouring while moving the kettle in a circle, and count how many \\'TICKs\\' it takes to complete 1 full rotation.\\n6. Enter those numbers into the fields below!',
      'calib_header': 'Equipment & Calibration',
      'calib_q1': 'What was your target water volume (ml)?',
      'calib_q2': 'How many TICKs to reach that target ml?',
      'calib_q3': 'How many TICKs for 1 full circular pour?',
      'calib_grinder_select': 'Select Your Coffee Grinder:',
      'calib_grinder_title': 'Select Grinder',
      'calib_grinder_manual': 'Manual Grinder',
      'calib_grinder_electric': 'Electric Grinder',
      'calib_spoon_q': 'How many grams does your measuring spoon hold?',
      'calib_sim_btn': 'Metronome Simulation (Play Countdown)',
      
      'ai_greet_edit': "Hi! I see you're editing the '{0}' recipe. What would you like to change?",
      'ai_greet_new': "Hi! What kind of brew recipe would you like to create today?",
      'ai_error_general': "Sorry, an error occurred while processing your request.",
      'ai_hint': "Type a message...",
      'ai_voice_note': "🎤 [Voice Note]",
      'ai_apply_btn': "Apply to Form",
      'ai_send_label': "Send text message",
      'ai_record_start_label': "Start voice recording",
      'ai_record_stop_label': "Stop recording",
      'ai_coffee': "Coffee",
      'ai_water': "Water",
      'ai_time': "Time",
      
      'tts_preview_btn': "Preview Voice",
      'tts_preview_text': "This is a voice sample with your current settings.",
      
      'action_swirl': 'Swirl Brewer',
      'action_cap': 'Attach Cap',
      'action_flip': 'Flip Brewer',
      
      'ai_chat_title': 'Design with AI',
"""

# Insert into 'id': { block
content = re.sub(
    r"('id':\s*\{)",
    r"\1\n" + id_keys,
    content
)

# Insert into 'en': { block
content = re.sub(
    r"('en':\s*\{)",
    r"\1\n" + en_keys,
    content
)

with open('lib/core/app_strings.dart', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated app_strings.dart")
