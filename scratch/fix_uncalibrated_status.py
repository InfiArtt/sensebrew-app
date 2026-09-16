import re

with open('lib/core/app_strings.dart', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    "'uncalibrated_status': 'Belum dikalibrasi',",
    "'uncalibrated_status': 'Debit air belum dikalibrasi.',"
)

with open('lib/core/app_strings.dart', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated uncalibrated_status ID")
