import re

with open('lib/core/grinder_database.dart', 'r', encoding='utf-8') as f:
    text = f.read()

vesper_lens = """    getSetting: (microns) {
      if (microns <= 400) return '8 - 15 klik';
      if (microns <= 600) return '16 - 24 klik';
      if (microns <= 800) return '25 - 35 klik';
      if (microns <= 1000) return '36 - 44 klik';
      if (microns <= 1200) return '45 - 50 klik';
      return '51 - 54 klik';
    },"""

# Replace Vesper Lens
text = re.sub(r'id:\s*\'vesper_lens\',\s*name:\s*\'Vesper Lens\',\s*isManual:\s*true,\s*getSetting:\s*\(microns\)\s*\{[^}]+\},',
              f"id: 'vesper_lens',\n    name: 'Vesper Lens',\n    isManual: true,\n{vesper_lens}", text)

with open('lib/core/grinder_database.dart', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated Vesper Lens logic for 54 clicks max!")
