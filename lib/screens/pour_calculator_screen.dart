import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'dart:async';
import '../core/app_strings.dart';
import '../core/calibration_state.dart';
import '../core/settings_state.dart';
import '../core/timer_state.dart';
import 'package:wakelock_plus/wakelock_plus.dart';
import 'package:flutter/semantics.dart';
import '../widgets/native_text_field.dart';


class PourCalculatorScreen extends StatefulWidget {
  final String lang;
  const PourCalculatorScreen({super.key, required this.lang});

  @override
  _PourCalculatorScreenState createState() => _PourCalculatorScreenState();
}

class _PourCalculatorScreenState extends State<PourCalculatorScreen> {
  int _targetMl = 50;
  bool _isPlaying = false;
  bool _isCountdown = false;
  int _counter = 0;
  Timer? _timer;
  
  late TextEditingController _mlController;

  @override
  void initState() {
    super.initState();
    _mlController = TextEditingController(text: _targetMl.toString());
  }

  @override
  void dispose() {
    _timer?.cancel();
    final timerAudio = Provider.of<TimerAudioState>(context, listen: false);
    timerAudio.stopMetronome();
    WakelockPlus.disable();
    _mlController.dispose();
    super.dispose();
  }
  
  void _startPour() async {
    final timerAudio = Provider.of<TimerAudioState>(context, listen: false);
    
    if (_isPlaying) {
      _stopPour();
      return;
    }
    
    final calibration = Provider.of<CalibrationState>(context, listen: false);
    if (calibration.mlPerSecond <= 0) return;
    
    int estTime = (_targetMl / calibration.mlPerSecond).round();
    if (estTime <= 0) estTime = 1;

    WakelockPlus.enable();

    setState(() {
      _isPlaying = true;
      _isCountdown = true;
      _counter = 3;
    });

    await timerAudio.speak(AppStrings.str(widget.lang, 'pour_calc_ready') ?? 'Siap-siap');

    final stopwatch = Stopwatch()..start();
    int lastProjectedSecond = -1;
    int lastActualSecond = -1;
    final settings = Provider.of<SettingsState>(context, listen: false);
    int ttsOffsetMs = 0;

    _timer = Timer.periodic(const Duration(milliseconds: 50), (timer) {
      if (!mounted) return;

      int elapsedMs = stopwatch.elapsedMilliseconds;
      int projectedMs = elapsedMs + ttsOffsetMs;
      int projectedSec = (projectedMs / 1000).floor();
      int actualSec = (elapsedMs / 1000).floor();

      // Handle TTS (Projected Time)
      if (projectedSec > lastProjectedSecond) {
        lastProjectedSecond = projectedSec;
        
        if (_isCountdown) {
          int count = 3 - projectedSec;
          if (count > 0 && count <= 3) {
            timerAudio.speak(count.toString());
          } else if (count == 0) {
            timerAudio.speak(widget.lang == 'en' ? 'Start!' : 'Mulai!');
          }
        } else {
          int remaining = estTime - (projectedSec - 4); // 4 seconds of countdown (0,1,2,3)
          if (remaining == 0) {
            timerAudio.speak(AppStrings.str(widget.lang, 'pour_calc_stop') ?? 'Berhenti');
          }
        }
      }

      // Handle UI & Metronome (Actual Time)
      if (actualSec > lastActualSecond) {
        lastActualSecond = actualSec;
        
        setState(() {
          if (_isCountdown) {
            int count = 3 - actualSec;
            if (count > 0) {
              _counter = count;
            } else if (count == 0) {
              _isCountdown = false;
              _counter = estTime;
              
              if (settings.audioMetronome) {
                timerAudio.startMetronome(
                  tickIntervalSeconds: 1.0,
                  onTick: (beat) {}
                );
              }
            }
          } else {
            int remaining = estTime - (actualSec - 4);
            if (remaining > 0) {
              _counter = remaining;
            } else {
              _stopPour();
            }
          }
        });
      }
    });
  }
  
  void _stopPour() {
    _timer?.cancel();
    final timerAudio = Provider.of<TimerAudioState>(context, listen: false);
    timerAudio.stopMetronome();
    WakelockPlus.disable();
    setState(() {
      _isPlaying = false;
      _isCountdown = false;
      _counter = 0;
    });
  }

  void _adjustVolume(int delta) {
    if (_isPlaying) return;
    setState(() {
      _targetMl += delta;
      if (_targetMl < 10) _targetMl = 10;
      if (_targetMl > 1000) _targetMl = 1000;
      _mlController.text = _targetMl.toString();
    });
  }
  
