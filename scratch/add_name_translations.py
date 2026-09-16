import re

with open('lib/core/app_strings.dart', 'r', encoding='utf-8') as f:
    text = f.read()

en_translations = """
      'Ca Phe Sua Da (Kopi Susu Es)': 'Ca Phe Sua Da (Iced Milk Coffee)',
      'Ca Phe Den (Kopi Hitam)': 'Ca Phe Den (Black Coffee)',
      'Vietnam Drip Gula Aren': 'Vietnam Drip Palm Sugar',
      'Tradisional Vietnam Drip': 'Traditional Vietnam Drip',
"""

text = text.replace("'en': {", "'en': {" + en_translations)

with open('lib/core/app_strings.dart', 'w', encoding='utf-8') as f:
    f.write(text)

print("Added recipe name translations to EN map!")
