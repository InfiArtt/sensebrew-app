import re

with open('lib/core/recipe.dart', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Add swirl to enum
text = text.replace('  stir,\n', '  stir,\n  swirl,\n')

# 2. Update descriptions and actions for V60 recipes
# Hoffmann
text = text.replace(
    'RecipePhase(startTimeSeconds: 10, action: PhaseAction.stir)',
    'RecipePhase(startTimeSeconds: 10, action: PhaseAction.swirl)'
)
text = text.replace(
    'RecipePhase(startTimeSeconds: 105, action: PhaseAction.stir)',
    'RecipePhase(startTimeSeconds: 105, action: PhaseAction.swirl)'
)
text = re.sub(
    r'(name: "James Hoffmann Ultimate V60",\n\s*description: )".*?"',
    r'\1"Buat lubang kecil (divot) di tengah bubuk kopi sebelum mulai. Gunakan air sangat panas (99°C). Goyangkan dripper (swirl) di fase bloom dan di akhir agar ekstraksi merata rata."',
    text
)

# Scott Rao
text = text.replace(
    'RecipePhase(startTimeSeconds: 5, action: PhaseAction.stir)',
    'RecipePhase(startTimeSeconds: 5, action: PhaseAction.swirl)'
)
text = text.replace(
    'RecipePhase(startTimeSeconds: 90, action: PhaseAction.stir)',
    'RecipePhase(startTimeSeconds: 90, action: PhaseAction.swirl)'
)
text = re.sub(
    r'(name: "Scott Rao V60",\n\s*description: )".*?"',
    r'\1"Buat lubang (divot) di tengah. Gunakan suhu tinggi. Lakukan \'Rao Spin\' (goyangkan dripper melingkar) setelah bloom dan di akhir untuk meratakan bed ampas kopi dan mencegah channeling."',
    text
)

# Yoshua Tanu
text = text.replace(
    'name: "Yoshua Tanu Fast Flow",\n    description: "Teknik seduh cepat (2 menit) dari 3x Juara Barista Indonesia. Agitasi kuat dan suhu tinggi (93°C) untuk menonjolkan aroma biji proses eksperimental tanpa berbau earthy.",',
    'name: "Yoshua Tanu Fast Flow",\n    description: "Suhu tinggi (93°C). Tuang air sangat deras (fast flow). Goyang/swirl dripper lumayan agresif di awal agar semua bubuk basah merata. Selesai super singkat di 2 menit.",'
)
# We already used stir for Yoshua Tanu, let's change to swirl
match = re.search(r'(name: "Yoshua Tanu Fast Flow".*?phases: \[)(.*?)(\],)', text, re.DOTALL)
if match:
    phases = match.group(2).replace('PhaseAction.stir', 'PhaseAction.swirl')
    text = text[:match.start()] + match.group(1) + phases + match.group(3) + text[match.end():]

# Osmotic Flow
text = re.sub(
    r'(name: "Osmotic Flow",\n\s*description: )".*?"',
    r'\1"Gilingan cenderung medium-fine. Tuang air perlahan hanya di area tengah (seukuran koin). JANGAN biarkan air mengenai kertas. Jaga struktur \'kubah\' kopi tidak hancur untuk mengeluarkan sweetness maksimal."',
    text
)

# April
text = re.sub(
    r'(name: "April Pour-Over",\n\s*description: )".*?"',
    r'\1"Gunakan suhu rendah (sekitar 90°C). Tuang melingkar lambat dan stabil tanpa agitasi keras. Sangat dianjurkan memakai flat bed dripper. Menghasilkan acidity cerah dengan body ringan."',
    text
)

# Kasuya 4-6
text = re.sub(
    r'(name: "Tetsu Kasuya 4-6 Method",\n\s*description: )".*?"',
    r'\1"Gilingan kasar (coarse). Biarkan air turun sepenuhnya menembus kopi (bed kering) sebelum lanjut ke tuangan berikutnya. 40% air pertama mengatur manis/asam, 60% sisa mengatur kepekatan."',
    text
)

# Hario Official
text = re.sub(
    r'(name: "Hario Official V60",\n\s*description: )".*?"',
    r'\1"Resep klasik bawaan pabrik Hario. Sangat ramah pemula. Tuang perlahan secara memutar dari tengah ke luar, lalu kembali ke tengah."',
    text
)

# Hario Switch Tetsu
text = re.sub(
    r'(name: "Hario Switch \(Tetsu Kasuya\)",\n\s*description: )".*?"',
    r'\1"God Recipe Tetsu Kasuya. Suhu 90°C. BUKA keran di awal (perkolasi). Di detik ke-65, TUTUP keran (imersi). BUKA keran lagi di akhir. Menghasilkan ekstraksi balance sempurna."',
    text
)

# Kasuya Devil
text = re.sub(
    r'(name: "Kasuya Devil Recipe \(Switch\)",\n\s*description: )".*?"',
    r'\1"Devil Recipe V60 Switch. BUKA keran di awal. WAJIB gunakan air SUHU RUANG (dingin/biasa) untuk fase Bloom 60ml pertama. Sisanya, gunakan air sangat mendidih untuk fase imersi."',
    text
)

# Japanese Iced (Sweet & Fruity)
text = re.sub(
    r'(name: "Japanese Iced Coffee \(Fruity\)",\n\s*description: )".*?"',
    r'\1"(Siapkan 100g es batu di server/gelas). Gilingan sedikit lebih halus. Fokus ekstraksi beruntun di awal untuk menonjolkan rasa buah (fruity) yang cerah."',
    text
)
text = re.sub(
    r'(name: "Japanese Iced Coffee \(Sweet\)",\n\s*description: )".*?"',
    r'\1"(Siapkan 100g es batu di server/gelas). Gilingan sedikit lebih halus. Tuangan dibagi dan dijedah lebih lama untuk memancing karamel (sweetness) keluar lebih banyak."',
    text
)

# Clever Dripper
text = re.sub(
    r'(name: "Clever Dripper / Full Immersion",\n\s*description: )".*?"',
    r'\1"Tutup keran/tuas dari awal. Tuang seluruh air, lalu aduk pelan permukaannya dengan sendok. Tunggu 2 menit, buka tuas. (Bisa juga tuang air duluan sebelum kopi agar tidak mampet)."',
    text
)

with open('lib/core/recipe.dart', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated recipe.dart successfully")
