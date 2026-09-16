import os

strings_file = "lib/core/app_strings.dart"
with open(strings_file, 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace(
    "'calibrate_flow_rate': 'Pengaturan Alat & Kalibrasi',",
    "'calibrate_flow_rate': 'Kalibrasi Flow Rate',"
)
text = text.replace(
    "'calibrate_flow_rate': 'Device Settings & Calibration',",
    "'calibrate_flow_rate': 'Calibrate Flow Rate',"
)
# Also change the menu headers inside the calibration screen if they exist
text = text.replace(
    "'calib_header': 'Alat Seduh & Kalibrasi',",
    "'calib_header': 'Kalibrasi Flow Rate',"
)
text = text.replace(
    "'calib_header': 'Brewing Device & Calibration',",
    "'calib_header': 'Calibration',"
)
text = text.replace(
    "'calib_title': 'Kalibrasi Alat',",
    "'calib_title': 'Kalibrasi',"
)
text = text.replace(
    "'calib_title': 'Device Calibration',",
    "'calib_title': 'Calibration',"
)

with open(strings_file, 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated menu titles to original wording successfully.")
