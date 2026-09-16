import re

with open('lib/core/recipe.dart', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the octal escape bug (change `p,` back to `\n      totalWaterMl: 60,`)
# Let's just find Alan Adler and replace the whole thing safely
bad_str = 'name: "Alan Adler (Original)",p,'
good_str = 'name: "Alan Adler (Original)",\n      extraIngredients: "140ml Air panas tambahan (Bypass)",\n      description: "Gunakan kertas filter. Air suhu 80AC (sangat rendah). Aduk cepat selama 10 detik, lalu tekan perlahan. Jangan menekan sampai mendesis.\\n\\nEstimasi Rasa: Sangat manis, acidity rendah, body tebal, mirip espresso concentrate.",\n      coffeeGrams: 15,\n      totalWaterMl: 60,'

content = content.replace(bad_str, good_str)

with open('lib/core/recipe.dart', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed 'p' bug!")
