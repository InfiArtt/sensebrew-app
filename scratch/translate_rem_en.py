import re

with open('lib/core/app_strings.dart', 'r', encoding='utf-8') as f:
    text = f.read()

# Fix mangled degree symbols (like 93AC, 99AC, etc.) globally
text = re.sub(r'(\d+)\s*A\S?C', r'\1°C', text)

id_part, en_part = text.split("'en': {", 1)

translations = {
    r"'desc_key_2': 'Gilingan medium-fine.*?diredam\.',": r"'desc_key_2': 'Medium-fine grind. 90-92°C water. Pour water very slowly only in the center, about the size of a coin. DO NOT let water touch the paper filter. Keep the coffee dome intact.\\n\\nTaste Estimation: Very sweet (maximum sweetness), soft and thick body, with muted acidity.',",
    r"'desc_key_6': 'God Recipe Tetsu Kasuya.*?imersi\.',": r"'desc_key_6': 'God Recipe Tetsu Kasuya. 90°C temperature. OPEN valve at the start (percolation). At 65 seconds, CLOSE valve (immersion). OPEN valve again at the end. Produces perfectly balanced extraction.\\n\\nTaste Estimation: Very sweet, a unique blend of V60 clarity and immersion body.',",
    r"'desc_key_8': 'Gilingan medium \(tidak.*?seimbang\.',": r"'desc_key_8': 'Medium grind (not too coarse). Steep for 4 minutes, then stir the coffee crust on the surface. Clean the foam (skim). Wait another 5-8 minutes before pouring, and DO NOT press the plunger to the bottom.\\n\\nTaste Estimation: Full body but very clean without grounds, thick texture, and balanced taste.',",
    r"'desc_key_11': 'Gilingan sedang-halus.*?perlahan\.',": r"'desc_key_11': 'Medium-fine grind. Stir evenly with a spoon right at the beginning. Let it steep for 5 minutes. Press plunger ONLY until it touches the water so fine grounds remain at the bottom.\\n\\nTaste Estimation: Very clean for a French Press, soft body, sweet taste extracted slowly.',",
    r"'desc_key_12': 'Aduk kuat di awal.*?tradisional\.',": r"'desc_key_12': 'Stir vigorously at the beginning and immediately remove foam in the first minute for even extraction from the start.\\n\\nTaste Estimation: Thick body but minimal fine particles (grit), cleaner taste than traditional.',",
    r"'desc_key_13': 'Pra-seduh dengan air.*?lembut\.',": r"'desc_key_13': 'Pre-infuse with room temperature water for 1 minute, then pour hot water. Reduces bitterness and enhances natural sweetness.\\n\\nTaste Estimation: Reduces sharp acidity and bitterness, highlights a softer sweet profile.',",
    r"'desc_key_14': 'Mirip cupping.*?bowl\.',": r"'desc_key_14': 'Similar to cupping. Steep for 4 minutes, stir gently, remove foam and crust, wait another 5 minutes before pressing.\\n\\nTaste Estimation: Nordic roast (light) profile, bright acidity, light body, more like a cupping bowl.',",
    r"'desc_key_15': 'Gunakan kertas filter.*?concentrate\.',": r"'desc_key_15': 'Use a paper filter. 80°C water (very low). Stir quickly for 10 seconds, then press slowly. Do not press until it hisses.\\n\\nTaste Estimation: Very sweet, low acidity, thick body, similar to espresso concentrate.',",
    r"'desc_key_16': 'Gilingan medium-fine.*?V60\.',": r"'desc_key_16': 'Medium-fine grind. Boiling water. Standard brew (non-inverted). Stir gently, then press slowly at 60 seconds.\\n\\nTaste Estimation: Clean cup, bright acidity, taste similar to V60 pour-over.',",
    r"'desc_key_22': 'Durasi panjang 9 menit.*?under-extracted\.',": r"'desc_key_22': 'Long 9-minute duration with V60-size grind. Produces sweet and even extraction without bitterness.\\n\\nTaste Estimation: Very high extraction (high EY), maximum sweetness, no under-extracted sourness.',"
}

for pattern, replacement in translations.items():
    en_part = re.sub(pattern, replacement, en_part, flags=re.DOTALL)

text = id_part + "'en': {" + en_part

with open('lib/core/app_strings.dart', 'w', encoding='utf-8') as f:
    f.write(text)

print("Fixed degree symbols and remaining translations.")
