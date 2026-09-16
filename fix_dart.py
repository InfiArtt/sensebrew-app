import json
import re

with open("id_data.json", "r", encoding="utf-8") as f:
    id_data = json.load(f)

# Load the translations we already made
with open("translated_new.json", "r", encoding="utf-8") as f:
    trans_new = json.load(f)

# Manually add missing ones 5 to 8
trans_new["desc_key_5"] = "Classic Hario factory recipe. Very beginner-friendly. Pour slowly in a circular motion from the center outwards, then back to the center.\n\nFlavor Profile: Classic, medium body, prominent acidity, and strong brewing aroma."
trans_new["desc_key_6"] = "God Recipe by Tetsu Kasuya. Temperature 90°C. OPEN the valve at the start (percolation). At 65 seconds, CLOSE the valve (immersion). OPEN the valve again at the end. Produces a perfectly balanced extraction.\n\nFlavor Profile: Very sweet, a unique blend of V60 clarity and immersion body."
trans_new["desc_key_7"] = "Medium grind. Pour water first, then add the coffee grounds. Stir after a few moments, then let it steep.\n\nFlavor Profile: Full body, very balanced flavor, and minimal risk of over-extraction."
trans_new["desc_key_8"] = "Medium grind (does not need to be too coarse). Brew for 4 minutes, then stir the coffee crust on the surface. Skim the foam. Wait another 5-8 minutes before pouring, and DO NOT press the plunger to the bottom.\n\nFlavor Profile: Full body yet very clean without grounds, thick texture, and balanced flavor."

trans_new["desc_key_0"] = "Use water at 99°C and a medium-fine grind. Create a divot in the center of the coffee bed. Swirl the brewer during the bloom phase and after the final pour to ensure even extraction.\n\nEstimated Flavor Profile: Balanced extraction, optimal sweetness, and high clarity."
trans_new["desc_key_1"] = "Use a coarse grind and 90-92°C water. Allow the bed to dry completely before proceeding to the next pour. The first 40% of the water influences acidity and sweetness, and the remaining 60% controls the strength.\n\nFlavor Profile: Clean cup, bright acidity, with a light, tea-like body."
trans_new["desc_key_2"] = "Medium-fine grind. Water at 90-92°C. Pour water very slowly, only in a coin-sized area in the center. DO NOT let the water touch the filter paper. Keep the coffee dome intact.\n\nEstimated Flavor Profile: Very sweet (maximum sweetness), with a smooth and rich body, and muted acidity."
trans_new["desc_key_3"] = "Use a low temperature (around 90°C) and a coarse grind. Pour slowly in a circular motion without vigorous agitation. A flat-bed dripper is recommended.\n\nFlavor Profile: Very bright acidity, a clean cup, and prominent fruity notes."
trans_new["desc_key_4"] = "Make a divot in the center. Use a high temperature. Perform a 'Rao Spin' (swirl the dripper in a circular motion) after the bloom and at the end to level the coffee bed and prevent channeling.\n\nEstimated Taste: Balanced extraction (high extraction yield), sweet, minimal astringency."

with open("lib/core/app_strings.dart", "r", encoding="utf-8") as f:
    content = f.read()

# Replace each key in the EN block
# We will do this by replacing the entire value for the key in the EN block.
en_block_match = re.search(r"('en': \{)(.*?)(\n    \},)", content, re.DOTALL)
en_text = en_block_match.group(2)

new_en_text = en_text
for key in id_data.keys():
    if key in trans_new:
        val = trans_new[key]
        # escape for Dart single quotes
        safe_val = val.replace("'", "\\'")
        # literal \n for Dart code
        safe_val = safe_val.replace('\n', '\\n')
        
        # Regex to find the key in the EN block. It might span multiple lines currently because it's corrupted.
        # We find 'key': ... up to the next key or end of dict.
        # It's safer to just replace the whole en_text line by line? No, it spans multiple lines.
        # Let's match 'key': '...'(comma or end)
        pattern = rf"('{key}':\s*')(.*?)(',\n|'\n|',\s*'desc_key|',\s*'extra_key|',\s*'|'\s*'desc_key)"
        
        def replacer(m):
            end_match = m.group(3)
            if end_match.startswith("',"):
                return f"{m.group(1)}{safe_val}',\n"
            else:
                return f"{m.group(1)}{safe_val}'\n"
                
        # Wait, a safer regex:
        # Match from 'key': ' until the LAST single quote before a comma or before another key.
        # Actually, since it's just Dart string, let's just split by keys!
        
new_en_text = re.sub(r"('desc_key_\d+': ')(.*?)(',\n|'\n|',\r\n|'\r\n)", lambda m: f"{m.group(1)}{trans_new.get(m.group(0).split(\"'\")[1], m.group(2)).replace('\'', '\\\'').replace(chr(10), '\\n')}{m.group(3)}", en_text, flags=re.DOTALL)

# But wait, my previous regex ruined the file, some don't have trailing commas maybe.
