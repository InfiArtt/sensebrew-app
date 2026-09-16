import 'package:flutter/material.dart';
import 'package:flutter/semantics.dart';
import 'package:provider/provider.dart';
import '../core/calibration_state.dart';
import '../core/timer_state.dart';
import '../core/recipe.dart';
import '../core/settings_state.dart';
import '../core/app_strings.dart';
import 'calibration_screen.dart';
import 'brewing_screen.dart';
import 'custom_recipe_screen.dart';
import 'settings_screen.dart';
import 'method_recipe_screen.dart';
import 'pour_calculator_screen.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {

  Widget _buildMethodCard(BuildContext context, BrewMethod method, String name, String desc, IconData icon) {
    return Card(
      margin: const EdgeInsets.only(bottom: 12, left: 16, right: 16),
      child: Semantics(
        excludeSemantics: true,
        label: '$name. $desc',
        child: ListTile(
          leading: Icon(icon, size: 40),
          title: Text(name, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 18)),
          subtitle: Text(desc),
          onTap: () {
            Navigator.push(
              context,
              MaterialPageRoute(builder: (_) => MethodRecipeScreen(method: method, methodName: name)),
            );
          },
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final settings = Provider.of<SettingsState>(context);
    final audio = Provider.of<TimerAudioState>(context, listen: false);
    final lang = settings.appLanguage;
    
    audio.applySettings(
      settings.appLanguage, 
      settings.ttsSpeed, 
      settings.isTtsEnabled, 
      settings.audioOutputMode,
      settings.ttsPitch,
      settings.ttsVolume,
      settings.ttsVoiceName,
      settings.ttsVoiceLocale,
      settings.hapticMetronome,
      settings.audioMetronome,
    );
    
    return Scaffold(
      appBar: AppBar(
        title: Text(AppStrings.str(lang, 'app_title') ?? 'SenseBrew'),
        excludeHeaderSemantics: true,
        actions: [
          IconButton(
            icon: const Icon(Icons.settings),
            tooltip: AppStrings.str(lang, 'settings_menu'),
            onPressed: () {
              Navigator.push(
                context,
                MaterialPageRoute(builder: (_) => const SettingsScreen()),
              );
            },
          )
        ],
      ),
      body: Consumer<CalibrationState>(
        builder: (context, calibration, child) {
          final isCalibrated = calibration.isCalibrated;
          return Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              Padding(
                padding: const EdgeInsets.all(16.0),
                child: Semantics(
                  label: isCalibrated 
                    ? '${AppStrings.str(lang, 'calibrate_flow_rate')}. ${AppStrings.str(lang, 'calibrated_status', [calibration.mlPerSecond.toStringAsFixed(1)])}'
                    : '${AppStrings.str(lang, 'calibrate_flow_rate')}. ${AppStrings.str(lang, 'uncalibrated_status')}',
                  button: true,
                  excludeSemantics: true, child: ElevatedButton.icon(
                    icon: const Icon(Icons.water_drop),
                    label: Text(
                      isCalibrated 
                        ? AppStrings.str(lang, 'calibrated_btn', [calibration.mlPerSecond.toStringAsFixed(1)]) 
                        : '${AppStrings.str(lang, 'calibrate_flow_rate')}\n${AppStrings.str(lang, 'uncalibrated_btn')}',
                      textAlign: TextAlign.center,
                    ),
                    style: ElevatedButton.styleFrom(
                      padding: const EdgeInsets.symmetric(vertical: 24, horizontal: 32),
                      backgroundColor: isCalibrated ? Colors.green : Colors.red,
                      foregroundColor: Colors.white,
                    ),
                    onPressed: () {
                      Navigator.push(
                        context,
                        MaterialPageRoute(builder: (_) => const CalibrationScreen()),
                      );
                    },
                  ),
                ),
              ),
              Padding(
                padding: const EdgeInsets.symmetric(horizontal: 16.0),
                child: ElevatedButton.icon(
                  icon: const Icon(Icons.calculate),
                  label: Text(
                    AppStrings.str(lang, 'pour_calc_title') ?? 'Kalkulator Tuang',
                    textAlign: TextAlign.center,
                    style: const TextStyle(fontSize: 18),
                  ),
                  style: ElevatedButton.styleFrom(
                    padding: const EdgeInsets.symmetric(vertical: 18),
                    backgroundColor: Colors.teal,
                    foregroundColor: Colors.white,
                  ),
                  onPressed: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(builder: (_) => PourCalculatorScreen(lang: lang)),
                    );
                  },
                ),
              ),
              const SizedBox(height: 16),
              Padding(
                padding: const EdgeInsets.symmetric(horizontal: 16.0, vertical: 8.0),
                child: Text(AppStrings.str(lang, 'home_select_method'), style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
              ),
              Expanded(
                child: SingleChildScrollView(child: Column(
                  children: [
                    _buildMethodCard(context, BrewMethod.v60, "V60 / Pour-over", AppStrings.str(lang, 'method_v60_desc'), Icons.filter_alt),
                    _buildMethodCard(context, BrewMethod.frenchPress, "French Press", AppStrings.str(lang, 'method_fp_desc'), Icons.coffee),
                    _buildMethodCard(context, BrewMethod.aeropress, "Aeropress", AppStrings.str(lang, 'method_ap_desc'), Icons.local_cafe),
                    _buildMethodCard(context, BrewMethod.vietnamDrip, "Vietnam Drip", AppStrings.str(lang, 'method_vd_desc'), Icons.coffee_maker),
                    _buildMethodCard(context, BrewMethod.cupping, "SCA Cupping Protocol", AppStrings.str(lang, 'method_cup_desc'), Icons.emoji_food_beverage),
                  ],
                )),
              ),
            ],
          );
        },
      ),
    );
  }
}



