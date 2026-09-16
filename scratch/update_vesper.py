import re

with open('lib/core/grinder_database.dart', 'r', encoding='utf-8') as f:
    text = f.read()

vesper_fold = """    getSetting: (microns) {
      if (microns <= 400) return '10 - 25 klik';
      if (microns <= 600) return '26 - 40 klik';
      if (microns <= 800) return '41 - 60 klik';
      if (microns <= 1000) return '61 - 80 klik';
      if (microns <= 1200) return '81 - 100 klik';
      return '101 - 120 klik';
    },"""

vesper_lens = """    getSetting: (microns) {
      if (microns <= 400) return '5 - 11 klik';
      if (microns <= 600) return '12 - 18 klik';
      if (microns <= 800) return '19 - 27 klik';
      if (microns <= 1000) return '28 - 38 klik';
      if (microns <= 1200) return '39 - 46 klik';
      return '47 - 54 klik';
    },"""

# Replace Vesper VS3 Fold
text = re.sub(r'id:\s*\'vesper_vs3_fold\',\s*name:\s*\'Vesper VS3 Fold\',\s*isManual:\s*true,\s*getSetting:\s*\(microns\)\s*\{[^}]+\},',
              f"id: 'vesper_vs3_fold',\n    name: 'Vesper VS3 Fold',\n    isManual: true,\n{vesper_fold}", text)

# Replace Vesper Lens
text = re.sub(r'id:\s*\'vesper_lens\',\s*name:\s*\'Vesper Lens\',\s*isManual:\s*true,\s*getSetting:\s*\(microns\)\s*\{[^}]+\},',
              f"id: 'vesper_lens',\n    name: 'Vesper Lens',\n    isManual: true,\n{vesper_lens}", text)

with open('lib/core/grinder_database.dart', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated Vesper grinders logic!")
