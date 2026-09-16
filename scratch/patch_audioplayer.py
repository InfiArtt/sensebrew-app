import re

with open('lib/core/timer_state.dart', 'r', encoding='utf-8') as f:
    timer_code = f.read()

# 1. Change `final AudioPlayer _audioPlayer = AudioPlayer();` to `late AudioPlayer _audioPlayer;`
timer_code = timer_code.replace("final AudioPlayer _audioPlayer = AudioPlayer();", "late AudioPlayer _audioPlayer;")

# 2. Inside `_initTts()`, instantiate `_audioPlayer` right after setting global context
old_init = """    AudioPlayer.global.setAudioContext(audioContext);
    _audioPlayer.setAudioContext(audioContext);"""

new_init = """    AudioPlayer.global.setAudioContext(audioContext);
    _audioPlayer = AudioPlayer();
    _audioPlayer.setAudioContext(audioContext);"""
timer_code = timer_code.replace(old_init, new_init)

# 3. Change usageType to alarm
timer_code = timer_code.replace("usageType: AndroidUsageType.assistanceAccessibility,", "usageType: AndroidUsageType.alarm,")
timer_code = timer_code.replace("contentType: AndroidContentType.speech,", "contentType: AndroidContentType.sonification,")

with open('lib/core/timer_state.dart', 'w', encoding='utf-8') as f:
    f.write(timer_code)

print("Fixed TimerAudioState AudioPlayer instantiation and usage type.")
