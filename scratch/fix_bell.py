import re

with open('lib/core/timer_state.dart', 'r', encoding='utf-8') as f:
    code = f.read()

# Add _bellPlayer member
target_class = r'class TimerState extends ChangeNotifier \{'
replacement_class = r'''class TimerState extends ChangeNotifier {
  final AudioPlayer _bellPlayer = AudioPlayer();'''
code = re.sub(target_class, replacement_class, code, count=1)

# Fix playBell
target_bell = r'Future<void> playBell\(\) async \{\s*final bellPlayer = AudioPlayer\(\);\s*await bellPlayer\.play\(AssetSource\(\'bell\.wav\'\)\);\s*\}'
replacement_bell = r'''Future<void> playBell() async {
    await _bellPlayer.play(AssetSource('bell.wav'));
  }'''
code = re.sub(target_bell, replacement_bell, code)

with open('lib/core/timer_state.dart', 'w', encoding='utf-8') as f:
    f.write(code)

print('Timer state fixed!')
