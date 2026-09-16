import re

with open("lib/core/app_strings.dart", "r", encoding="utf-8") as f:
    content = f.read()

# Replace gemini and groq help content in the EN block
en_gemini_id = r"'gemini_help_content': '1. Buka aistudio.google.com\\n2. Login dengan akun Google.\\n3. Klik \"Get API key\" > \"Create API key\".\\n4. Salin kodenya.\\n\\nCatatan: Layanan ini gratis tanpa perlu kartu kredit.',"
en_gemini_en = r"'gemini_help_content': '1. Go to aistudio.google.com\n2. Log in with your Google account.\n3. Click \"Get API key\" > \"Create API key\".\n4. Copy the code.\n\nNote: This service is free without requiring a credit card.',"

en_groq_id = r"'groq_help_content': '1. Buka console.groq.com/keys\\n2. Login dengan akunmu.\\n3. Klik \"Create API Key\".\\n4. Salin kodenya (biasanya diawali dengan gsk_).\\n\\nCatatan: Layanan ini gratis tanpa perlu kartu kredit.',"
en_groq_en = r"'groq_help_content': '1. Go to console.groq.com/keys\n2. Log in with your account.\n3. Click \"Create API Key\".\n4. Copy the code (usually starts with gsk_).\n\nNote: This service is free without requiring a credit card.',"

en_block_match = re.search(r"('en': \{)(.*?)(\n    \},)", content, re.DOTALL)
en_text = en_block_match.group(2)

new_en_text = en_text.replace(
    '\'gemini_help_content\': \'1. Buka aistudio.google.com\\n2. Login dengan akun Google.\\n3. Klik "Get API key" > "Create API key".\\n4. Salin kodenya.\\n\\nCatatan: Layanan ini gratis tanpa perlu kartu kredit.\',',
    '\'gemini_help_content\': \'1. Go to aistudio.google.com\\n2. Log in with your Google account.\\n3. Click "Get API key" > "Create API key".\\n4. Copy the code.\\n\\nNote: This service is free and does not require a credit card.\','
)

new_en_text = new_en_text.replace(
    '\'groq_help_content\': \'1. Buka console.groq.com/keys\\n2. Login dengan akunmu.\\n3. Klik "Create API Key".\\n4. Salin kodenya (biasanya diawali dengan gsk_).\\n\\nCatatan: Layanan ini gratis tanpa perlu kartu kredit.\',',
    '\'groq_help_content\': \'1. Go to console.groq.com/keys\\n2. Log in with your account.\\n3. Click "Create API Key".\\n4. Copy the code (usually starts with gsk_).\\n\\nNote: This service is free and does not require a credit card.\','
)

content = content.replace(en_text, new_en_text)

with open("lib/core/app_strings.dart", "w", encoding="utf-8") as f:
    f.write(content)
print("Updated app_strings.dart help contents!")
