import re

with open('lib/core/app_strings.dart', 'r', encoding='utf-8') as f:
    app_strings = f.read()

# INDONESIAN REPLACEMENTS
app_strings = app_strings.replace(
    "'calib_guide': 'Panduan Kalibrasi:\\n1. Siapkan teko kopi (berisi air) dan timbangan atau gelas takar.\\n2. Aktifkan tombol \\'Simulasi Metronom\\' di bawah.\\n3. Setelah aba-aba \\'Mulai\\', mulailah menuang air seperti biasa.\\n4. Hitung ada berapa bunyi \\'TIK\\' yang terdengar sampai air mencapai target ml yang kamu mau.\\n5. Coba tuang sambil memutar teko (tuang melingkar), lalu hitung butuh berapa \\'TIK\\' untuk menyelesaikan 1 putaran penuh.\\n6. Masukkan angka-angka tadi ke dalam kolom di bawah!',",
    "'calib_guide': 'Panduan Kalibrasi:\\n1. Siapkan teko kopi berisi air, dan timbangan atau gelas takar.\\n2. Aktifkan tombol Simulasi Metronom di bawah.\\n3. Setelah aba-aba mulai, tuang air seperti biasa.\\n4. Hitung ada berapa bunyi TIK yang terdengar sampai air mencapai target mililiter yang kamu inginkan.\\n5. Coba tuang sambil memutar teko, lalu hitung butuh berapa bunyi TIK untuk menyelesaikan satu putaran penuh.\\n6. Masukkan angka-angka tersebut ke dalam kolom di bawah!',"
)

app_strings = app_strings.replace(
    "'calib_q1': 'Target Air di Timbangan / Ukuran Gelas Takar (ml)',",
    "'calib_q1': 'Target Air di Timbangan atau Gelas Takar dalam mililiter',"
)

app_strings = app_strings.replace(
    "'total_water': 'Total Water (ml)',",
    "'total_water': 'Total Water (milliliters)',"
)
app_strings = app_strings.replace(
    "'total_water': 'Total Air (ml)',",
    "'total_water': 'Total Air (mililiter)',"
)

app_strings = app_strings.replace(
    "'water_ml': 'Jumlah Air (ml)',",
    "'water_ml': 'Jumlah Air (mililiter)',"
)
app_strings = app_strings.replace(
    "'water_ml': 'Water Amount (ml)',",
    "'water_ml': 'Water Amount (milliliters)',"
)


# ENGLISH REPLACEMENTS
app_strings = app_strings.replace(
    "'calib_guide': 'Calibration Guide:\\n1. Prepare a coffee kettle (with water) and a scale or measuring cup.\\n2. Activate the \\'Metronome Simulation\\' button below.\\n3. After the \\'Start\\' cue, begin pouring water normally.\\n4. Count how many \\'TICK\\' sounds you hear until the water reaches your target ml.\\n5. Try pouring while moving the kettle in a circle, and count how many \\'TICKs\\' it takes to complete 1 full rotation.\\n6. Enter those numbers into the fields below!',",
    "'calib_guide': 'Calibration Guide:\\n1. Prepare a coffee kettle with water, and a scale or measuring cup.\\n2. Activate the Metronome Simulation button below.\\n3. After the start cue, begin pouring water normally.\\n4. Count how many TICK sounds you hear until the water reaches your target milliliters.\\n5. Try pouring while moving the kettle in a circle, and count how many TICKs it takes to complete one full rotation.\\n6. Enter those numbers into the fields below!',"
)

app_strings = app_strings.replace(
    "'calib_q1': 'What was your target water volume (ml)?',",
    "'calib_q1': 'What was your target water volume in milliliters?',"
)

with open('lib/core/app_strings.dart', 'w', encoding='utf-8') as f:
    f.write(app_strings)

print("Fixed abbreviations in app_strings.dart")
