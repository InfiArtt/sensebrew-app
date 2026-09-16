import os

strings_file = "lib/core/app_strings.dart"
with open(strings_file, 'r', encoding='utf-8') as f:
    text = f.read()

# ID
text = text.replace(
    "'calib_q1': 'Berapa gram/ml air hasil tuanganmu tadi?',", 
    "'calib_q1': '1. Berapa ml gelas takar yang kamu gunakan?',"
)
text = text.replace(
    "'calib_q2': 'Butuh berapa TIK untuk mencapai hasil tersebut?',", 
    "'calib_q2': '2. Nyalakan metronom lalu tuang air. Berapa detik/ketukan yang dibutuhkan sampai gelas penuh?',"
)
text = text.replace(
    "'calib_q3': 'Butuh berapa TIK untuk 1 putaran tuang melingkar?',", 
    "'calib_q3': '3. Biasanya kamu butuh berapa detik untuk 1 putaran penuh saat menuang melingkar?',"
)

# EN
text = text.replace(
    "'calib_q1': 'How many grams/ml of water did you pour?',", 
    "'calib_q1': '1. What is the volume of your measuring cup in ml?',"
)
text = text.replace(
    "'calib_q2': 'How many TICKs did it take to reach that amount?',", 
    "'calib_q2': '2. Turn on the metronome, then pour water. How many seconds (beats) does it take to fill the cup?',"
)
text = text.replace(
    "'calib_q3': 'How many TICKs for 1 circular pour rotation?',", 
    "'calib_q3': '3. Typically, how many seconds do you need to complete 1 full circle rotation (spiral) when pouring?',"
)

with open(strings_file, 'w', encoding='utf-8') as f:
    f.write(text)

print("Reverted calib_q1, calib_q2, calib_q3 to original wording successfully.")
