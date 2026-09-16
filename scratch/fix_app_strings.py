import re

with open('lib/core/app_strings.dart', 'r', encoding='utf-8') as f:
    text = f.read()

bad1 = """      'gemini_help_content': '1. Buka aistudio.google.com
2. Login dengan akun Google.
3. Klik "Get API key" > "Create API key".
4. Salin kodenya.

Catatan: Layanan ini gratis tanpa perlu kartu kredit.',"""

good1 = """      'gemini_help_content': '1. Buka aistudio.google.com\\n2. Login dengan akun Google.\\n3. Klik "Get API key" > "Create API key".\\n4. Salin kodenya.\\n\\nCatatan: Layanan ini gratis tanpa perlu kartu kredit.',"""

bad2 = """      'groq_help_content': '1. Buka console.groq.com/keys
2. Login dengan akunmu.
3. Klik "Create API Key".
4. Salin kodenya (biasanya diawali dengan gsk_).

Catatan: Layanan ini gratis tanpa perlu kartu kredit.',"""

good2 = """      'groq_help_content': '1. Buka console.groq.com/keys\\n2. Login dengan akunmu.\\n3. Klik "Create API Key".\\n4. Salin kodenya (biasanya diawali dengan gsk_).\\n\\nCatatan: Layanan ini gratis tanpa perlu kartu kredit.',"""

bad3 = """      'gemini_help_content': '1. Open aistudio.google.com
2. Sign in with Google.
3. Click "Get API key" > "Create API key".
4. Copy the code.

Note: This is a free tier with no credit card required.',"""

good3 = """      'gemini_help_content': '1. Open aistudio.google.com\\n2. Sign in with Google.\\n3. Click "Get API key" > "Create API key".\\n4. Copy the code.\\n\\nNote: This is a free tier with no credit card required.',"""

bad4 = """      'groq_help_content': '1. Open console.groq.com/keys
2. Sign in to your account.
3. Click "Create API Key".
4. Copy the code (starts with gsk_).

Note: This is a free tier with no credit card required.',"""

good4 = """      'groq_help_content': '1. Open console.groq.com/keys\\n2. Sign in to your account.\\n3. Click "Create API Key".\\n4. Copy the code (starts with gsk_).\\n\\nNote: This is a free tier with no credit card required.',"""

text = text.replace(bad1, good1).replace(bad2, good2).replace(bad3, good3).replace(bad4, good4)

with open('lib/core/app_strings.dart', 'w', encoding='utf-8') as f:
    f.write(text)

print("Fixed app_strings.dart multiline strings.")
