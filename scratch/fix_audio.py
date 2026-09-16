import re

with open('lib/core/timer_state.dart', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace usageType and contentType for the metronome context
text = re.sub(
    r'contentType: AndroidContentType\.music,(\s*)usageType: AndroidUsageType\.media,',
    r'contentType: AndroidContentType.sonification,\1usageType: AndroidUsageType.assistanceAccessibility,',
    text, flags=re.DOTALL
)

with open('lib/core/timer_state.dart', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated AudioContext to assistanceAccessibility.")
