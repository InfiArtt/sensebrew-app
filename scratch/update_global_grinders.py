import re

with open('lib/core/grinder_database.dart', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('< 500', '<= 400')
text = text.replace('< 700', '<= 700')
text = text.replace('< 1000', '<= 1000')

with open('lib/core/grinder_database.dart', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated global grinder thresholds to <=")
