import 'dart:async';
import 'package:flutter/material.dart';
import 'package:flutter/semantics.dart';
import 'package:provider/provider.dart';
import '../core/calibration_state.dart';
import '../core/timer_state.dart';
import '../core/settings_state.dart';
import '../core/app_strings.dart';
import '../core/grinder_database.dart';
import '../widgets/native_text_field.dart';

class CalibrationScreen extends StatefulWidget {
  const CalibrationScreen({super.key});

  @override
  State<CalibrationScreen> createState() => _CalibrationScreenState();
}

class _CalibrationScreenState extends State<CalibrationScreen> {
  int targetVolume = 200;
  int totalSeconds = 20;
  int secondsPerRotation = 2;
  double spoonCapacity = 10.0;
  String selectedGrinderId = grinderDatabase.first.id;




  @override
  void initState() {
    super.initState();
    final calibration = Provider.of<CalibrationState>(context, listen: false);
    targetVolume = calibration.lastVolume;
    totalSeconds = calibration.lastSeconds;
    secondsPerRotation = calibration.secondsPerRotation.toInt();
    spoonCapacity = calibration.spoonCapacityGrams;
    selectedGrinderId = calibration.grinderId;

    if (!grinderDatabase.any((g) => g.id == selectedGrinderId)) {
      selectedGrinderId = grinderDatabase.first.id;
    }
  }

  void _updateVol(int val) => setState(() => targetVolume = val);
  void _updateSec(int val) => setState(() => totalSeconds = val);
  void _updateRot(int val) => setState(() => secondsPerRotation = val);
  void _updateSpoon(int val) => setState(() => spoonCapacity = val.toDouble());

