import re

with open('lib/core/app_strings.dart', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("'gemini_title': 'Google Gemini API Key',", "'gemini_title': 'AI Provider',")
content = content.replace("'gemini_desc': 'Enter your Gemini API key to use AI features.',", "'gemini_desc': 'To use the \"Create Recipe with AI\" feature, copy your API Key from Google AI Studio or Groq Console, and paste it below:',")

with open('lib/core/app_strings.dart', 'w', encoding='utf-8') as f:
    f.write(content)
