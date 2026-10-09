import 'package:flutter/material.dart';
import 'package:flutter/semantics.dart';
import '../core/recipe.dart';

/// Generates a 4:6 recipe with adjusted taste and strength.
///
/// [rasa]     : -2 (very sour) .. 0 (balanced) .. +2 (very sweet)
/// [kekuatan] : -1 (light/2 pours) .. 0 (standard/3 pours) .. +1 (bold/4 pours)
Recipe generate46Recipe(Recipe base, int rasa, int kekuatan) {
  final double totalWater = base.totalWaterMl;
  final double frontBlock = totalWater * 0.40; // 40% → taste
  final double backBlock = totalWater * 0.60;  // 60% → strength

  // --- FRONT BLOCK: 2 pours, ratio controlled by [rasa] ---
  // rasa -2: first=30%, second=70%  (very sweet)
  // rasa  0: first=50%, second=50%  (balanced)
  // rasa +2: first=70%, second=30%  (very sour)
  final double firstRatio = 0.50 + (rasa * 0.10); // maps -2..+2 → 0.30..0.70
  final double pour1 = (frontBlock * firstRatio).roundToDouble();
  final double pour2 = (frontBlock - pour1).roundToDouble();

  // --- BACK BLOCK: 2, 3, or 4 pours controlled by [kekuatan] ---
  final int backPourCount = kekuatan == -1 ? 2 : (kekuatan == 0 ? 3 : 4);
  final double perBackPour =
      (backBlock / backPourCount * 2).round() / 2; // round to 0.5ml

  // Dynamically calculate interval based on AI's recipe spacing
    int interval = 45;
    if (base.phases.length >= 2) {
      int firstGap = base.phases[1].startTimeSeconds - base.phases[0].startTimeSeconds;
      if (firstGap > 15 && firstGap <= 90) {
        interval = firstGap;
      }
    }

    // Build phases using dynamic interval
    final List<RecipePhase> phases = [];
    int t = 0;

    // Phase 1 & 2 (front block)
    phases.add(RecipePhase(
      startTimeSeconds: t,
      pourAmountMl: pour1,
      action: PhaseAction.pourCircle,
    ));
    t += interval;
    phases.add(RecipePhase(
      startTimeSeconds: t,
      pourAmountMl: pour2,
      action: PhaseAction.pourCircle,
    ));
    t += interval;

    // Back block pours
    for (int i = 0; i < backPourCount; i++) {
      phases.add(RecipePhase(
        startTimeSeconds: t,
        pourAmountMl: perBackPour,
        action: PhaseAction.pourCircle,
      ));
      t += interval;
    }

    // totalDuration = last pour start + interval drawdown
    final int totalDuration = t;

  return base.copyWith(phases: phases, totalDurationSeconds: totalDuration);
}

/// Bottom sheet that shows the Flavor Dial UI for the 4:6 method.
/// Returns a [Recipe] with adjusted phases, or null if user cancelled.
Future<Recipe?> showFlavorDialSheet(
    BuildContext context, Recipe base, String lang) {
  return showModalBottomSheet<Recipe>(
    context: context,
    isScrollControlled: true,
    useSafeArea: true,
    shape: const RoundedRectangleBorder(
      borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
    ),
    builder: (_) => _FlavorDialSheet(base: base, lang: lang),
  );
}

class _FlavorDialSheet extends StatefulWidget {
  final Recipe base;
  final String lang;
  const _FlavorDialSheet({required this.base, required this.lang});

  @override
  State<_FlavorDialSheet> createState() => _FlavorDialSheetState();
}

class _FlavorDialSheetState extends State<_FlavorDialSheet> {
  int _rasa = 0;      // -2 .. +2
  int _kekuatan = 0;  // -1 .. +1

  Recipe get _preview => generate46Recipe(widget.base, _rasa, _kekuatan);

  String _rasaLabel(String lang) {
    if (_rasa <= -2) return lang == 'en' ? 'Very Sweet' : 'Sangat Manis';
    if (_rasa == -1) return lang == 'en' ? 'Sweet' : 'Manis';
    if (_rasa == 0)  return lang == 'en' ? 'Balanced' : 'Seimbang';
    if (_rasa == 1)  return lang == 'en' ? 'Bright/Sour' : 'Cerah/Asam';
    return lang == 'en' ? 'Very Bright' : 'Sangat Cerah';
  }

  String _kekuatanLabel(String lang) {
    if (_kekuatan == -1) return lang == 'en' ? 'Light (2 pours)' : 'Ringan (2 tuangan)';
    if (_kekuatan == 0)  return lang == 'en' ? 'Standard (3 pours)' : 'Standar (3 tuangan)';
    return lang == 'en' ? 'Bold (4 pours)' : 'Kuat (4 tuangan)';
  }

  String _formatTime(int seconds) {
    final m = seconds ~/ 60;
    final s = seconds % 60;
    return '${m.toString().padLeft(2, '0')}:${s.toString().padLeft(2, '0')}';
  }

