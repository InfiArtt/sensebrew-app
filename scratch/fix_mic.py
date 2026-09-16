import re

with open('lib/core/app_strings.dart', 'r', encoding='utf-8') as f:
    content = f.read()

mic_id = "'ai_voice_note': '\" + chr(0x1F399) + chr(0xFE0F) + \" [Pesan Suara]'"
mic_en = "'ai_voice_note': '\" + chr(0x1F399) + chr(0xFE0F) + \" [Voice Message]'"

content = re.sub(r"'ai_voice_note':\s*\"[^\"]+\"", mic_id, content, count=1)
content = re.sub(r"'ai_voice_note':\s*\"[^\"]+\"", mic_en, content)

with open('lib/core/app_strings.dart', 'w', encoding='utf-8') as f:
    f.write(content)

print('Done')
