import re

with open('lib/core/timer_state.dart', 'r', encoding='utf-8') as f:
    timer_code = f.read()

timer_code = timer_code.replace(
    "_audioPlayer.play(AssetSource('tick.wav'));",
    "_audioPlayer.seek(Duration.zero);\n        _audioPlayer.resume();"
)

with open('lib/core/timer_state.dart', 'w', encoding='utf-8') as f:
    f.write(timer_code)

print("Reverted to seek/resume for low latency.")
