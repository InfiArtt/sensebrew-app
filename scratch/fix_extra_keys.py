import re

with open('lib/core/app_strings.dart', 'r', encoding='utf-8') as f:
    text = f.read()

id_part, en_part = text.split("'en': {", 1)

translations = {
    r"'extra_key_0': 'Hot Milk \(150ml\)',": r"'extra_key_0': 'Susu Panas (150ml)',",
    r"'extra_key_2': 'Cold Liquid Milk \(100ml\), Ice Cubes \(100g\)',": r"'extra_key_2': 'Susu Cair Dingin (100ml), Es Batu (100g)',",
    r"'extra_key_3': 'Prepare 80 ml hot water in the serving glass for bypass',": r"'extra_key_3': 'Siapkan 80 ml air panas di gelas saji (untuk bypass)',",
    r"'extra_key_4': 'Ice cubes \(around 100g\)',": r"'extra_key_4': 'Es batu (sekitar 100g)',",
    r"'extra_key_5': 'Sweetened Condensed Milk \(30g\), Ice Cubes \(150g\)',": r"'extra_key_5': 'Susu Kental Manis (30g), Es Batu (150g)',",
    r"'extra_key_7': '30 ml sweetened condensed milk',": r"'extra_key_7': '30 ml susu kental manis',",
    r"'extra_key_8': 'Ice Cubes \(100g in server\)',": r"'extra_key_8': 'Es Batu (100g di server)',",
    r"'extra_key_9': 'Ice Cubes \(90g in server\)',": r"'extra_key_9': 'Es Batu (90g di server)',",
    r"'extra_key_10': 'Additional hot water/ice for dilution \(Bypass\)',": r"'extra_key_10': 'Air panas/es tambahan untuk bypass',",
    r"'extra_key_11': 'Salted Cream \(Milk 20ml, Condensed Milk 10g, Pinch of Salt\), Ice Cubes \(100g\)',": r"'extra_key_11': 'Krim Asin (Susu 20ml, SKM 10g, Sejumput Garam), Es Batu (100g)',",
    r"'extra_key_12': 'Egg Yolk \(1 pc\), Condensed Milk \(20g\), Honey \(1 tsp\)',": r"'extra_key_12': 'Kuning Telur (1 butir), SKM (20g), Madu (1 sdt)',",
    r"'extra_key_14': 'Chocolate/Cocoa Syrup \(15g\), Condensed Milk \(20g\)',": r"'extra_key_14': 'Sirup Cokelat/Kakao (15g), SKM (20g)',"
}

for pattern, replacement in translations.items():
    id_part = re.sub(pattern, replacement, id_part, flags=re.DOTALL)

text = id_part + "'en': {" + en_part

with open('lib/core/app_strings.dart', 'w', encoding='utf-8') as f:
    f.write(text)

print("Fixed Indonesian extra_keys!")
