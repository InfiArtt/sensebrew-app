import re

# 1. Update app_strings.dart
with open('lib/core/app_strings.dart', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace the single gemini_help_content with two separated ones for both ID and EN
bad_id = r"'gemini_help_content': 'Google Gemini:\\n1. Buka aistudio.google.com\\n2. Login dengan akun Google.\\n3. Klik \"Get API key\" > \"Create API key\".\\n4. Salin kodenya.\\n\\nGroq Llama 3 \(Lebih Cepat\):\\n1. Buka console.groq.com/keys\\n2. Login, klik \"Create API Key\".\\n3. Salin kodenya \(berawalan gsk_\).\\n\\nCatatan: Keduanya gratis tanpa kartu kredit.',"
good_id = """'gemini_help_content': '1. Buka aistudio.google.com\\n2. Login dengan akun Google.\\n3. Klik "Get API key" > "Create API key".\\n4. Salin kodenya.\\n\\nCatatan: Layanan ini gratis tanpa perlu kartu kredit.',
      'groq_help_content': '1. Buka console.groq.com/keys\\n2. Login dengan akunmu.\\n3. Klik "Create API Key".\\n4. Salin kodenya (biasanya diawali dengan gsk_).\\n\\nCatatan: Layanan ini gratis tanpa perlu kartu kredit.',"""

bad_en = r"'gemini_help_content': 'Google Gemini:\\n1. Open aistudio.google.com\\n2. Sign in with Google.\\n3. Click \"Get API key\" > \"Create API key\".\\n4. Copy the code.\\n\\nGroq Llama 3 \(Faster\):\\n1. Open console.groq.com/keys\\n2. Sign in, click \"Create API Key\".\\n3. Copy the code \(starts with gsk_\).\\n\\nNote: Both provide free tiers with no credit card required.',"
good_en = """'gemini_help_content': '1. Open aistudio.google.com\\n2. Sign in with Google.\\n3. Click "Get API key" > "Create API key".\\n4. Copy the code.\\n\\nNote: This is a free tier with no credit card required.',
      'groq_help_content': '1. Open console.groq.com/keys\\n2. Sign in to your account.\\n3. Click "Create API Key".\\n4. Copy the code (starts with gsk_).\\n\\nNote: This is a free tier with no credit card required.',"""

text = re.sub(bad_id, good_id, text)
text = re.sub(bad_en, good_en, text)

with open('lib/core/app_strings.dart', 'w', encoding='utf-8') as f:
    f.write(text)

# 2. Update settings_screen.dart
with open('lib/screens/settings_screen.dart', 'r', encoding='utf-8') as f:
    stext = f.read()

bad_setting = """                    content: SingleChildScrollView(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        mainAxisSize: MainAxisSize.min,
                        children: AppStrings.str(lang, 'gemini_help_content').split('\\n').map((line) {
                          if (line.trim().isEmpty) {
                            return const SizedBox(height: 12);
                          }
                          return Padding(
                            padding: const EdgeInsets.only(bottom: 6.0),
                            child: Text(line, style: const TextStyle(fontSize: 16)),
                          );
                        }).toList(),
                      ),
                    ),"""

good_setting = """                    content: SingleChildScrollView(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        mainAxisSize: MainAxisSize.min,
                        children: AppStrings.str(lang, settings.aiProvider == 'groq' ? 'groq_help_content' : 'gemini_help_content').split('\\n').map((line) {
                          if (line.trim().isEmpty) {
                            return const SizedBox(height: 12);
                          }
                          return Padding(
                            padding: const EdgeInsets.only(bottom: 6.0),
                            child: Text(line, style: const TextStyle(fontSize: 16)),
                          );
                        }).toList(),
                      ),
                    ),"""

stext = stext.replace(bad_setting, good_setting)

with open('lib/screens/settings_screen.dart', 'w', encoding='utf-8') as f:
    f.write(stext)

print("Updated help instructions based on selected provider.")
