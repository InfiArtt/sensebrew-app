import re

with open('lib/core/recipe.dart', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. DELETE REDUNDANT RECIPES
recipes_to_delete = [
    "French Press Espresso Style",
    "Long Steep French Press \\(10 Menit\\)",
    "Sprometheus French Press",
    "Coconut Vietnam Drip",
    "Rapid QC Cupping",
    "Roast Defect Cupping",
    "High Extraction Cupping",
    "Espresso Roast Cupping",
    "Sifted Fines Cupping",
    "Travel Cupping \\(Thermos\\)"
]

for recipe_name in recipes_to_delete:
    # Match from Recipe( up to the end of the Recipe block
    pattern = r'\s*Recipe\(\s*name:\s*"' + recipe_name + r'".*?\]\s*,\s*\),'
    text = re.sub(pattern, '', text, flags=re.DOTALL)

# 2. UPDATE AEROPRESS
# Hoffmann Aeropress
text = text.replace(
    'name: "James Hoffmann Ultimate Aeropress",\n      description: "Lebih hemat kopi. Posisi standar. Seduh 2 menit, putar sedikit, diamkan 30 detik, lalu tekan perlahan.",',
    'name: "James Hoffmann Ultimate Aeropress",\n      description: "(Posisi Standar). Tuang air. Di menit ke-2, pegang tabung dan goyangkan perlahan (swirl), bukan diaduk pakai sendok. Diamkan 30 detik agar ampas turun, lalu tekan pelan.",'
)
match_hoffmann_aero = re.search(r'(name: "James Hoffmann Ultimate Aeropress".*?phases: \[)(.*?)(\],)', text, re.DOTALL)
if match_hoffmann_aero:
    phases = match_hoffmann_aero.group(2).replace('PhaseAction.stir', 'PhaseAction.swirl')
    text = text[:match_hoffmann_aero.start()] + match_hoffmann_aero.group(1) + phases + match_hoffmann_aero.group(3) + text[match_hoffmann_aero.end():]

# Inverted Classic
text = re.sub(
    r'(name: "Inverted Classic",\n\s*description: )".*?"',
    r'\1"(WAJIB Posisi Terbalik / Inverted). Tuang air, aduk kuat dengan sendok, lalu tutup. Di menit 1:30, balikkan alat ke atas gelas perlahan dan tekan turun."',
    text
)

# Alan Adler
text = re.sub(
    r'(name: "Alan Adler \(Original\)",\n\s*description: )".*?"',
    r'\1"(Posisi Standar). Suhu sangat rendah (80°C). Masukkan kopi, tuang air sampai angka 1. Aduk kuat selama 10 detik dengan sendok/paddle bawaan, lalu langsung tekan secepatnya."',
    text
)

# Tim Wendelboe Aeropress
text = re.sub(
    r'(name: "Tim Wendelboe Aeropress",\n\s*description: )".*?"',
    r'\1"(Posisi Standar). Tuang seluruh air, aduk cukup kuat dengan sendok 3 kali ke depan dan belakang. Pasang tutupnya, tunggu 1 menit, lalu tekan perlahan."',
    text
)

# 3. UPDATE FRENCH PRESS
# Hoffmann French Press
text = re.sub(
    r'(name: "James Hoffmann French Press",\n\s*description: )".*?"',
    r'\1"Di menit ke-4, gunakan sendok untuk memecah kerak kopi di permukaan dan buang busanya (skim). Tunggu 5-8 menit lagi, lalu tekan plunger HANYA sampai menyentuh air (jangan sampai ke dasar)."',
    text
)

# Traditional French Press
text = re.sub(
    r'(name: "Traditional French Press",\n\s*description: )".*?"',
    r'\1"Resep klasik 4 menit. Gilingan sangat kasar. Di menit pertama buka tutup dan aduk pelan dengan sendok kayu/plastik agar kaca tidak pecah. Menit ke-4 langsung tekan plunger sampai dasar."',
    text
)

# Lance Hedrick French Press
text = re.sub(
    r'(name: "Lance Hedrick French Press",\n\s*description: )".*?"',
    r'\1"Gilingan sedang-halus. Langsung aduk merata dengan sendok di awal. Diamkan 5 menit. Tekan plunger HANYA sampai menyentuh air agar serbuk halus tetap tertahan di bawah."',
    text
)

# 4. UPDATE VIETNAM DRIP
# Tradisional Vietnam Drip
text = re.sub(
    r'(name: "Tradisional Vietnam Drip",\n\s*description: )".*?"',
    r'\1"Tuang kental manis di dasar gelas. Masukkan Phin, beri kopi, dan padatkan (tamping) sedang. Tuang sedikit air untuk bloom, biarkan air menetes perlahan. Aduk dengan sendok panjang sebelum diminum."',
    text
)

# Ca Phe Sua Da
text = re.sub(
    r'(name: "Ca Phe Sua Da \(Kopi Susu Es\)",\n\s*description: )".*?"',
    r'\1"Gunakan kental manis lebih banyak. Padatkan (tamp) kopi lebih kuat. Setelah selesai menetes, aduk rata dengan sendok lalu tuang seluruhnya ke dalam gelas penuh es batu."',
    text
)

# 5. UPDATE CUPPING
# SCA Protocol
text = re.sub(
    r'(name: "SCA Cupping Protocol",\n\s*description: )".*?"',
    r'\1"Suhu 93°C. Di menit ke-4, dorong punggung sendok cupping sebanyak 3 kali ke permukaan kopi (break the crust). Bersihkan sisa busanya. Mulai seruput di menit ke-10 saat suhu turun."',
    text
)

with open('lib/core/recipe.dart', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated non-V60 recipes and pruned duplicates.")
