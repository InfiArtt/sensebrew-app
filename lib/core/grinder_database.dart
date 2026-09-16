import 'app_strings.dart';

class GrinderModel {
  final String id;
  final String name;
  final bool isManual;
  final String Function(int microns) getSetting;

  const GrinderModel({
    required this.id,
    required this.name,
    required this.isManual,
    required this.getSetting,
  });
}

final List<GrinderModel> grinderDatabase = [
  // Manual Grinders
  GrinderModel(
    id: 'timemore_c2',
    name: 'Timemore C2 / C3',
    isManual: true,
    getSetting: (microns) {
      if (microns <= 400) return '8 - 10 ';
      if (microns <= 600) return '11 - 14 ';
      if (microns <= 800) return '15 - 18 ';
      if (microns <= 1000) return '19 - 22 ';
      if (microns <= 1200) return '23 - 26 ';
      return '27 - 30 ';
    },
  ),
  GrinderModel(
    id: 'comandante_c40',
    name: 'Comandante C40',
    isManual: true,
    getSetting: (microns) {
      if (microns <= 400) return '8 - 12 ';
      if (microns <= 600) return '13 - 19 ';
      if (microns <= 800) return '20 - 25 ';
      if (microns <= 1000) return '26 - 30 ';
      if (microns <= 1200) return '31 - 35 ';
      return '36 - 40 ';
    },
  ),
  GrinderModel(
    id: 'kingrinder_k6',
    name: 'Kingrinder K6',
    isManual: true,
    getSetting: (microns) {
      if (microns <= 400) return '30 - 50 ';
      if (microns <= 600) return '55 - 75 ';
      if (microns <= 800) return '80 - 100 ';
      if (microns <= 1000) return '105 - 120 ';
      if (microns <= 1200) return '125 - 140 ';
      return '145 - 160 ';
    },
  ),
  GrinderModel(
    id: '1zpresso_jxpro',
    name: '1Zpresso JX-Pro',
    isManual: true,
    getSetting: (microns) {
      if (microns <= 400) return '1.2 - 1.6 putaran';
      if (microns <= 600) return '2.0 - 2.5 putaran';
      if (microns <= 800) return '2.8 - 3.4 putaran';
      if (microns <= 1000) return '3.5 - 3.9 putaran';
      if (microns <= 1200) return '4.0 - 4.5 putaran';
      return '4.6 - 5.0 putaran';
    },
  ),
  GrinderModel(
    id: '1zpresso_kultra',
    name: '1Zpresso K-Ultra',
    isManual: true,
    getSetting: (microns) {
      if (microns <= 400) return '2.5 - 4.0 angka';
      if (microns <= 600) return '4.5 - 6.0 angka';
      if (microns <= 800) return '6.5 - 8.0 angka';
      if (microns <= 1000) return '8.5 - 9.5 angka';
      if (microns <= 1200) return '9.5 - 10.5 angka';
      return '11.0 - 12.0 angka';
    },
  ),
  GrinderModel(
    id: 'vesper_vs3_fold',
    name: 'Vesper VS3 Fold',
    isManual: true,
    getSetting: (microns) {
      if (microns <= 400) return '15 - 28 ';
      if (microns <= 600) return '29 - 45 ';
      if (microns <= 800) return '46 - 65 ';
      if (microns <= 1000) return '66 - 85 ';
      if (microns <= 1200) return '86 - 105 ';
      return '106 - 120 ';
    },
  ),
  GrinderModel(
    id: 'vesper_lens',
    name: 'Vesper Lens',
    isManual: true,
    getSetting: (microns) {
      if (microns <= 400) return '8 - 15 ';
      if (microns <= 600) return '16 - 24 ';
      if (microns <= 800) return '25 - 35 ';
      if (microns <= 1000) return '36 - 44 ';
      if (microns <= 1200) return '45 - 50 ';
      return '51 - 54 ';
    },
  ),
  GrinderModel(
    id: 'kinu_m47',
    name: 'Kinu M47',
    isManual: true,
    getSetting: (microns) {
      if (microns <= 400) return '0.8 - 1.5 putaran';
      if (microns <= 600) return '2.0 - 2.8 putaran';
      if (microns <= 800) return '3.0 - 4.0 putaran';
      if (microns <= 1000) return '4.2 - 4.8 putaran';
      if (microns <= 1200) return '5.0 - 5.8 putaran';
      return '6.0 - 7.0 putaran';
    },
  ),
  GrinderModel(
    id: 'hario_skerton',
    name: 'Hario Skerton Pro',
    isManual: true,
    getSetting: (microns) {
      if (microns <= 400) return '2 - 3 ';
      if (microns <= 600) return '4 - 6 ';
      if (microns <= 800) return '7 - 9 ';
      if (microns <= 1000) return '10 - 12 ';
      if (microns <= 1200) return '13 - 15 ';
      return '16 - 18 ';
    },
  ),
  GrinderModel(
    id: 'porlex_mini',
    name: 'Porlex Mini',
    isManual: true,
    getSetting: (microns) {
      if (microns <= 400) return '3 - 5 ';
      if (microns <= 600) return '6 - 8 ';
      if (microns <= 800) return '9 - 11 ';
      if (microns <= 1000) return '12 - 14 ';
      if (microns <= 1200) return '15 - 17 ';
      return '18 - 20 ';
    },
  ),

  // Electric Grinders
  GrinderModel(
    id: 'baratza_encore',
    name: 'Baratza Encore',
    isManual: false,
    getSetting: (microns) {
      if (microns <= 400) return '5 - 9';
      if (microns <= 600) return '10 - 14';
      if (microns <= 800) return '15 - 22';
      if (microns <= 1000) return '23 - 27';
      if (microns <= 1200) return '28 - 32';
      return '33 - 40';
    },
  ),
  GrinderModel(
    id: 'fellow_ode_gen2',
    name: 'Fellow Ode Gen 2',
    isManual: false,
    getSetting: (microns) {
      if (microns <= 400) return '1 - 2 (Not Espresso)';
      if (microns <= 600) return '3 - 4';
      if (microns <= 800) return '5 - 7';
      if (microns <= 1000) return '7.5 - 8.5';
      if (microns <= 1200) return '9 - 10';
      return '11';
    },
  ),
  GrinderModel(
    id: 'niche_zero',
    name: 'Niche Zero',
    isManual: false,
    getSetting: (microns) {
      if (microns <= 400) return '10 - 20';
      if (microns <= 600) return '25 - 35';
      if (microns <= 800) return '40 - 50';
      if (microns <= 1000) return '55 - 65';
      if (microns <= 1200) return '70 - 80';
      return '85 - 100';
    },
  ),
  GrinderModel(
    id: 'eureka_mignon',
    name: 'Eureka Mignon',
    isManual: false,
    getSetting: (microns) {
      if (microns <= 400) return '0.5 - 1.5 putaran';
      if (microns <= 600) return '1.5 - 2.5 putaran';
      if (microns <= 800) return '2.5 - 3.5 putaran';
      if (microns <= 1000) return '3.5 - 4.5 putaran';
      if (microns <= 1200) return '4.5 - 5.5 putaran';
      return '6.0+ putaran';
    },
  ),
  GrinderModel(
    id: 'df64',
    name: 'Turin DF64',
    isManual: false,
    getSetting: (microns) {
      if (microns <= 400) return '10 - 20 angka';
      if (microns <= 600) return '25 - 40 angka';
      if (microns <= 800) return '45 - 65 angka';
      if (microns <= 1000) return '70 - 85 angka';
      if (microns <= 1200) return '90 - 100 angka';
      return '100+ angka';
    },
  ),
  GrinderModel(
    id: 'wilfa_svart',
    name: 'Wilfa Svart',
    isManual: false,
    getSetting: (microns) {
      if (microns <= 400) return 'Aeropress (Fine)';
      if (microns <= 600) return 'Aeropress';
      if (microns <= 800) return 'Filter';
      if (microns <= 1000) return 'Filter (Coarse)';
      if (microns <= 1200) return 'French Press';
      return 'Steep';
    },
  ),
  GrinderModel(
    id: 'baratza_sette',
    name: 'Baratza Sette 270',
    isManual: false,
    getSetting: (microns) {
      if (microns <= 400) return '5E - 9E';
      if (microns <= 600) return '12A - 15A';
      if (microns <= 800) return '20 - 25';
      if (microns <= 1000) return '26 - 31';
      if (microns <= 1200) return 'Not Recommended';
      return 'Not Recommended';
    },
  ),
  GrinderModel(
    id: 'breville_sgp',
    name: 'Breville Smart Grinder Pro',
    isManual: false,
    getSetting: (microns) {
      if (microns <= 400) return '10 - 20';
      if (microns <= 600) return '25 - 35';
      if (microns <= 800) return '40 - 50';
      if (microns <= 1000) return '50 - 55';
      if (microns <= 1200) return '55 - 60';
      return '60 (Max)';
    },
  ),
  GrinderModel(
    id: 'lagom_p64',
    name: 'Option-O Lagom P64',
    isManual: false,
    getSetting: (microns) {
      if (microns <= 400) return '0.5 - 1.5 angka';
      if (microns <= 600) return '2.0 - 3.5 angka';
      if (microns <= 800) return '4.0 - 6.0 angka';
      if (microns <= 1000) return '6.5 - 8.0 angka';
      if (microns <= 1200) return '8.5 - 9.5 angka';
      return '9.5 - 10.0 angka';
    },
  ),
  GrinderModel(
    id: 'mahlkonig_ek43',
    name: 'Mahlkönig EK43',
    isManual: false,
    getSetting: (microns) {
      if (microns <= 400) return '1.5 - 3.0';
      if (microns <= 600) return '4.0 - 6.0';
      if (microns <= 800) return '7.0 - 9.5';
      if (microns <= 1000) return '10.0 - 12.0';
      if (microns <= 1200) return '13.0 - 15.0';
      return '15.0 - 16.0';
    },
  ),
];

String getGrindCategoryName(int microns, String lang) {
  if (microns <= 400) return AppStrings.str(lang, 'custom_grind_400');
  if (microns <= 600) return AppStrings.str(lang, 'custom_grind_600');
  if (microns <= 800) return AppStrings.str(lang, 'custom_grind_800');
  if (microns <= 1000) return AppStrings.str(lang, 'custom_grind_1000');
  if (microns <= 1200) return AppStrings.str(lang, 'custom_grind_1200');
  return AppStrings.str(lang, 'custom_grind_1400');
}
