import re

with open('lib/core/recipe.dart', 'r', encoding='utf-8') as f:
    content = f.read()

# Define the updates for specific recipes
# Key: Recipe name (substring match is fine as long as it's unique)
# Value: (new_description, new_extra_ingredients)

updates = {
    "James Hoffmann Ultimate V60": (
        "Gunakan air 99°C dan gilingan medium-fine. Buat divot (lubang kecil) di tengah kopi. Goyangkan (swirl) alat seduh di fase bloom dan setelah tuangan terakhir untuk meratakan ekstraksi.\n\nEstimasi Rasa: Ekstraksi seimbang (balanced), manis yang optimal, dan clarity (kejernihan rasa) yang tinggi.",
        ""
    ),
    "Tetsu Kasuya 4-6 Method": (
        "Gunakan gilingan kasar (coarse) dan air 90-92°C. Biarkan air turun sepenuhnya (bed kering) sebelum lanjut ke tuangan berikutnya. 40% air pertama mengatur asam/manis, 60% sisanya mengatur kepekatan.\n\nEstimasi Rasa: Sangat jernih (clean cup), acidity (keasaman) terang, dengan body yang ringan (tea-like).",
        ""
    ),
    "Osmotic Flow": (
        "Gilingan medium-fine. Air 90-92°C. Tuang air sangat perlahan hanya di area tengah sebesar koin logam. JANGAN biarkan air mengenai kertas. Jaga kubah kopi (coffee dome) tetap utuh.\n\nEstimasi Rasa: Sangat manis (sweetness maksimal), body lembut dan tebal, dengan acidity yang diredam.",
        ""
    ),
    "April Pour-Over": (
        "Gunakan suhu rendah (sekitar 90°C) dan gilingan coarse. Tuang melingkar lambat tanpa agitasi keras. Disarankan menggunakan dripper flat-bed.\n\nEstimasi Rasa: Keasaman (acidity) yang sangat cerah, clean cup, dan rasa buah yang menonjol.",
        ""
    ),
    "Clever Dripper / Full Immersion": (
        "Gilingan medium. Tuang air terlebih dahulu, lalu masukkan bubuk kopi. Aduk setelah beberapa saat, lalu diamkan (steep).\n\nEstimasi Rasa: Body penuh, rasa sangat seimbang, dan minim risiko over-ekstraksi.",
        ""
    ),
    "James Hoffmann French Press": (
        "Gilingan medium (tidak perlu terlalu kasar). Seduh selama 4 menit, lalu aduk kerak kopi di permukaan. Bersihkan busa (skim). Tunggu lagi 5-8 menit sebelum menuang, dan JANGAN menekan plunger sampai bawah.\n\nEstimasi Rasa: Body penuh namun sangat jernih tanpa ampas, tekstur kental, dan rasa seimbang.",
        ""
    ),
    "Traditional French Press": (
        "Gilingan coarse (kasar). Tuang seluruh air, aduk merata. Diamkan selama 4 menit, lalu tekan plunger perlahan sampai dasar.\n\nEstimasi Rasa: Body sangat tebal, aroma kuat, tekstur berpasir/kotor (gritty) klasik.",
        ""
    ),
    "Alan Adler (Original)": (
        "Gunakan kertas filter. Air suhu 80°C (sangat rendah). Aduk cepat selama 10 detik, lalu tekan perlahan. Jangan menekan sampai mendesis.\n\nEstimasi Rasa: Sangat manis, acidity rendah, body tebal, mirip espresso concentrate.",
        ""
    ),
    "Tim Wendelboe Aeropress": (
        "Gilingan medium-fine. Air mendidih. Seduh normal (non-inverted). Aduk perlahan, lalu tekan perlahan di detik ke 60.\n\nEstimasi Rasa: Clean cup, acidity cerah, rasa mirip pour-over filter V60.",
        ""
    ),
    "Aeropress Iced Coffee": (
        "Gunakan metode inverted atau standar. Air mendidih untuk mengekstrak konsentrat kopi. Aduk merata, lalu tekan ke atas gelas yang berisi bongkahan es.\n\nEstimasi Rasa: Segar, pekat di awal namun mencair perlahan (refreshing), manis.",
        "Es batu (sekitar 100g)"
    ),
    "Tradisional Vietnam Drip": (
        "Gilingan medium-coarse. Kopi Robusta gelap. Padatkan dengan saringan tekan. Tuang air mendidih. Proses tetesan memakan waktu sekitar 5-6 menit.\n\nEstimasi Rasa: Pahit pekat, smokey, body sangat kental (syrupy) dan kuat.",
        ""
    ),
    "Ca Phe Sua Da (Kopi Susu Es)": (
        "Letakkan kental manis di dasar gelas. Kopi Robusta diteteskan langsung di atasnya. Setelah selesai, aduk merata, lalu tuangkan ke gelas berisi es batu.\n\nEstimasi Rasa: Manis karamel yang intens, gurih susu, kopi pekat yang menendang, tekstur creamy.",
        "Susu Kental Manis (30g), Es Batu (150g)"
    ),
    "Vietnam Drip Gula Aren": (
        "Gilingan medium. Gunakan sirup gula aren di dasar gelas. Seduh perlahan (tetasan 4-5 menit). Aduk rata lalu tambahkan es.\n\nEstimasi Rasa: Manis legit aren berpadu dengan pahit kopi, creamy, aroma rempah/karamel.",
        "Sirup Gula Aren (20ml), Es Batu (150g)"
    ),
    "Ca Phe Muoi (Salted Coffee)": (
        "Buat krim garam dengan mengocok susu kental manis, susu cair/krim, dan garam hingga berbusa. Teteskan kopi di atasnya. Aduk sebelum diminum.\n\nEstimasi Rasa: Kombinasi menakjubkan antara asin gurih, manis kental, dan pahit kopi pekat. Umami!",
        "Krim Asin (Susu 20ml, SKM 10g, Garam Sejumput), Es Batu (100g)"
    ),
    "Ca Phe Trung (Egg Coffee)": (
        "Kocok kuning telur ayam kampung dengan susu kental manis dan sedikit madu hingga mengembang menjadi busa kental. Teteskan kopi panas di atas/bawahnya.\n\nEstimasi Rasa: Sangat creamy, mirip dessert (tiramisu), manis kental, tanpa amis telur.",
        "Kuning Telur (1 butir), SKM (20g), Madu (1 sdt)"
    ),
    "Ca Phe Sua Chua (Yogurt Coffee)": (
        "Kombinasi unik Vietnam. Masukkan yogurt di dasar gelas, tambahkan kental manis, seduh kopi di atasnya, tambahkan es batu.\n\nEstimasi Rasa: Asam segar yogurt berpadu dengan manis creamy dan pahit kopi. Sangat menyegarkan.",
        "Yogurt Plain (50g), SKM (15g), Es Batu (100g)"
    ),
    "Vietnam Drip Mocha": (
        "Tambahkan bubuk kakao atau sirup coklat ke dalam kental manis. Teteskan kopi menembus coklat. Aduk rata.\n\nEstimasi Rasa: Coklat pekat (dark chocolate), manis, tebal, mirip permen kopi cokelat.",
        "Sirup Coklat/Kakao (15g), SKM (20g)"
    ),
    "Japanese Iced Coffee (Fruity)": (
        "Gilingan medium-fine. Tuang air panas ke kopi, tetesan akan langsung mengenai es batu di dalam server untuk mengunci aroma volatile. \n\nEstimasi Rasa: Acidity buah yang sangat tajam, segar, dan aromatik (floral/fruity).",
        "Es Batu (100g di server)"
    ),
    "Japanese Iced Coffee (Sweet)": (
        "Sama dengan Japanese Iced Coffee, namun rasio es batu disesuaikan dan tuangan dibagi untuk memaksimalkan manis. \n\nEstimasi Rasa: Lebih manis dan balance, tidak terlalu asam, body sedikit lebih tebal.",
        "Es Batu (90g di server)"
    ),
    "Double Tamp Vietnam Drip": (
        "Metode langka: Tekan kopi dengan saringan, tuang air bloom, lalu tekan LAGI (tamp kedua) sebelum menuang sisa air. Menghasilkan tetesan yang jauh lebih lambat.\n\nEstimasi Rasa: Intensitas ekstrak luar biasa, seperti espresso, body sangat tebal.",
        ""
    ),
    "Aeropress Milk Punch": (
        "Seduh kopi sangat pekat (concentrate) lalu aduk langsung dengan susu dingin dan es batu di dalam gelas.\n\nEstimasi Rasa: Milk punch yang lembut, creamy, dan segar.",
        "Susu Cair Dingin (100ml), Es Batu (100g)"
    ),
    "Cafe au Lait (Strong French Press)": (
        "Seduh kopi sangat pekat. Campurkan dengan susu panas yang di steam atau dihangatkan dengan rasio 1:1.\n\nEstimasi Rasa: Hangat, milky, gurih susu dengan karakter kopi yang tetap kuat.",
        "Susu Panas (150ml)"
    )
}

