import re

with open('lib/screens/settings_screen.dart', 'r', encoding='utf-8') as f:
    text = f.read()

bad_ai_section = """          Padding(
            padding: const EdgeInsets.all(16.0),
            child: Text(AppStrings.str(lang, 'gemini_title'), style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
          ),
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 16.0),
            child: Text(AppStrings.str(lang, 'gemini_desc')),
          ),
          const SizedBox(height: 16),
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 16.0),
            child: TextField(
              controller: _geminiController,
              decoration: const InputDecoration(
                labelText: 'Google Gemini API Key',
                border: OutlineInputBorder(),
              ),
              obscureText: true,
              onChanged: (val) {
                settings.setGeminiApiKey(val);
              },
            ),
          ),
          const SizedBox(height: 8),
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 16.0),
            child: TextField(
              controller: _groqController,
              decoration: const InputDecoration(
                labelText: 'Groq API Key',
                border: OutlineInputBorder(),
              ),
              obscureText: true,
              onChanged: (val) {
                settings.setGroqApiKey(val);
              },
            ),
          ),
          const SizedBox(height: 8),
          Align(
            alignment: Alignment.centerLeft,
            child: TextButton.icon(
              icon: const Icon(Icons.help_outline),
              label: Text(lang == 'en' ? 'How to get an API Key?' : 'Cara Mendapatkan API Key'),
              onPressed: () {
                showDialog(
                  context: context,
                  builder: (context) => AlertDialog(
                    title: Text(AppStrings.str(lang, 'gemini_help_title')),
                    content: SingleChildScrollView(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          const Text("Google Gemini (Gemini 2.5 Flash):", style: TextStyle(fontWeight: FontWeight.bold)),
                          Text(AppStrings.str(lang, 'gemini_help_content')),
                          const SizedBox(height: 16),
                          const Text("Groq (Llama 3):", style: TextStyle(fontWeight: FontWeight.bold)),
                          Text(AppStrings.str(lang, 'groq_help_content')),
                        ],
                      ),
                    ),
                    actions: [
                      TextButton(
                        onPressed: () => Navigator.pop(context),
                        child: Text(AppStrings.str(lang, 'close')),
                      ),
                    ],
                  ),
                );
              },
            ),
          ),"""

good_ai_section = """          ListTile(
            title: Text(AppStrings.str(lang, 'gemini_title'), style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            subtitle: Text(AppStrings.str(lang, 'gemini_desc')),
            trailing: ElevatedButton(
              onPressed: () {
                _showSelectionBottomSheet(
                  title: AppStrings.str(lang, 'gemini_title'),
                  options: [
                    {'value': 'gemini', 'label': 'Google Gemini'},
                    {'value': 'groq', 'label': 'Groq (Llama 3)'},
                  ],
                  currentValue: settings.aiProvider,
                  onSelected: (val) {
                    settings.setAiProvider(val);
                  },
                );
              },
              child: Text(settings.aiProvider == 'gemini' ? 'Gemini' : 'Groq'),
            ),
          ),
          const SizedBox(height: 8),
          if (settings.aiProvider == 'gemini')
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 16.0),
              child: TextField(
                controller: _geminiController,
                decoration: const InputDecoration(
                  labelText: 'Google Gemini API Key',
                  border: OutlineInputBorder(),
                ),
                obscureText: true,
                onChanged: (val) {
                  settings.setGeminiApiKey(val);
                },
              ),
            ),
          if (settings.aiProvider == 'groq')
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 16.0),
              child: TextField(
                controller: _groqController,
                decoration: const InputDecoration(
                  labelText: 'Groq API Key',
                  border: OutlineInputBorder(),
                ),
                obscureText: true,
                onChanged: (val) {
                  settings.setGroqApiKey(val);
                },
              ),
            ),
          const SizedBox(height: 8),
          Align(
            alignment: Alignment.centerLeft,
            child: TextButton.icon(
              icon: const Icon(Icons.help_outline),
              label: Text(lang == 'en' ? 'How to get an API Key?' : 'Cara Mendapatkan API Key'),
              onPressed: () {
                showDialog(
                  context: context,
                  builder: (context) => AlertDialog(
                    title: Text(AppStrings.str(lang, 'gemini_help_title')),
                    content: SingleChildScrollView(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          if (settings.aiProvider == 'gemini') ...[
                            const Text("Google Gemini (Gemini 2.5 Flash):", style: TextStyle(fontWeight: FontWeight.bold)),
                            Text(AppStrings.str(lang, 'gemini_help_content')),
                          ],
                          if (settings.aiProvider == 'groq') ...[
                            const Text("Groq (Llama 3):", style: TextStyle(fontWeight: FontWeight.bold)),
                            Text(AppStrings.str(lang, 'groq_help_content')),
                          ],
                        ],
                      ),
                    ),
                    actions: [
                      TextButton(
                        onPressed: () => Navigator.pop(context),
                        child: Text(AppStrings.str(lang, 'close')),
                      ),
                    ],
                  ),
                );
              },
            ),
          ),"""

text = text.replace(bad_ai_section, good_ai_section)

with open('lib/screens/settings_screen.dart', 'w', encoding='utf-8') as f:
    f.write(text)
print("Updated AI Provider section in settings_screen.dart")
