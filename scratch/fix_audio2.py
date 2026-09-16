import re

with open('lib/core/timer_state.dart', 'r', encoding='utf-8') as f:
    text = f.read()

# Revert usageType and contentType back to media/music, but set audioFocus to none
text = re.sub(
    r'contentType: AndroidContentType\.sonification,(\s*)usageType: AndroidUsageType\.assistanceAccessibility,(\s*)audioFocus: AndroidAudioFocus\.gainTransientMayDuck,',
    r'contentType: AndroidContentType.music,\1usageType: AndroidUsageType.media,\2audioFocus: AndroidAudioFocus.none,',
    text, flags=re.DOTALL
)

with open('lib/core/timer_state.dart', 'w', encoding='utf-8') as f:
    f.write(text)

print("Reverted to media, set audioFocus to none.")
