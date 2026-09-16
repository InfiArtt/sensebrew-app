import re

with open('lib/core/app_strings.dart', 'r', encoding='utf-8') as f:
    text = f.read()

# Add Prismo note to ID
text = text.replace(
    "'desc_key_20': 'Seduh kopi sangat pekat (concentrate) lalu aduk langsung dengan susu dingin dan es batu di dalam gelas.\\n\\nEstimasi Rasa: Milk punch yang lembut, creamy, dan segar.',",
    "'desc_key_20': 'Seduh kopi sangat pekat (concentrate) (Gunakan alat Prismo / Flow Control) lalu aduk langsung dengan susu dingin dan es batu di dalam gelas.\\n\\nEstimasi Rasa: Milk punch yang lembut, creamy, dan segar.',"
)

# Add Prismo note to EN
text = text.replace(
    "'desc_key_20': 'Brew very concentrated coffee then stir directly with cold milk and ice cubes in a glass.\\n\\nTaste Estimation: Soft, creamy, and fresh milk punch.',",
    "'desc_key_20': 'Brew very concentrated coffee (Use Prismo / Flow Control cap) then stir directly with cold milk and ice cubes in a glass.\\n\\nTaste Estimation: Soft, creamy, and fresh milk punch.',"
)

with open('lib/core/app_strings.dart', 'w', encoding='utf-8') as f:
    f.write(text)
print("Updated desc_key_20")
