import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

class CalibrationState extends ChangeNotifier {
  double _mlPerSecond = 0.0;
  double _secondsPerRotation = 2.0;
  bool _isCalibrated = false;

  int _lastVolume = 150;
  int _lastSeconds = 20;

  double _spoonCapacityGrams = 10.0;
  String _grinderId = 'timemore_c2';

  double get mlPerSecond => _mlPerSecond;
  double get secondsPerRotation => _secondsPerRotation;
  bool get isCalibrated => _isCalibrated;
  
  int get lastVolume => _lastVolume;
  int get lastSeconds => _lastSeconds;
  
  double get spoonCapacityGrams => _spoonCapacityGrams;
  String get grinderId => _grinderId;

  CalibrationState() {
    _loadCalibration();
  }

  Future<void> _loadCalibration() async {
    final prefs = await SharedPreferences.getInstance();
    _mlPerSecond = prefs.getDouble('ml_per_second') ?? 0.0;
    _secondsPerRotation = prefs.getDouble('seconds_per_rotation') ?? 2.0;
    _isCalibrated = prefs.getBool('is_calibrated') ?? false;
    _lastVolume = prefs.getInt('last_volume') ?? 150;
    _lastSeconds = prefs.getInt('last_seconds') ?? 20;
    _spoonCapacityGrams = prefs.getDouble('spoon_capacity') ?? 10.0;
    _grinderId = prefs.getString('grinder_id') ?? 'timemore_c2';
    notifyListeners();
  }

  Future<void> saveCalibration(double targetVolumeMl, int totalSeconds, int secondsPerRotation, double spoonCapacity, String grinderId) async {
    _mlPerSecond = targetVolumeMl / totalSeconds;
    _secondsPerRotation = secondsPerRotation.toDouble();
    _lastVolume = targetVolumeMl.toInt();
    _lastSeconds = totalSeconds;
    _spoonCapacityGrams = spoonCapacity;
    _grinderId = grinderId;
    _isCalibrated = true;
    
    final prefs = await SharedPreferences.getInstance();
    await prefs.setDouble('ml_per_second', _mlPerSecond);
    await prefs.setDouble('seconds_per_rotation', _secondsPerRotation);
    await prefs.setBool('is_calibrated', true);
    await prefs.setInt('last_volume', _lastVolume);
    await prefs.setInt('last_seconds', _lastSeconds);
    await prefs.setDouble('spoon_capacity', _spoonCapacityGrams);
    await prefs.setString('grinder_id', _grinderId);
    
    notifyListeners();
  }
}
