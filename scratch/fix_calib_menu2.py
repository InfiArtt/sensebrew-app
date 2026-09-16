import os

strings_file = "lib/core/app_strings.dart"
with open(strings_file, 'r', encoding='utf-8') as f:
    text = f.read()

# Update ID
text = text.replace(
    "'calibrate_flow_rate': 'Kalibrasi Flow Rate',",
    "'calibrate_flow_rate': 'Pengaturan Alat Seduh dan Kalibrasi Debit Air',"
)
text = text.replace(
    "'calib_header': 'Kalibrasi Flow Rate',",
    "'calib_header': 'Pengaturan Alat Seduh dan Kalibrasi Debit Air',"
)
text = text.replace(
    "'calib_title': 'Kalibrasi',",
    "'calib_title': 'Pengaturan Alat Seduh dan Kalibrasi Debit Air',"
)

# Update EN
text = text.replace(
    "'calibrate_flow_rate': 'Calibrate Flow Rate',",
    "'calibrate_flow_rate': 'Brewing Equipment & Flow Rate Calibration',"
)
text = text.replace(
    "'calib_header': 'Calibration',",
    "'calib_header': 'Brewing Equipment & Flow Rate Calibration',"
)
text = text.replace(
    "'calib_title': 'Calibration',",
    "'calib_title': 'Brewing Equipment & Flow Rate Calibration',"
)

with open(strings_file, 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated menu titles to Equipment and specific Indonesian translation successfully.")
