import 'dart:io';

void main() {
  final result = Process.runSync('C:\\Users\\Administrator\\AppData\\Local\\Android\\Sdk\\platform-tools\\adb.exe', ['shell', 'run-as', 'com.example.v60_blind_guide', 'cat', 'shared_prefs/FlutterSharedPreferences.xml']);
  final xml = result.stdout as String;
  print(xml.substring(0, 300));
}