# General fallback for any recipe not in updates to append a generic "Estimasi Rasa" if lacking
import re

for recipe_name, (new_desc, new_ingredients) in updates.items():
    # Find the recipe block
    pattern = r'(Recipe\(\s*name: "' + re.escape(recipe_name) + r'".*?description: ")(.*?)(".*?extraIngredients: ")(.*?)(")'
    match = re.search(pattern, content, flags=re.DOTALL)
    
    if match:
        content = re.sub(pattern, r'\g<1>' + new_desc + r'\g<3>' + new_ingredients + r'\g<5>', content, flags=re.DOTALL)
    else:
        # Fallback if extraIngredients is missing, inject it before phases
        pattern2 = r'(Recipe\(\s*name: "' + re.escape(recipe_name) + r'".*?description: ")(.*?)(")'
        match2 = re.search(pattern2, content, flags=re.DOTALL)
        if match2:
            # Check if extraIngredients exists somewhere else
            if "extraIngredients:" not in content[match2.start():match2.end()+200]:
                content = re.sub(pattern2, r'\g<1>' + new_desc + r'"' + f',\n    extraIngredients: "{new_ingredients}"', content, flags=re.DOTALL)
            else:
                content = re.sub(pattern2, r'\g<1>' + new_desc + r'\g<3>', content, flags=re.DOTALL)

with open('lib/core/recipe.dart', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated recipe descriptions and ingredients.")
