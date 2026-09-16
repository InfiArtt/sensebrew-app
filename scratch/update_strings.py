import re

with open('lib/core/app_strings.dart', 'r', encoding='utf-8') as f:
    text = f.read()

id_strings = """
      'pour_calc_title': 'Kalkulator Tuang',
      'pour_calc_desc': 'Alat bantu tuang bebas. Masukkan jumlah air (ml) yang ingin dituang, aplikasi akan menghitung dan memandu waktunya berdasarkan kalibrasi teko Anda.',
      'pour_calc_target': 'Target Tuangan (ml)',
      'pour_calc_est': 'Estimasi Waktu: {0} detik',
      'pour_calc_start': 'Mulai Tuang',
      'pour_calc_stop': 'Berhenti',
      'pour_calc_ready': 'Siap-siap, tuang dalam',
"""

en_strings = """
      'pour_calc_title': 'Pour Calculator',
      'pour_calc_desc': 'Free pour helper. Enter the target amount of water (ml), and the app will calculate and guide the pour time based on your kettle calibration.',
      'pour_calc_target': 'Target Pour (ml)',
      'pour_calc_est': 'Estimated Time: {0} seconds',
      'pour_calc_start': 'Start Pouring',
      'pour_calc_stop': 'Stop',
      'pour_calc_ready': 'Get ready to pour in',
"""

text = text.replace("'save_success': 'Kalibrasi berhasil disimpan.',", "'save_success': 'Kalibrasi berhasil disimpan.',\n" + id_strings)
text = text.replace("'save_success': 'Calibration saved successfully.',", "'save_success': 'Calibration saved successfully.',\n" + en_strings)

with open('lib/core/app_strings.dart', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated app_strings.dart")