  @override
  Widget build(BuildContext context) {
    final timerAudio = Provider.of<TimerAudioState>(context);
    final settings = Provider.of<SettingsState>(context);
    final lang = settings.appLanguage;
    final bool isPlaying = timerAudio.isRunning;
    final String secLabel = lang == 'en' ? 'sec' : 'detik';

    return Scaffold(
      appBar: AppBar(
        title: Text(AppStrings.str(lang, 'calib_header')),
      ),
      body: SingleChildScrollView(padding: const EdgeInsets.all(16.0), child: Column(children: [
          Container(
            padding: const EdgeInsets.all(16.0),
            decoration: BoxDecoration(
              color: Colors.blue.shade50,
              borderRadius: BorderRadius.circular(8.0),
              border: Border.all(color: Colors.blue.shade200)
            ),
            child: Text(
              AppStrings.str(lang, 'calib_guide'),
              style: const TextStyle(fontSize: 18),
            ),
          ),
          const SizedBox(height: 32),
          ElevatedButton.icon(
            style: ElevatedButton.styleFrom(
              padding: const EdgeInsets.symmetric(vertical: 16),
              backgroundColor: isPlaying ? Colors.red.shade100 : Colors.blue.shade100,
            ),
            icon: Icon(isPlaying ? Icons.stop : Icons.play_arrow, size: 28),
            label: Text(isPlaying ? (AppStrings.str(lang, 'stop_metronome') ?? '') : (AppStrings.str(lang, 'calib_sim_btn')), style: const TextStyle(fontSize: 18)),
            onPressed: () {
              if (isPlaying) {
                timerAudio.stopMetronome();
              } else {
                int count = -3;
                Timer.periodic(const Duration(seconds: 1), (timer) {
                  if (!mounted) {
                    timer.cancel();
                    return;
                  }
                  if (count == -3) timerAudio.speak(lang == 'en' ? 'Three' : 'Tiga');
                  else if (count == -2) timerAudio.speak(lang == 'en' ? 'Two' : 'Dua');
                  else if (count == -1) timerAudio.speak(lang == 'en' ? 'One' : 'Satu');
                  else if (count == 0) {
                    timerAudio.speak(lang == 'en' ? 'Start' : 'Mulai');
                    timerAudio.startMetronome(tickIntervalSeconds: 1.0);
                    timer.cancel();
                  }
                  count++;
                });
              }
            },
          ),
          const SizedBox(height: 32),
          Text(AppStrings.str(lang, 'calib_grinder_select'), style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
          const SizedBox(height: 8),
          Card(
            margin: EdgeInsets.zero,
            child: ListTile(
              title: Text(grinderDatabase.firstWhere((g) => g.id == selectedGrinderId).name, style: const TextStyle(fontSize: 18)),
              trailing: const Icon(Icons.arrow_drop_down, size: 30),
              onTap: () {
                showModalBottomSheet(
                  context: context,
                  isScrollControlled: true,
                  builder: (ctx) {
                    return SafeArea(
                      child: Container(
                        padding: const EdgeInsets.symmetric(vertical: 8),
                        height: MediaQuery.of(context).size.height * 0.7,
                        child: Column(
                          children: [
                            Padding(
                              padding: const EdgeInsets.all(16.0),
                              child: Text(AppStrings.str(lang, 'calib_grinder_title'), style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
                            ),
                            Expanded(
                              child: ListView.builder(
                                itemCount: grinderDatabase.length,
                                itemBuilder: (ctx, i) {
                                  final g = grinderDatabase[i];
                                  return ListTile(
                                    title: Text(g.name, style: const TextStyle(fontSize: 18)),
                                    subtitle: Text(g.isManual ? (AppStrings.str(lang, 'calib_grinder_manual')) : (AppStrings.str(lang, 'calib_grinder_electric'))),
                                    onTap: () {
                                      setState(() {
                                        selectedGrinderId = g.id;
                                      });
                                      Navigator.pop(ctx);
                                    },
                                  );
                                }
                              ),
                            ),
                          ],
                        ),
                      ),
                    );
                  }
                );
              },
            ),
          ),
          
          const SizedBox(height: 24),
          Text(AppStrings.str(lang, 'calib_spoon_q'), style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
          const SizedBox(height: 8),
          _buildAdjuster(lang, spoonCapacity.toInt(), (val) => _updateSpoon(val), unit: "gram", minVal: 1, step: 1, semanticLabel: "gram"),

          const SizedBox(height: 24),
          Text(AppStrings.str(lang, 'calib_q1') ?? '', style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
          const SizedBox(height: 8),
          _buildAdjuster(lang, targetVolume, (val) => _updateVol(val), unit: "ml", minVal: 10, step: 10, semanticLabel: "ml"),
          
          const SizedBox(height: 24),
          Text(AppStrings.str(lang, 'calib_q2') ?? '', style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
          const SizedBox(height: 8),
          _buildAdjuster(lang, totalSeconds, (val) => _updateSec(val), unit: "TIK", minVal: 1, semanticLabel: "TIK"),

          const SizedBox(height: 24),
          Text(AppStrings.str(lang, 'calib_q3') ?? '', style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
          const SizedBox(height: 8),
          _buildAdjuster(lang, secondsPerRotation, (val) => _updateRot(val), unit: "TIK", minVal: 1, semanticLabel: "TIK"),


          const SizedBox(height: 32),
          ElevatedButton(
            style: ElevatedButton.styleFrom(
              backgroundColor: Colors.green,
              padding: const EdgeInsets.all(16),
            ),
            onPressed: () {
              timerAudio.stopMetronome();

              final calibration = Provider.of<CalibrationState>(context, listen: false);
              calibration.saveCalibration(targetVolume.toDouble(), totalSeconds, secondsPerRotation, spoonCapacity, selectedGrinderId);
              
              ScaffoldMessenger.of(context).showSnackBar(
                SnackBar(content: Text(AppStrings.str(lang, 'save_success') ?? '')),
              );
              Navigator.pop(context);
            },

            child: Text(AppStrings.str(lang, 'save_calib_label') ?? '', style: const TextStyle(fontSize: 24, color: Colors.white)),
          ),
        ],
      )),
    );
  }

  Widget _buildAdjuster(String lang, int currentValue, Function(int) onButtonChange, {int minVal = 10, int step = 1, required String unit, required String semanticLabel}) {
    return Semantics(
      explicitChildNodes: true,
      child: Row(
        children: [
          Semantics(
            sortKey: const OrdinalSortKey(1.0),
            child: IconButton(
              icon: const Icon(Icons.remove_circle, size: 48, color: Colors.red),
              tooltip: AppStrings.str(lang, 'reduce', [(currentValue - step).toString(), unit]),
              onPressed: () {
                if (currentValue - step >= minVal) {
                  onButtonChange(currentValue - step);
                }
              },
            ),
          ),
          Expanded(
            child: Semantics(
              sortKey: const OrdinalSortKey(2.0),
              child: NativeTextField(
                label: semanticLabel,
                value: currentValue.toString(),
                isNumber: true,
                onChanged: (val) {
                  final parsed = int.tryParse(val);
                  if (parsed != null && parsed >= minVal) {
                    onButtonChange(parsed);
                  }
                },
              ),
            ),
          ),
          const SizedBox(width: 8),
          ExcludeSemantics(
            child: Text(unit, style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
          ),
          const SizedBox(width: 8),
          Semantics(
            sortKey: const OrdinalSortKey(3.0),
            child: IconButton(
              icon: const Icon(Icons.add_circle, size: 48, color: Colors.green),
              tooltip: AppStrings.str(lang, 'add', [(currentValue + step).toString(), unit]),
              onPressed: () => onButtonChange(currentValue + step),
            ),
          ),
        ],
      ),
    );
  }
}
