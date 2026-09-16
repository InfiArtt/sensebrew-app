import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'core/calibration_state.dart';
import 'core/timer_state.dart';
import 'core/settings_state.dart';
import 'core/recipe_repository.dart';
import 'screens/home_screen.dart';

void main() {
  runApp(
    MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => CalibrationState()),
        ChangeNotifierProvider(create: (_) => TimerAudioState()),
        ChangeNotifierProvider(create: (_) => SettingsState()),
        ChangeNotifierProvider(create: (_) => RecipeRepository()..loadRecipes()),
      ],
      child: const V60BlindGuideApp(),
    ),
  );
}

class V60BlindGuideApp extends StatelessWidget {
  const V60BlindGuideApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'SenseBrew',
      theme: ThemeData(
        primarySwatch: Colors.brown,
        visualDensity: VisualDensity.adaptivePlatformDensity,
        textTheme: const TextTheme(
          displayLarge: TextStyle(fontSize: 48, fontWeight: FontWeight.bold),
          bodyLarge: TextStyle(fontSize: 24),
        ),
      ),
      home: const HomeScreen(),
    );
  }
}
