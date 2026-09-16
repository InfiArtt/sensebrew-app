import os
import re

strings_file = "lib/core/app_strings.dart"
with open(strings_file, 'r', encoding='utf-8') as f:
    text = f.read()

id_part, en_part = text.split("'en': {", 1)

translations = {
    r"'desc_key_0': 'Gunakan air 99.*?tinggi\.',": r"'desc_key_0': 'Use 99°C water and medium-fine grind. Make a small divot in the center of the coffee. Swirl the brewer during bloom and after the final pour to even out extraction.\\n\\nTaste Estimation: Balanced extraction, optimal sweetness, and high clarity.',",
    r"'desc_key_4': 'Buat lubang \(divot\).*?astringency\.',": r"'desc_key_4': 'Make a divot in the center. Use high temperature. Do a Rao Spin (swirl the dripper in a circle) after bloom and at the end to flatten the bed and prevent channeling.\\n\\nTaste Estimation: High extraction yield, sweet, minimal astringency.',",
    r"'desc_key_21': 'Resep juara dunia Aeropress 2023.*?\(silky\)\.',": r"'desc_key_21': '2023 World Aeropress Champion recipe. Low temperature extraction with intense stirring, then bypassed with hot water at the end.\\n\\nTaste Estimation: Complex, sweet, bright fruity acidity but with a very silky texture.',",
    r"'desc_key_25': 'Gilingan medium-coarse.*?kuat\.',": r"'desc_key_25': 'Medium-coarse grind. Dark roasted Robusta. Tamp with the press filter. Pour boiling water. Dripping process takes around 5-6 minutes.\\n\\nTaste Estimation: Intensely bitter, smokey, very syrupy and strong body.',",
    r"'desc_key_27': 'Vietnam Drip tanpa susu kental manis.*?syrupy\.',": r"'desc_key_27': 'Vietnam Drip without condensed milk. Longer water ratio and coarser grind to avoid bitterness.\\n\\nTaste Estimation: Very bitter, strong, dominant dark chocolate/roasted nut flavor, syrupy.',",
    r"'desc_key_31': 'Menggunakan kertas saring.*?jelas\.',": r"'desc_key_31': 'Use a paper filter (Aeropress size) at the bottom of the Phin before adding coffee. Produces a super clean brew without fine grounds. (Optional: place another filter on top of coffee before tamping for super even extraction).\\n\\nTaste Estimation: Much cleaner without grounds, reduced body but clearer flavor.',",
    r"'desc_key_34': 'Suhu 93.*?kualitas\.',": r"'desc_key_34': '93°C temperature. At minute 4, push the back of a cupping spoon 3 times into the coffee surface (break the crust). Clean the remaining foam. Start slurping at minute 10 when the temperature drops.\\n\\nTaste Estimation: Pure flavor profile of the coffee bean for defect/quality evaluation.',",
    r"'desc_key_35': 'Cupping ala rumahan.*?2 biji\.',": r"'desc_key_35': 'Home cupping. Use two spoons to remove foam at minute 4.\\n\\nTaste Estimation: Pure flavor of the coffee bean without paper filter interference, very suitable for comparing 2 beans.',",
    r"'desc_key_36': 'Evaluasi fokus di rasa kopi.*?kecut\)\.',": r"'desc_key_36': 'Evaluation focuses on coffee taste when very cold at minute 15. Same initial phases, but wait very long.\\n\\nTaste Estimation: Assessing coffee taste at room temperature (highlights sweetness or reveals sour defects).',",
    r"'desc_key_38': 'Gilingan medium-fine.*?\(floral/fruity\)\.',": r"'desc_key_38': 'Medium-fine grind. Pour hot water onto coffee, drips will directly hit ice cubes in the server to lock in volatile aromas.\\n\\nTaste Estimation: Very sharp, fresh, and aromatic fruity acidity (floral/fruity).',",
    r"'desc_key_41': 'Suhu tinggi.*?kopi\.',": r"'desc_key_41': 'High temperature (93°C). Very fast flow pour. Aggressively swirl dripper at the beginning to wet all grounds evenly. Super fast finish in 2 minutes.\\n\\nTaste Estimation: Very transparent fruity acidity, light, like coffee-flavored sweet tea.',",
    r"'desc_key_42': 'Tuangan konsisten untuk.*?balance\.',": r"'desc_key_42': 'Consistent pours for a flat bed dripper. Highlights acidity and flavor clarity.\\n\\nTaste Estimation: Incredible sweetness thanks to the flat bed, consistent extraction, balanced.',",
    r"'desc_key_43': 'Gunakan air suhu 85C.*?berlebih\.',": r"'desc_key_43': 'Use 85°C water and fast center pours to avoid burnt and excessive bitter flavors in dark roasted beans.\\n\\nTaste Estimation: Smooth bitterness, caramel sweetness, without excessive burnt/smokey taste.',",
    r"'desc_key_44': 'Devil Recipe V60 Switch.*?body\.',": r"'desc_key_44': 'Devil Recipe V60 Switch. OPEN valve at the start. MUST use ROOM TEMPERATURE water for the first 60ml Bloom phase. For the rest, use boiling water for the immersion phase.\\n\\nTaste Estimation: Very bold, intense sweet extraction at first, finished with immersion for body.',",
    r"'desc_key_46': 'Resep juara 2017.*?natural\.',": r"'desc_key_46': '2017 Champion recipe. Intense 1:5 ratio at first, added with bypass water at the end. Inverted.\\n\\nTaste Estimation: Round body, balanced, very delicious for natural coffees.',",
    r"'desc_key_47': 'Aeropress standar \(tidak inverted\).*?juicy\.',": r"'desc_key_47': 'Standard Aeropress (not inverted). 80°C water, let it drip slowly then press very slowly.\\n\\nTaste Estimation: Complex, dominantly sweet, juicy body.',",
    r"'desc_key_48': 'Menggunakan cap Prismo.*?waktunya\.',": r"'desc_key_48': 'Using Prismo cap or Flow Control. Full immersion without inverted.\\n\\nTaste Estimation: Like home espresso, intense, no premature water leakage.',",
    r"'desc_key_49': 'Ekstraksi konsentrat tinggi.*?susu\.',": r"'desc_key_49': 'High concentrate extraction resembling espresso. Use Prismo/Flow Control and espresso grind.\\n\\nTaste Estimation: Bitter, thick, intense, suitable for mixing with brown sugar or milk.',",
    r"'desc_key_51': 'Khusus untuk kopi Robusta.*?manis\.',": r"'desc_key_51': 'Specifically for Robusta coffee. Short extraction with 85°C temperature so it is not too bitter.\\n\\nTaste Estimation: Typical Robusta bitterness but balanced with thick texture and sweet nutty flavor.',",
    r"'desc_key_52': 'Buat krim garam.*?Umami!',": r"'desc_key_52': 'Make salted cream by shaking condensed milk, liquid milk/cream, and salt until foamy. Drip coffee on top. Stir before drinking.\\n\\nTaste Estimation: Amazing combination of savory salty, thick sweet, and intense bitter coffee. Umami!',",
    r"'desc_key_53': 'Kocok kuning telur.*?telur\.',": r"'desc_key_53': 'Beat free-range egg yolk with condensed milk and a little honey until it fluffs into thick foam. Drip hot coffee on top/bottom.\\n\\nTaste Estimation: Very creamy, like dessert (tiramisu), thick sweetness, no eggy smell.',",
    r"'desc_key_55': 'Vietnam Drip khusus.*?Robusta\.',": r"'desc_key_55': 'Vietnam Drip specifically for Arabica beans. Tamp slightly, 92°C temperature for a thick yet fruity body.\\n\\nTaste Estimation: Typical Arabica fruity acidity, body is not as thick as Robusta.',",
    r"'desc_key_56': 'Tambahkan bubuk kakao.*?cokelat\.',": r"'desc_key_56': 'Add cocoa powder or chocolate syrup into condensed milk. Drip coffee through the chocolate. Stir well.\\n\\nTaste Estimation: Intense dark chocolate, sweet, thick, like chocolate coffee candy.',",
    
    r"'extra_key_1': '140ml Air panas tambahan \(Bypass\)',": r"'extra_key_1': '140ml Additional hot water (Bypass)',",
    r"'extra_key_6': 'Susu Kental Manis \(15-20ml\), Sirup Gula Aren \(10-15ml\), Es Batu',": r"'extra_key_6': 'Sweetened Condensed Milk (15-20ml), Palm Sugar Syrup (10-15ml), Ice Cubes',",
    r"'extra_key_13': 'Yogurt Plain \(50g\), SKM \(15g\), Es Batu \(100g\)',": r"'extra_key_13': 'Plain Yogurt (50g), Condensed Milk (15g), Ice Cubes (100g)',",
    r"'extra_key_15': '40 ml susu kental manis.*?penampung\)',": r"'extra_key_15': '40 ml sweetened condensed milk, 60 ml liquid coconut milk, 100 grams ice cubes. (Mix all in the serving glass)',"
}

for pattern, replacement in translations.items():
    en_part = re.sub(pattern, replacement, en_part, flags=re.DOTALL)

text = id_part + "'en': {" + en_part

with open(strings_file, 'w', encoding='utf-8') as f:
    f.write(text)

print("Translated remaining Indonesian descriptions to English.")
