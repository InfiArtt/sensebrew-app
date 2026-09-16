import re

with open('lib/core/grinder_database.dart', 'r', encoding='utf-8') as f:
    text = f.read()

vesper_fold = """    getSetting: (microns) {
      if (microns <= 400) return '15 - 28 klik';
      if (microns <= 600) return '29 - 45 klik';
      if (microns <= 800) return '46 - 65 klik';
      if (microns <= 1000) return '66 - 85 klik';
      if (microns <= 1200) return '86 - 105 klik';
      return '106 - 120 klik';
    },"""

vesper_lens = """    getSetting: (microns) {
      if (microns <= 400) return '10 - 20 klik';
      if (microns <= 600) return '21 - 32 klik';
      if (microns <= 800) return '33 - 48 klik';
      if (microns <= 1000) return '49 - 60 klik';
      if (microns <= 1200) return '61 - 75 klik';
      return '76 - 85 klik';
    },"""

# Replace Vesper VS3 Fold
text = re.sub(r'id:\s*\'vesper_vs3_fold\',\s*name:\s*\'Vesper VS3 Fold\',\s*isManual:\s*true,\s*getSetting:\s*\(microns\)\s*\{[^}]+\},',
              f"id: 'vesper_vs3_fold',\n    name: 'Vesper VS3 Fold',\n    isManual: true,\n{vesper_fold}", text)

# Replace Vesper Lens
text = re.sub(r'id:\s*\'vesper_lens\',\s*name:\s*\'Vesper Lens\',\s*isManual:\s*true,\s*getSetting:\s*\(microns\)\s*\{[^}]+\},',
              f"id: 'vesper_lens',\n    name: 'Vesper Lens',\n    isManual: true,\n{vesper_lens}", text)

with open('lib/core/grinder_database.dart', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated Vesper grinders logic again!")
