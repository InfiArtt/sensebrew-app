import re

with open('lib/core/ai_service.dart', 'r', encoding='utf-8') as f:
    content = f.read()

content = re.sub(r'\"description\": \"ID:.*?\"', '\"description\": {\"id\": \"Penjelasan singkat.\", \"en\": \"Short explanation.\"}', content)
content = re.sub(r'\"extraIngredients\": \"ID:.*?\"', '\"extraIngredients\": {\"id\": \"15 ml susu kental manis\", \"en\": \"15 ml condensed milk\"}', content)
content = re.sub(r'\"instructionText\": \"ID:.*?\"', '\"instructionText\": {\"id\": \"Tuang 50 ml air\", \"en\": \"Pour 50 ml of water\"}', content)

with open('lib/core/ai_service.dart', 'w', encoding='utf-8') as f:
    f.write(content)
