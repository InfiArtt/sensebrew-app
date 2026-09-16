import re

with open('lib/core/timer_state.dart', 'r', encoding='utf-8') as f:
    text = f.read()

# Change back to assistanceAccessibility to ensure it punches through the SCO routing
text = re.sub(
    r'contentType: AndroidContentType\.music,(\s*)usageType: AndroidUsageType\.media,(\s*)audioFocus: AndroidAudioFocus\.none,',
    r'contentType: AndroidContentType.speech,\1usageType: AndroidUsageType.assistanceAccessibility,\2audioFocus: AndroidAudioFocus.gainTransientMayDuck,',
    text, flags=re.DOTALL
)

with open('lib/core/timer_state.dart', 'w', encoding='utf-8') as f:
    f.write(text)

print("Changed to assistanceAccessibility and speech.")
