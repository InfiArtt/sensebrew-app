import re

with open('lib/core/grinder_database.dart', 'r', encoding='utf-8') as f:
    text = f.read()

bad_vs3 = """  GrinderModel(
    id: 'vesper_vs3_fold',
    name: 'Vesper VS3 Fold',
    isManual: true,
    getSetting: (microns) {
      // Adjusted for realistic limits (max is usually ~36-40 before burr drops)
      if (microns < 500) return '10 - 14 klik';
      if (microns < 700) return '15 - 20 klik';
      if (microns < 1000) return '22 - 28 klik';
      return '30 - 35 klik';
    },
  ),"""

good_vs3 = """  GrinderModel(
    id: 'vesper_vs3_fold',
    name: 'Vesper VS3 Fold',
    isManual: true,
    getSetting: (microns) {
      // VS3 Fold has very fine threads, up to 110+ clicks
      if (microns < 500) return '15 - 30 klik';
      if (microns < 700) return '35 - 50 klik';
      if (microns < 1000) return '55 - 75 klik';
      return '80 - 110 klik';
    },
  ),"""

bad_lens = """  GrinderModel(
    id: 'vesper_lens',
    name: 'Vesper Lens',
    isManual: true,
    getSetting: (microns) {
      // Adjusted for realistic limits (similar to standard Timemore C2 threads)
      if (microns < 500) return '8 - 12 klik';
      if (microns < 700) return '13 - 17 klik';
      if (microns < 1000) return '18 - 24 klik';
      return '25 - 30 klik';
    },
  ),"""

good_lens = """  GrinderModel(
    id: 'vesper_lens',
    name: 'Vesper Lens',
    isManual: true,
    getSetting: (microns) {
      // Vesper Lens maximum is around 54 clicks
      if (microns < 500) return '12 - 16 klik';
      if (microns < 700) return '18 - 25 klik';
      if (microns < 1000) return '28 - 38 klik';
      return '42 - 54 klik';
    },
  ),"""

if bad_vs3 in text:
    text = text.replace(bad_vs3, good_vs3)
    print("Replaced VS3 Fold")
if bad_lens in text:
    text = text.replace(bad_lens, good_lens)
    print("Replaced Vesper Lens")

with open('lib/core/grinder_database.dart', 'w', encoding='utf-8') as f:
    f.write(text)
