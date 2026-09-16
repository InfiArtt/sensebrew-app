import 'package:flutter/material.dart';
import 'package:flutter/semantics.dart';
import 'package:provider/provider.dart';
import 'package:wakelock_plus/wakelock_plus.dart';
import 'dart:async';
import '../core/recipe.dart';
import '../core/timer_state.dart';
import '../core/calibration_state.dart';
import '../core/settings_state.dart';
import '../core/app_strings.dart';
import '../core/grinder_database.dart';

class BrewingScreen extends StatefulWidget {
  final Recipe recipe;
  const BrewingScreen({super.key, required this.recipe});

  @override
  State<BrewingScreen> createState() => _BrewingScreenState();
}

class _BrewingScreenState extends State<BrewingScreen> {
  Timer? _brewTimer;
  int _currentSecond = 0;
  bool _isBrewing = false;
  int _currentPhaseIndex = 0;
  int _currentPhaseStartSecond = 0;

  final FocusNode _cancelFocusNode = FocusNode();

  late TimerAudioState _timerAudio;
  late Recipe _activeRecipe;
  bool _isInitialized = false;

  @override
  void initState() {
    super.initState();
    _timerAudio = Provider.of<TimerAudioState>(context, listen: false);
  }

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    if (!_isInitialized) {
      _initDynamicRecipe();
      _isInitialized = true;
    }
  }

  void _initDynamicRecipe() {
    final calibration = Provider.of<CalibrationState>(context, listen: false);
    
    List<RecipePhase> dynamicPhases = [];
    int timeShift = 0;
    int lastEndSecond = 0;

    for (var phase in widget.recipe.phases) {
      int proposedStart = phase.startTimeSeconds + timeShift;
      
      if (proposedStart <= lastEndSecond && dynamicPhases.isNotEmpty) {
        int extraShift = lastEndSecond - proposedStart + 1; // 1 second gap for safety
        timeShift += extraShift;
        proposedStart += extraShift;
      }
      
      dynamicPhases.add(RecipePhase(
        startTimeSeconds: proposedStart,
        pourAmountMl: phase.pourAmountMl,
        instructionText: phase.instructionText,
        action: phase.action
      ));

      if (phase.action == PhaseAction.pourCircle || phase.action == PhaseAction.pourCenter) {
        int duration = (phase.pourAmountMl / calibration.mlPerSecond).round();
        lastEndSecond = proposedStart + duration;
      } else {
        lastEndSecond = proposedStart + 2; 
      }
    }
    
    int newTotalDuration = widget.recipe.totalDurationSeconds + timeShift;
    if (newTotalDuration < lastEndSecond) newTotalDuration = lastEndSecond;

    _activeRecipe = Recipe(
      name: widget.recipe.name,
      description: widget.recipe.description,
      coffeeGrams: widget.recipe.coffeeGrams,
      totalWaterMl: widget.recipe.totalWaterMl,
      extraIngredients: widget.recipe.extraIngredients,
      totalDurationSeconds: newTotalDuration,
      method: widget.recipe.method,
      targetGrindSizeMicrons: widget.recipe.targetGrindSizeMicrons,
      beanType: widget.recipe.beanType,
      phases: dynamicPhases,
    );
  }

  Future<void> _startBrewing() async {
    final calibration = Provider.of<CalibrationState>(context, listen: false);
    final settings = Provider.of<SettingsState>(context, listen: false);
    final lang = settings.appLanguage;
    final stopPourStr = lang == 'en' ? 'Stop and wait.' : 'Berhenti dan tunggu.';
    
    WakelockPlus.enable(); // Keep screen awake
    setState(() {
      _isBrewing = true;
      _currentSecond = -4; // Will hold at -4 while speaking
      _currentPhaseIndex = -1;
      _currentPhaseStartSecond = 0;
    });

    // Request focus on the cancel button so screen reader doesn't speak blindly
    WidgetsBinding.instance.addPostFrameCallback((_) {
      _cancelFocusNode.requestFocus();
    });

    if (_activeRecipe.phases.isNotEmpty) {
      final p = _activeRecipe.phases[0];
      if (p.action == PhaseAction.pourCircle || p.action == PhaseAction.pourCenter) {
         int actionDuration = (p.pourAmountMl / calibration.mlPerSecond).round();
         String prepText = "";
         if (p.action == PhaseAction.pourCircle) {
             double rotations = actionDuration / calibration.secondsPerRotation;
             double roundedRotations = (rotations * 2).round() / 2;
             String unit = lang == "en" ? "rotations" : "putaran"; String half = AppStrings.str(lang, "rotations_half") ?? " setengah"; String rotStr = (roundedRotations % 1 == 0) ? "${roundedRotations.toInt()} $unit" : "${roundedRotations.toStringAsFixed(1).replaceAll('.5', half).replaceAll('.0', '')} $unit";
             prepText = lang == 'en' ? "Prepare to pour, $rotStr." : "Siap-siap, tuang $rotStr.";
         } else {
             int actionDuration = (p.pourAmountMl / calibration.mlPerSecond).round();
             prepText = lang == 'en' ? "Prepare for center pour, $actionDuration seconds." : "Siap-siap, tuang tengah $actionDuration detik.";
         }
         await _timerAudio.speak(prepText);
      } else {
         await _timerAudio.speak(" "); // TTS Warm-up
      }
    } else {
      await _timerAudio.speak(" ");
    }

    if (!mounted || !_isBrewing) return; // In case user pressed stop while speaking

    _brewTimer = Timer.periodic(const Duration(seconds: 1), (timer) {
      if (!mounted) {
        timer.cancel();
        return;
      }
      setState(() {
        _currentSecond++;
      });
      
      if (_currentSecond > 0 && _currentSecond >= _activeRecipe.totalDurationSeconds) {
        _stopBrewing(finished: true, lang: lang);
        return;
      }

      int activeIdx = -1;
      for (int i = 0; i < _activeRecipe.phases.length; i++) {
         if (_currentSecond >= _activeRecipe.phases[i].startTimeSeconds) {
            activeIdx = i;
         }
      }
      
      if (activeIdx != -1 && activeIdx != _currentPhaseIndex) {
         _currentPhaseIndex = activeIdx;
         _currentPhaseStartSecond = _activeRecipe.phases[activeIdx].startTimeSeconds;
         _processPhase(activeIdx, _timerAudio, calibration, stopPourStr, lang);
      }

      for (int i = activeIdx + 1; i < _activeRecipe.phases.length; i++) {
        final p = _activeRecipe.phases[i];
        int timeUntil = p.startTimeSeconds - _currentSecond;
        if (timeUntil > 0 && timeUntil <= 5 && (p.action == PhaseAction.pourCircle || p.action == PhaseAction.pourCenter)) {
           // Skip countdown if gap from current phase is too short (< 6s)
           int currentPhaseEnd = _currentPhaseStartSecond;
           if (activeIdx != -1) {
             final currP = _activeRecipe.phases[activeIdx];
             if (currP.action == PhaseAction.pourCircle || currP.action == PhaseAction.pourCenter) {
                currentPhaseEnd += (currP.pourAmountMl / calibration.mlPerSecond).round();
             }
           }
           bool skipCountdown = activeIdx != -1 && (p.startTimeSeconds - currentPhaseEnd) < 6;

           if (!skipCountdown) {
             if (timeUntil == 5) {
                 if (p.action == PhaseAction.pourCircle) {
                    int actionDuration = (p.pourAmountMl / calibration.mlPerSecond).round();
                    double rotations = actionDuration / calibration.secondsPerRotation;
                    double roundedRotations = (rotations * 2).round() / 2;
                    String unit = lang == "en" ? "rotations" : "putaran"; String half = AppStrings.str(lang, "rotations_half") ?? " setengah"; String rotStr = (roundedRotations % 1 == 0) ? "${roundedRotations.toInt()} $unit" : "${roundedRotations.toStringAsFixed(1).replaceAll('.5', half).replaceAll('.0', '')} $unit";
                    _timerAudio.speak(lang == 'en' ? "Prepare to pour, $rotStr." : "Siap, tuang $rotStr.");
                 } else if (p.action == PhaseAction.pourCenter) {
                    int actionDuration = (p.pourAmountMl / calibration.mlPerSecond).round();
                    _timerAudio.speak(lang == 'en' ? "Prepare for center pour, $actionDuration seconds." : "Siap, tuang tengah $actionDuration detik.");
                 }
             } else if (timeUntil == 3) {
                 _timerAudio.speak(lang == 'en' ? "Three." : "Tiga.");
             } else if (timeUntil == 2) {
                 _timerAudio.speak(lang == 'en' ? "Two." : "Dua.");
             } else if (timeUntil == 1) {
                 _timerAudio.speak(lang == 'en' ? "One." : "Satu.");
             }
           }
        }
      }
    });
  }

  void _processPhase(int phaseIndex, TimerAudioState timerAudio, CalibrationState calibration, String stopStr, String lang) {
    final phase = _activeRecipe.phases[phaseIndex];
    int actionDuration = 0;

    if (phase.action == PhaseAction.pourCircle || phase.action == PhaseAction.pourCenter) {
      actionDuration = (phase.pourAmountMl / calibration.mlPerSecond).round();
      // If we skipped the 3-2-1 countdown due to short gap, let's say "Lanjut" instead of "Mulai"
      bool isContinuation = false;
      if (phaseIndex > 0) {
        final prevPhase = _activeRecipe.phases[phaseIndex - 1];
        int prevEnd = prevPhase.startTimeSeconds;
        if (prevPhase.action == PhaseAction.pourCircle || prevPhase.action == PhaseAction.pourCenter) {
           prevEnd += (prevPhase.pourAmountMl / calibration.mlPerSecond).round();
           if ((phase.startTimeSeconds - prevEnd) < 5) {
              isContinuation = true;
           }
        }
      }
      if (isContinuation) {
         if (phase.action == PhaseAction.pourCircle) {
             double rotations = actionDuration / calibration.secondsPerRotation;
             double roundedRotations = (rotations * 2).round() / 2;
             String unit = lang == "en" ? "rotations" : "putaran"; String half = AppStrings.str(lang, "rotations_half") ?? " setengah"; String rotStr = (roundedRotations % 1 == 0) ? "${roundedRotations.toInt()} $unit" : "${roundedRotations.toStringAsFixed(1).replaceAll('.5', half).replaceAll('.0', '')} $unit";
             timerAudio.speak(lang == 'en' ? "Continue, $rotStr." : "Lanjut tuang $rotStr.");
         } else {
             timerAudio.speak(lang == 'en' ? "Continue center pour, $actionDuration seconds." : "Lanjut tuang tengah, $actionDuration detik.");
         }
      } else {
         timerAudio.speak(lang == 'en' ? "Start!" : "Mulai!");
      }
    } else if (phase.action == PhaseAction.stir) {
      timerAudio.speak(AppStrings.str(lang, 'stir_instruction'));
    } else if (phase.action == PhaseAction.swirl) {
      timerAudio.speak(AppStrings.str(lang, 'action_swirl'));
    } else if (phase.action == PhaseAction.cap) {
      timerAudio.speak(AppStrings.str(lang, 'action_cap'));
    } else if (phase.action == PhaseAction.flip) {
      timerAudio.speak(lang == 'en' ? 'Carefully flip the Aeropress.' : 'Balikkan alat seduh dengan hati-hati.');
    } else if (phase.action == PhaseAction.press) {
      timerAudio.speak(AppStrings.str(lang, 'press_instruction') ?? 'Tekan perlahan.');
    } else if (phase.action == PhaseAction.openValve) {
      timerAudio.speak(AppStrings.str(lang, 'open_valve_instruction') ?? 'Buka switch atau keran.');
    } else if (phase.action == PhaseAction.closeValve) {
      timerAudio.speak(AppStrings.str(lang, 'close_valve_instruction') ?? 'Tutup switch atau keran.');
    } else if (phase.action == PhaseAction.wait) {
      if (phaseIndex > 0) {
        final prevPhase = _activeRecipe.phases[phaseIndex - 1];
        if (prevPhase.action == PhaseAction.stir || prevPhase.action == PhaseAction.swirl || prevPhase.action == PhaseAction.press || prevPhase.action == PhaseAction.cap || prevPhase.action == PhaseAction.flip) {
          timerAudio.speak(AppStrings.str(lang, 'action_wait'));
        }
      }
    }
    
    if (phase.action == PhaseAction.pourCircle || phase.action == PhaseAction.pourCenter) {
      int endPourSecond = _currentPhaseStartSecond + actionDuration;
      double interval = 1.0; // Flat 60 BPM clock for all methods
      timerAudio.startMetronome(
        tickIntervalSeconds: interval,
        onTick: (beat) {
          if (_currentPhaseIndex != phaseIndex) {
            timerAudio.stopMetronome();
            return;
          }
          
          if (_currentSecond >= endPourSecond) {
            if (_currentSecond == endPourSecond) {
               timerAudio.stopMetronome(); // Kill the 8th tick immediately!
               timerAudio.speak(lang == 'en' ? 'Stop.' : 'Berhenti.');
               
               // Plan the Tunggu command quietly
               Future.delayed(const Duration(seconds: 1), () {
                 if (mounted && _currentPhaseIndex == phaseIndex) {
                   timerAudio.speak(lang == 'en' ? 'Wait.' : 'Tunggu.');
                 }
               });
            }
          } else {
             int elapsed = _currentSecond - _currentPhaseStartSecond;
             if (phase.action == PhaseAction.pourCircle) {
                 if (elapsed > 0 && elapsed % calibration.secondsPerRotation == 0) {
                     int rot = elapsed ~/ calibration.secondsPerRotation;
                     timerAudio.speak(rot.toString());
                 }
             } else if (phase.action == PhaseAction.pourCenter) {
                 if (elapsed > 0 && elapsed % 10 == 0) {
                     timerAudio.speak(elapsed.toString());
                 }
             }
          }
        }
      );
    }
  }

  Future<void> _stopBrewing({bool finished = false, String lang = 'id'}) async {
    _brewTimer?.cancel();
    WakelockPlus.disable(); // Allow screen to sleep again
    if (mounted) {
      _timerAudio.stopMetronome();
      if (finished) {
        await _timerAudio.playBell();
        await Future.delayed(const Duration(milliseconds: 1000));
        _timerAudio.speak(AppStrings.str(lang, 'brew_complete') ?? 'Waktu seduh selesai. Selamat menikmati kopimu!');
      }
      setState(() {
        _isBrewing = false;
      });
    }
  }

  @override
  void dispose() {
    _cancelFocusNode.dispose();
    _brewTimer?.cancel();
    _timerAudio.stopMetronome();
    WakelockPlus.disable(); // Failsafe
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final calibration = Provider.of<CalibrationState>(context, listen: false);
    final settings = Provider.of<SettingsState>(context);
    final lang = settings.appLanguage;

    String currentPhaseText = "";
    if (_isBrewing && _currentPhaseIndex >= 0 && _currentPhaseIndex < _activeRecipe.phases.length) {
      final phase = _activeRecipe.phases[_currentPhaseIndex];
      
      if (phase.action == PhaseAction.pourCircle || phase.action == PhaseAction.pourCenter) {
        int pourDuration = (phase.pourAmountMl / calibration.mlPerSecond).round();
        int endPourSecond = _currentPhaseStartSecond + pourDuration;
        
        if (_currentSecond < endPourSecond) {
          if (phase.action == PhaseAction.pourCircle) {
            double rotations = pourDuration / calibration.secondsPerRotation;
            double roundedRotations = (rotations * 2).round() / 2;
            String rotStr = (roundedRotations % 1 == 0) ? "${roundedRotations.toInt()}" : roundedRotations.toStringAsFixed(1).replaceAll('.5', AppStrings.str(lang, 'rotations_half') ?? ' setengah').replaceAll('.0', '');
            currentPhaseText = AppStrings.str(lang, 'pour_circle_instruction', [phase.pourAmountMl.toStringAsFixed(0), rotStr]) ?? 'Tuang ${phase.pourAmountMl.toStringAsFixed(0)} mili, $rotStr putaran.';
          } else {
            currentPhaseText = AppStrings.str(lang, 'pour_center_instruction', [phase.pourAmountMl.toStringAsFixed(0), pourDuration.toString()]) ?? 'Tuang ${phase.pourAmountMl.toStringAsFixed(0)} selama $pourDuration detik';
          }
        } else {
          currentPhaseText = AppStrings.str(lang, 'wait_instruction') ?? 'Tunggu...';
        }
      } else if (phase.action == PhaseAction.stir) {
        currentPhaseText = AppStrings.str(lang, 'stir_instruction');
      } else if (phase.action == PhaseAction.swirl) {
        currentPhaseText = AppStrings.str(lang, 'action_swirl');
      } else if (phase.action == PhaseAction.cap) {
        currentPhaseText = AppStrings.str(lang, 'action_cap');
      } else if (phase.action == PhaseAction.flip) {
        currentPhaseText = lang == 'en' ? 'Flip Aeropress' : 'Balikkan Alat';
      } else if (phase.action == PhaseAction.press) {
        currentPhaseText = AppStrings.str(lang, 'press_instruction') ?? 'Tekan perlahan.';
      } else if (phase.action == PhaseAction.wait) {
        currentPhaseText = AppStrings.str(lang, 'wait_instruction') ?? 'Tunggu...';
      } else if (phase.action == PhaseAction.openValve) {
        currentPhaseText = AppStrings.str(lang, 'open_valve_instruction') ?? 'Buka switch atau keran.';
      } else if (phase.action == PhaseAction.closeValve) {
        currentPhaseText = AppStrings.str(lang, 'close_valve_instruction') ?? 'Tutup switch atau keran.';
      }
    }

    final timerAudio = Provider.of<TimerAudioState>(context);

    return Scaffold(
      backgroundColor: _isBrewing && timerAudio.isRunning && settings.visualMetronome
          ? (timerAudio.beats % 2 == 0 ? Colors.brown.shade100 : Theme.of(context).scaffoldBackgroundColor)
          : null,
      appBar: AppBar(title: Text(AppStrings.str(lang, widget.recipe.name))),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            if (_isBrewing) ...[
              Semantics(
                liveRegion: true,
                label: AppStrings.str(lang, 'brew_sec', [_currentSecond.toString(), currentPhaseText]),
                child: Column(
                  children: [
                    Text(
                      '$_currentSecond',
                      style: const TextStyle(fontSize: 120, fontWeight: FontWeight.bold),
                    ),
                    Text(
                      currentPhaseText,
                      style: const TextStyle(fontSize: 32, color: Colors.blue),
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 48),
              ElevatedButton(
                focusNode: _cancelFocusNode,
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.red,
                  padding: const EdgeInsets.symmetric(horizontal: 48, vertical: 24),
                ),
                onPressed: () {
                  _stopBrewing();
                  Navigator.pop(context);
                },
                child: Text(AppStrings.str(lang, 'cancel_brew_btn'), style: const TextStyle(fontSize: 24, color: Colors.white)),
              ),
            ] else ...[
              Expanded(
                child: SingleChildScrollView(padding: const EdgeInsets.all(16.0), child: Column(children: [
                    Semantics(
                      header: true,
                      label: AppStrings.str(lang, 'recipe_label', [AppStrings.str(lang, widget.recipe.name), widget.recipe.coffeeGrams.toString(), widget.recipe.totalWaterMl.toStringAsFixed(0)]),
                      excludeSemantics: true,
                      child: Text(
                        '\${AppStrings.str(lang, widget.recipe.name)}\n${widget.recipe.coffeeGrams}g ☕ | ${widget.recipe.totalWaterMl.toStringAsFixed(0)}ml 💧',
                        style: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
                        textAlign: TextAlign.center,
                      ),
                    ),
                    const SizedBox(height: 16),
                    Builder(
                      builder: (context) {
                        double spoonCount = widget.recipe.coffeeGrams / calibration.spoonCapacityGrams;
                        String spoonStr = spoonCount.toStringAsFixed(1).replaceAll(RegExp(r'\.0$'), '');
                        
                        String grindText = "${AppStrings.str(lang, 'brew_grind')}: ${getGrindCategoryName(widget.recipe.targetGrindSizeMicrons, lang)}";
                        var grinder = grinderDatabase.firstWhere((g) => g.id == calibration.grinderId, orElse: () => grinderDatabase.first);
                        String clickSetting = grinder.getSetting(widget.recipe.targetGrindSizeMicrons);
                        grindText += "\n${grinder.name}: $clickSetting";
                        
                        return Container(
                          padding: const EdgeInsets.all(12),
                          decoration: BoxDecoration(
                            color: Colors.blue.shade50,
                            borderRadius: BorderRadius.circular(8),
                            border: Border.all(color: Colors.blue.shade200),
                          ),
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(AppStrings.str(lang, 'brew_dose', [spoonStr]), style: const TextStyle(fontSize: 16, fontWeight: FontWeight.w600)),
                              const SizedBox(height: 4),
                              Text(grindText, style: const TextStyle(fontSize: 16, fontWeight: FontWeight.w600)),
                              const SizedBox(height: 4),
                              Text("${AppStrings.str(lang, 'brew_bean')}: ${widget.recipe.beanType}", style: const TextStyle(fontSize: 16, fontWeight: FontWeight.w600, color: Colors.brown)),
                              if (widget.recipe.extraIngredients.isNotEmpty) ...[
                                const SizedBox(height: 4),
                                Text("${AppStrings.str(lang, 'brew_extra')}: ${AppStrings.str(lang, widget.recipe.extraIngredients)}", style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: Colors.brown)),
                              ]
                            ],
                          ),
                        );
                      }
                    ),
                    const SizedBox(height: 16),
                      if (widget.recipe.description.isNotEmpty)
                        Semantics(
                          excludeSemantics: true,
                          label: "${AppStrings.str(lang, 'brew_desc_title')} ${AppStrings.str(lang, widget.recipe.description)}",
                          child: Container(
                            padding: const EdgeInsets.all(12),
                            decoration: BoxDecoration(
                              color: Colors.yellow.shade100,
                              borderRadius: BorderRadius.circular(8),
                            ),
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Text(AppStrings.str(lang, 'brew_desc_title'), style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Colors.brown)),
                                const SizedBox(height: 4),
                                Text(
                                  AppStrings.str(lang, widget.recipe.description),
                                  style: const TextStyle(fontSize: 16, fontStyle: FontStyle.italic),
                                ),
                              ]
                            )
                          ),
                        ),
                    const SizedBox(height: 16),
                    Text(AppStrings.str(lang, 'brew_phases'), style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
                    const SizedBox(height: 8),
                    ..._activeRecipe.phases.map((p) {
                      String itemText = "";
                      String amountStr = p.pourAmountMl == p.pourAmountMl.toInt() ? p.pourAmountMl.toInt().toString() : p.pourAmountMl.toStringAsFixed(1).replaceAll(RegExp(r'\.0$'), '');
                      
                      if (p.action == PhaseAction.pourCircle) {
                        int actionDuration = (p.pourAmountMl / calibration.mlPerSecond).round();
                        double rotations = actionDuration / calibration.secondsPerRotation;
                        double roundedRotations = (rotations * 2).round() / 2;
                        String rotStr = (roundedRotations % 1 == 0) ? "${roundedRotations.toInt()}" : roundedRotations.toStringAsFixed(1).replaceAll('.5', AppStrings.str(lang, 'rotations_half') ?? ' setengah').replaceAll('.0', '');
                        itemText = lang == 'en' ? 'Pour $amountStr ml ($rotStr rotations)' : 'Tuang $amountStr ml ($rotStr putaran)';
                      } else if (p.action == PhaseAction.pourCenter) {
                        int actionDuration = (p.pourAmountMl / calibration.mlPerSecond).round();
                        itemText = lang == 'en' ? 'Center pour $amountStr ml ($actionDuration sec)' : 'Tuang tengah $amountStr ml ($actionDuration detik)';
                      } else if (p.action == PhaseAction.stir) {
                        itemText = AppStrings.str(lang, 'action_stir');
                      } else if (p.action == PhaseAction.swirl) {
                        itemText = AppStrings.str(lang, 'action_swirl');
                      } else if (p.action == PhaseAction.cap) {
                        itemText = AppStrings.str(lang, 'action_cap');
                      } else if (p.action == PhaseAction.flip) {
                        itemText = lang == 'en' ? 'Flip Aeropress' : 'Balikkan Alat';
                      } else if (p.action == PhaseAction.press) {
                        itemText = lang == 'en' ? 'Press' : 'Tekan perlahan';
                      } else if (p.action == PhaseAction.wait) {
                        itemText = lang == 'en' ? 'Wait' : 'Tunggu...';
                      } else if (p.action == PhaseAction.openValve) {
                        itemText = lang == 'en' ? 'Open Valve/Switch' : 'Buka Keran/Switch';
                      } else if (p.action == PhaseAction.closeValve) {
                        itemText = lang == 'en' ? 'Close Valve/Switch' : 'Tutup Keran/Switch';
                      }

                      String timeStr = '${(p.startTimeSeconds ~/ 60).toString().padLeft(2, '0')}:${(p.startTimeSeconds % 60).toString().padLeft(2, '0')}';
                      return Semantics(
                        label: '$timeStr: $itemText',
                        excludeSemantics: true,
                        child: ListTile(
                          contentPadding: EdgeInsets.zero,
                          leading: Text(
                            timeStr,
                            style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold, color: _currentPhaseIndex >= _activeRecipe.phases.indexOf(p) ? Colors.blue : Colors.grey),
                          ),
                          title: Text(itemText, style: TextStyle(fontSize: 18, color: _currentPhaseIndex >= _activeRecipe.phases.indexOf(p) ? Colors.black : Colors.grey)),
                        ),
                      );
                    }),
                  ],
                )),
              ),
              Padding(
                padding: const EdgeInsets.all(16.0),
                child: ElevatedButton(
                  style: ElevatedButton.styleFrom(
                    backgroundColor: _currentSecond >= widget.recipe.totalDurationSeconds ? Colors.blue : Colors.green,
                    padding: const EdgeInsets.symmetric(horizontal: 48, vertical: 24),
                  ),
                  onPressed: () {
                    if (_currentSecond >= widget.recipe.totalDurationSeconds) {
                      Navigator.pop(context);
                    } else {
                      _startBrewing();
                    }
                  },
                  child: Text(
                    _currentSecond >= widget.recipe.totalDurationSeconds ? AppStrings.str(lang, 'finish_brew_btn') : AppStrings.str(lang, 'start_brew_btn'), 
                    style: const TextStyle(fontSize: 24, color: Colors.white)
                  ),
                ),
              ),
            ],
          ],
        ),
      ),
    );
  }
}
