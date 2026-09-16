import re

with open('lib/core/ai_service.dart', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace("class AIService {", "class AiService {")

with open('lib/core/ai_service.dart', 'w', encoding='utf-8') as f:
    f.write(text)
print("Fixed AiService class name")
