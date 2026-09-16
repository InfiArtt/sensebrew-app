import re

with open('lib/core/app_strings.dart', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove the OLD calib_q1, calib_q2, calib_q3 which look like:
# 'calib_q1': 'Target Air di Timbangan / Ukuran Gelas Takar (ml)',
# 'calib_q2': 'Jumlah TIK untuk menuang air tersebut',
# 'calib_q3': 'Jumlah TIK untuk 1 putaran penuh',
# And the English versions:
# 'calib_q1': 'Target Water on Scale / Measuring Cup Volume (ml)',
# 'calib_q2': 'Number of TICKs to pour that amount',
# 'calib_q3': 'Number of TICKs for 1 full rotation',

content = re.sub(r"\s*'calib_q1': 'Target Air di Timbangan / Ukuran Gelas Takar \(ml\)',\n", "", content)
content = re.sub(r"\s*'calib_q2': 'Jumlah TIK untuk menuang air tersebut',\n", "", content)
content = re.sub(r"\s*'calib_q3': 'Jumlah TIK untuk 1 putaran penuh',\n", "", content)

content = re.sub(r"\s*'calib_q1': 'Target Water on Scale / Measuring Cup Volume \(ml\)',\n", "", content)
content = re.sub(r"\s*'calib_q2': 'Number of TICKs to pour that amount',\n", "", content)
content = re.sub(r"\s*'calib_q3': 'Number of TICKs for 1 full rotation',\n", "", content)

with open('lib/core/app_strings.dart', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed duplicate keys!")
