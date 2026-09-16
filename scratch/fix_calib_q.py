import os

strings_file = "lib/core/app_strings.dart"
with open(strings_file, 'r', encoding='utf-8') as f:
    text = f.read()

# ID
text = text.replace("'calib_q1': 'Berapa ml air target tuanganmu tadi?',", "'calib_q1': 'Berapa gram/ml air hasil tuanganmu tadi?',")
text = text.replace("'calib_q2': 'Butuh berapa TIK untuk mencapai target ml itu?',", "'calib_q2': 'Butuh berapa TIK untuk mencapai hasil tersebut?',")

# EN
text = text.replace("'calib_q1': 'What was your target water volume in ml?',", "'calib_q1': 'How many grams/ml of water did you pour?',")
text = text.replace("'calib_q2': 'How many TICKs to reach that target volume?',", "'calib_q2': 'How many TICKs did it take to reach that amount?',")

with open(strings_file, 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated calib_q1 and calib_q2 successfully.")