  void _onMlChanged(String value) {
    if (_isPlaying) return;
    int? parsed = int.tryParse(value);
    if (parsed != null) {
      setState(() {
        _targetMl = parsed;
        if (_targetMl < 10) _targetMl = 10;
        if (_targetMl > 1000) _targetMl = 1000;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    final calibration = Provider.of<CalibrationState>(context);
    final settings = Provider.of<SettingsState>(context);
    final timerAudio = Provider.of<TimerAudioState>(context);
    
    int estTime = 0;
    if (calibration.mlPerSecond > 0) {
      estTime = (_targetMl / calibration.mlPerSecond).round();
    }

    return Scaffold(
      backgroundColor: _isPlaying && !_isCountdown && timerAudio.isRunning && settings.visualMetronome
          ? (timerAudio.beats % 2 == 0 ? Colors.brown.shade100 : Theme.of(context).scaffoldBackgroundColor)
          : null,
      appBar: AppBar(
        title: Text(AppStrings.str(widget.lang, 'pour_calc_title') ?? 'Kalkulator Tuang'),
      ),
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              Text(
                AppStrings.str(widget.lang, 'pour_calc_desc') ?? '',
                style: const TextStyle(fontSize: 16),
              ),
              const SizedBox(height: 24),
              
              if (!calibration.isCalibrated)
                Container(
                  padding: const EdgeInsets.all(16),
                  color: Colors.red.shade100,
                  child: Text(
                    widget.lang == 'en' ? 'Please calibrate your kettle first in the Home screen.' : 'Harap kalibrasi teko Anda terlebih dahulu di layar Utama.',
                    style: TextStyle(fontSize: 18, color: Colors.red.shade900, fontWeight: FontWeight.bold),
                  ),
                )
              else ...[
                Text(
                  AppStrings.str(widget.lang, 'pour_calc_target') ?? 'Target Tuangan (ml)',
                  style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                  textAlign: TextAlign.center,
                ),
                const SizedBox(height: 16),
                
                // Volume Adjuster
                Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    IconButton(
                      icon: const Icon(Icons.remove_circle_outline),
                      iconSize: 48,
                      color: Theme.of(context).primaryColor,
                      tooltip: AppStrings.str(widget.lang, 'reduce', [(_targetMl - 10).toString(), 'ml']),
                      onPressed: _isPlaying ? null : () => _adjustVolume(-10),
                    ),
                    const SizedBox(width: 20),
                    Semantics(
                      sortKey: const OrdinalSortKey(2.0),
                      child: SizedBox(
                        width: 160,
                        child: NativeTextField(
                          label: 'ml',
                          value: _targetMl.toString(),
                          isNumber: true,
                          onChanged: _onMlChanged,
                        ),
                      ),
                    ),

                    const SizedBox(width: 20),
                    IconButton(
                      icon: const Icon(Icons.add_circle_outline),
                      iconSize: 48,
                      color: Theme.of(context).primaryColor,
                      tooltip: AppStrings.str(widget.lang, 'add', [(_targetMl + 10).toString(), 'ml']),
                      onPressed: _isPlaying ? null : () => _adjustVolume(10),
                    ),
                  ],
                ),
                
                const SizedBox(height: 32),
                
                // Estimated Time
                Text(
                  AppStrings.str(widget.lang, 'pour_calc_est', [estTime.toString()]) ?? 'Estimasi Waktu: $estTime detik',
                  style: const TextStyle(fontSize: 22, fontWeight: FontWeight.bold, color: Colors.blueGrey),
                  textAlign: TextAlign.center,
                ),
                
                const SizedBox(height: 32),
                
                // Play/Stop Button
                ElevatedButton.icon(
                  style: ElevatedButton.styleFrom(
                    padding: const EdgeInsets.symmetric(vertical: 24),
                    backgroundColor: _isPlaying ? Colors.red.shade100 : Theme.of(context).primaryColorLight,
                  ),
                  icon: Icon(_isPlaying ? Icons.stop : Icons.play_arrow, size: 36, color: _isPlaying ? Colors.red.shade900 : Theme.of(context).primaryColorDark),
                  label: Text(
                    _isPlaying 
                      ? (_isCountdown ? "$_counter" : "$_counter s")
                      : (AppStrings.str(widget.lang, 'pour_calc_start') ?? 'Mulai Tuang'),
                    style: TextStyle(fontSize: 24, color: _isPlaying ? Colors.red.shade900 : Theme.of(context).primaryColorDark),
                  ),
                  onPressed: _startPour,
                ),
              ],
            ],
          ),
        ),
      ),
    );
  }
}
