import re

with open('lib/core/recipe.dart', 'r', encoding='utf-8') as f:
    text = f.read()

fallback_tastes = {
    "Scott Rao V60": "Estimasi Rasa: Ekstraksi seimbang (high extraction yield), manis, minim astringency.",
    "Hario Official V60": "Estimasi Rasa: Klasik, body sedang, acidity menonjol, dan aroma seduh yang kuat.",
    "Hario Switch (Tetsu Kasuya)": "Estimasi Rasa: Sangat manis, perpaduan unik antara kejernihan V60 dan body dari imersi.",
    "Lance Hedrick French Press": "Estimasi Rasa: Sangat bersih untuk French Press, body lembut, rasa manis yang diekstrak perlahan.",
    "Slayer French Press (Skim Early)": "Estimasi Rasa: Body tebal namun minim partikel halus (grit), rasa lebih clean dari tradisional.",
    "French Press Cold Water Bloom": "Estimasi Rasa: Menurunkan acidity tajam dan pahit (bitterness), menonjolkan profil manis yang lebih lembut.",
    "Tim Wendelboe French Press": "Estimasi Rasa: Cita rasa Nordic roast (terang), acidity cerah, body ringan, lebih mirip cupping bowl.",
    "James Hoffmann Ultimate Aeropress": "Estimasi Rasa: Sangat efisien, manis, body penuh, dan ekstraksi merata tanpa asam berlebih.",
    "Inverted Classic": "Estimasi Rasa: Body kuat, rasa pekat (bold), cocok untuk dicampur susu atau diminum murni.",
    "Aeropress Espresso Concentrate": "Estimasi Rasa: Sangat pekat, asam dan pahit terkonsentrasi, cocok sebagai bahan dasar kopi susu.",
    "WAC 2023 Champion Recipe": "Estimasi Rasa: Kompleks, manis, acidity buah cerah namun tekstur sangat lembut (silky).",
    "Jonathan Gagne Long Steep": "Estimasi Rasa: Ekstraksi sangat tinggi (high EY), manis maksimal, tidak ada rasa asam under-extracted.",
    "Aeropress Espresso (Faux-Presso)": "Estimasi Rasa: Kuat, pekat (punchy), crema buatan (jika ditekan keras), cocok untuk mocktail/susu.",
    "Ca Phe Den (Kopi Hitam)": "Estimasi Rasa: Sangat pahit, kuat, dominan rasa coklat gelap/kacang sangrai, syrupy.",
    "Modern Specialty Drip": "Estimasi Rasa: Lebih jernih dari tradisional, acidity mulai muncul, kompleksitas rasa modern.",
    "Drip Ristretto Style": "Estimasi Rasa: Sangat pekat dan pendek, intensitas tinggi, pahit manis menghentak.",
    "Vietnam Drip Paper Filter Method": "Estimasi Rasa: Jauh lebih bersih (clean) tanpa ampas, body berkurang namun flavor lebih jelas.",
    "Specialty High-Ratio Drip (1:12)": "Estimasi Rasa: Rasio yang lebih panjang menghasilkan minuman yang lebih ringan, mirip pour-over pekat.",
    "SCA Cupping Protocol": "Estimasi Rasa: Profil rasa murni dari biji kopi untuk keperluan evaluasi cacat/kualitas.",
    "James Hoffmann Home Cupping": "Estimasi Rasa: Rasa murni biji kopi tanpa gangguan filter kertas, sangat cocok untuk membandingkan 2 biji.",
    "Cold Evaluation Cupping": "Estimasi Rasa: Menilai rasa kopi saat suhu ruang (menonjolkan sweetness atau justru defect/asam kecut).",
    "Minimal Agitation Cupping": "Estimasi Rasa: Sangat clean, ekstraksi lebih pelan menghindari kepahitan (astringency) berlebih.",
    "Ryan Wibawa WBrC 2024": "Estimasi Rasa: Rasa berlapis (layered), kompleksitas tinggi, manis aromatik yang elegan.",
    "Yoshua Tanu Fast Flow": "Estimasi Rasa: Acidity buah yang sangat transparan, ringan, mirip teh manis rasa kopi.",
    "Orea V3/Kalita Wave": "Estimasi Rasa: Tingkat kemanisan luar biasa berkat flat bed, ekstraksi konsisten, balance.",
    "V60 Dark Roast (Low Temp)": "Estimasi Rasa: Pahit yang lembut (smooth), manis karamel, tanpa rasa gosong/asap berlebih.",
    "Kasuya Devil Recipe (Switch)": "Estimasi Rasa: Sangat berani, ekstraksi manis pekat di awal, ditutup dengan imersi untuk body.",
    "W.A.C Carolina Ibarra (2018)": "Estimasi Rasa: Ceria (vibrant), acidity menyala, bersih (clean finish).",
    "W.A.C Paulina Miczka (2017)": "Estimasi Rasa: Bulat (round body), seimbang, sangat enak untuk kopi natural.",
    "Tuomas Merikanto W.A.C": "Estimasi Rasa: Kompleks, dominan manis, body juicy.",
    "Aeropress Flow Control": "Estimasi Rasa: Seperti espresso rumahan, pekat, tidak ada kebocoran air sebelum waktunya.",
    "Aeropress Espresso Fake": "Estimasi Rasa: Pahit, tebal, pekat, cocok dicampur gula merah atau susu.",
    "Aeropress Tea-like Extract": "Estimasi Rasa: Sangat ringan, tembus pandang, rasa bunga/buah dominan layaknya teh premium.",
    "Aeropress Robusta Sweet": "Estimasi Rasa: Pahit khas Robusta namun diimbangi tekstur kental dan rasa nutty yang manis.",
    "Phin Arabica Light": "Estimasi Rasa: Asam buah (fruity) khas Arabica, body tidak terlalu tebal dibanding Robusta.",
    "Phin Coconut (Bac Xiu)": "Estimasi Rasa: Manis gurih kelapa, sangat creamy, rasa kopi lebih lembut di latar belakang."
}

def replacer(match):
    name = match.group(1)
    desc = match.group(2)
    if 'Estimasi Rasa' not in desc and name in fallback_tastes:
        desc += "\\n\\n" + fallback_tastes[name]
    return f'Recipe(\n    name: "{name}",\n    description: "{desc}"'

# Regex to match the first two lines of Recipe constructor: name and description
pattern = r'Recipe\(\s*name: "(.*?)",\s*description: "(.*?)"'
text = re.sub(pattern, replacer, text)

# Phin Coconut (Bac Xiu) ingredient fix
if "Phin Coconut (Bac Xiu)" in text and 'Santan' not in text:
    text = re.sub(r'(name: "Phin Coconut \(Bac Xiu\)",.*?method: BrewMethod\.vietnamDrip,)', r'\1\n    extraIngredients: "Santan/Krim Kelapa (30ml), SKM (15g), Es Batu (100g)",', text, flags=re.DOTALL)

with open('lib/core/recipe.dart', 'w', encoding='utf-8') as f:
    f.write(text)

print("Appended generic Estimasi Rasa to all missing recipes.")