  @override
  Widget build(BuildContext context) {
    final lang = widget.lang;
    final preview = _preview;

    return Padding(
      padding: EdgeInsets.only(
        left: 20, right: 20, top: 20,
        bottom: MediaQuery.of(context).viewInsets.bottom + 24,
      ),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          // Header
          Center(
            child: Container(
              width: 40, height: 4,
              decoration: BoxDecoration(
                color: Colors.grey[400],
                borderRadius: BorderRadius.circular(2),
              ),
            ),
          ),
          const SizedBox(height: 16),
          Text(
            lang == 'en' ? '☕ Flavor Dial — 4:6 Method' : '☕ Atur Selera — Metode 4:6',
            style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            textAlign: TextAlign.center,
          ),
          const SizedBox(height: 4),
          Text(
            lang == 'en'
                ? 'Customize taste & strength before brewing'
                : 'Sesuaikan rasa & kekuatan sebelum seduh',
            style: TextStyle(fontSize: 13, color: Colors.grey[600]),
            textAlign: TextAlign.center,
          ),
          const SizedBox(height: 24),

                    // --- RASA DROPDOWN ---
          DropdownButtonFormField<int>(
            value: _rasa,
            decoration: InputDecoration(
              labelText: lang == 'en' ? 'Taste Profile' : 'Profil Rasa',
              border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
              contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
            ),
            items: [
              DropdownMenuItem(value: -2, child: Text(lang == 'en' ? 'Very Sweet' : 'Sangat Manis')),
              DropdownMenuItem(value: -1, child: Text(lang == 'en' ? 'Sweet' : 'Manis')),
              DropdownMenuItem(value: 0, child: Text(lang == 'en' ? 'Balanced' : 'Seimbang')),
              DropdownMenuItem(value: 1, child: Text(lang == 'en' ? 'Bright / Sour' : 'Cerah / Asam')),
              DropdownMenuItem(value: 2, child: Text(lang == 'en' ? 'Very Bright' : 'Sangat Cerah')),
            ],
            onChanged: (v) {
              if (v != null) {
                setState(() => _rasa = v);
                SemanticsService.announce(_rasaLabel(lang), TextDirection.ltr);
              }
            },
          ),

          const SizedBox(height: 20),

          // --- KEKUATAN DROPDOWN ---
          DropdownButtonFormField<int>(
            value: _kekuatan,
            decoration: InputDecoration(
              labelText: lang == 'en' ? 'Strength Profile' : 'Kekuatan Seduhan',
              border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
              contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
            ),
            items: [
              DropdownMenuItem(value: -1, child: Text(lang == 'en' ? 'Light (2 pours)' : 'Ringan (2 tuangan)')),
              DropdownMenuItem(value: 0, child: Text(lang == 'en' ? 'Standard (3 pours)' : 'Standar (3 tuangan)')),
              DropdownMenuItem(value: 1, child: Text(lang == 'en' ? 'Bold (4 pours)' : 'Kuat (4 tuangan)')),
            ],
            onChanged: (v) {
              if (v != null) {
                setState(() => _kekuatan = v);
                SemanticsService.announce(_kekuatanLabel(lang), TextDirection.ltr);
              }
            },
          ),

          const SizedBox(height: 8),

          // --- PHASE PREVIEW ---
          Semantics(
            label: lang == 'en' ? 'Pour plan preview' : 'Pratinjau rencana tuangan',
            child: Container(
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: Colors.grey[100],
                borderRadius: BorderRadius.circular(10),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    lang == 'en' ? 'Pour Plan Preview' : 'Rencana Tuangan',
                    style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 13),
                  ),
                  const SizedBox(height: 8),
                  ...preview.phases.asMap().entries.map((entry) {
                    final i = entry.key;
                    final phase = entry.value;
                    final isBack = i >= 2;
                    return Padding(
                      padding: const EdgeInsets.symmetric(vertical: 2),
                      child: Row(
                        children: [
                          Text(
                            _formatTime(phase.startTimeSeconds),
                            style: const TextStyle(
                                fontFamily: 'monospace',
                                fontSize: 13,
                                fontWeight: FontWeight.bold),
                          ),
                          const SizedBox(width: 10),
                          Container(
                            width: 8, height: 8,
                            decoration: BoxDecoration(
                              shape: BoxShape.circle,
                              color: isBack ? Colors.brown[800] : Colors.brown[400],
                            ),
                          ),
                          const SizedBox(width: 8),
                          Text(
                            '${phase.pourAmountMl.toStringAsFixed(0)} ml'
                            '${i < 2 ? (lang == 'en' ? ' (taste)' : ' (rasa)') : (lang == 'en' ? ' (strength)' : ' (kekuatan)')}',
                            style: TextStyle(
                              fontSize: 13,
                              color: isBack ? Colors.brown[800] : Colors.brown[500],
                            ),
                          ),
                        ],
                      ),
                    );
                  }),
                  const SizedBox(height: 6),
                  Text(
                    lang == 'en'
                        ? 'Total: ${preview.totalWaterMl.toStringAsFixed(0)} ml · Est. ${_formatTime(preview.totalDurationSeconds)}'
                        : 'Total: ${preview.totalWaterMl.toStringAsFixed(0)} ml · Estimasi ${_formatTime(preview.totalDurationSeconds)}',
                    style: TextStyle(fontSize: 12, color: Colors.grey[600]),
                  ),
                ],
              ),
            ),
          ),

          const SizedBox(height: 20),

          // --- ACTION BUTTONS ---
          Row(
            children: [
              Expanded(
                child: OutlinedButton(
                  onPressed: () => Navigator.pop(context, null),
                  child: Text(lang == 'en' ? 'Cancel' : 'Batal'),
                ),
              ),
              const SizedBox(width: 12),
              Expanded(
                flex: 2,
                child: Semantics(
                  button: true,
                  label: lang == 'en'
                      ? 'Start brewing with these settings'
                      : 'Mulai seduh dengan pengaturan ini',
                  child: ElevatedButton.icon(
                    icon: const Icon(Icons.play_arrow),
                    label: Text(lang == 'en' ? 'Brew!' : 'Seduh!',
                        style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Colors.brown,
                      foregroundColor: Colors.white,
                      padding: const EdgeInsets.symmetric(vertical: 14),
                    ),
                    onPressed: () => Navigator.pop(context, _preview),
                  ),
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }
}
