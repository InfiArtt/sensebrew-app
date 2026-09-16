import re

# 1. Fix app_strings.dart
with open('lib/core/app_strings.dart', 'r', encoding='utf-8') as f:
    content = f.read()

# I need to fix the unescaped newlines in the injected string.
# Instead of manual fixing, I'll just replace the multiline broken string.
content = re.sub(
    r"'calib_guide': 'Panduan Kalibrasi:.*?kolom di bawah!',",
    r"'calib_guide': 'Panduan Kalibrasi:\\n1. Siapkan teko kopi (berisi air) dan timbangan atau gelas takar.\\n2. Aktifkan tombol \\'Simulasi Metronom\\' di bawah.\\n3. Setelah aba-aba \\'Mulai\\', mulailah menuang air seperti biasa.\\n4. Hitung ada berapa bunyi \\'TIK\\' yang terdengar sampai air mencapai target ml yang kamu mau.\\n5. Coba tuang sambil memutar teko (tuang melingkar), lalu hitung butuh berapa \\'TIK\\' untuk menyelesaikan 1 putaran penuh.\\n6. Masukkan angka-angka tadi ke dalam kolom di bawah!',",
    content,
    flags=re.DOTALL
)

content = re.sub(
    r"'calib_guide': 'Calibration Guide:.*?fields below!',",
    r"'calib_guide': 'Calibration Guide:\\n1. Prepare a coffee kettle (with water) and a scale or measuring cup.\\n2. Activate the \\'Metronome Simulation\\' button below.\\n3. After the \\'Start\\' cue, begin pouring water normally.\\n4. Count how many \\'TICK\\' sounds you hear until the water reaches your target ml.\\n5. Try pouring while moving the kettle in a circle, and count how many \\'TICKs\\' it takes to complete 1 full rotation.\\n6. Enter those numbers into the fields below!',",
    content,
    flags=re.DOTALL
)

with open('lib/core/app_strings.dart', 'w', encoding='utf-8') as f:
    f.write(content)

# 2. Fix ai_chat_screen.dart
with open('lib/screens/ai_chat_screen.dart', 'r', encoding='utf-8') as f:
    chat_content = f.read()

# Fix `lang` in _processAiRequest
chat_content = chat_content.replace(
    "final settings = Provider.of<SettingsState>(context, listen: false);",
    "final settings = Provider.of<SettingsState>(context, listen: false);\n    final lang = settings.appLanguage;"
)

# Fix const InputDecoration
chat_content = chat_content.replace(
    "const InputDecoration(\n                      hintText",
    "InputDecoration(\n                      hintText"
)
chat_content = chat_content.replace(
    "border: InputBorder.none,\n                      contentPadding: EdgeInsets.symmetric(horizontal: 16),\n                    )",
    "border: InputBorder.none,\n                      contentPadding: const EdgeInsets.symmetric(horizontal: 16),\n                    )"
)

with open('lib/screens/ai_chat_screen.dart', 'w', encoding='utf-8') as f:
    f.write(chat_content)

print("Fixed syntax errors!")
