import os

strings_file = "lib/core/app_strings.dart"
with open(strings_file, 'r', encoding='utf-8') as f:
    text = f.read()

# ID
text = text.replace(
    "'calib_q1': '1. Berapa ml gelas takar yang kamu gunakan?',", 
    "'calib_q1': 'Berapa ml/gram gelas takar atau target tuanganmu?',"
)
text = text.replace(
    "'calib_q2': '2. Nyalakan metronom lalu tuang air. Berapa detik/ketukan yang dibutuhkan sampai gelas penuh?',", 
    "'calib_q2': 'Nyalakan metronom lalu tuang air. Berapa detik/ketukan yang dibutuhkan sampai target tercapai?',"
)
text = text.replace(
    "'calib_q3': '3. Biasanya kamu butuh berapa detik untuk 1 putaran penuh saat menuang melingkar?',", 
    "'calib_q3': 'Biasanya kamu butuh berapa detik untuk 1 putaran penuh saat menuang melingkar?',"
)

# EN
text = text.replace(
    "'calib_q1': '1. What is the volume of your measuring cup in ml?',", 
    "'calib_q1': 'What is the volume/weight of your measuring cup or target in ml/grams?',"
)
text = text.replace(
    "'calib_q2': '2. Turn on the metronome, then pour water. How many seconds (beats) does it take to fill the cup?',", 
    "'calib_q2': 'Turn on the metronome, then pour water. How many seconds (beats) does it take to reach the target?',"
)
text = text.replace(
    "'calib_q3': '3. Typically, how many seconds do you need to complete 1 full circle rotation (spiral) when pouring?',", 
    "'calib_q3': 'Typically, how many seconds do you need to complete 1 full circle rotation (spiral) when pouring?',"
)

with open(strings_file, 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated calib_q1, calib_q2, calib_q3 successfully.")
