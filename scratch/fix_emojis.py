import re

with open('lib/core/app_strings.dart', 'r', encoding='utf-8') as f:
    content = f.read()

fav_id = "'header_favorites': '" + chr(0x2B50) + " Favorit'"
fav_en = "'header_favorites': '" + chr(0x2B50) + " Favorites'"

cust_id = "'header_custom': '" + chr(0x2728) + " Resep Racikanmu'"
cust_en = "'header_custom': '" + chr(0x2728) + " Your Recipes'"

blt_id = "'header_builtin': '" + chr(0x2615) + " Resep Standar'"
blt_en = "'header_builtin': '" + chr(0x2615) + " Standard Recipes'"

content = re.sub(r"'header_favorites':\s*'[^\']+'", fav_id, content, count=1)
content = re.sub(r"'header_favorites':\s*'[^\']+'", fav_en, content)

content = re.sub(r"'header_custom':\s*'[^\']+'", cust_id, content, count=1)
content = re.sub(r"'header_custom':\s*'[^\']+'", cust_en, content)

content = re.sub(r"'header_builtin':\s*'[^\']+'", blt_id, content, count=1)
content = re.sub(r"'header_builtin':\s*'[^\']+'", blt_en, content)

with open('lib/core/app_strings.dart', 'w', encoding='utf-8') as f:
    f.write(content)

print('Done')
