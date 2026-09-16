import re

with open('lib/screens/settings_screen.dart', 'r', encoding='utf-8') as f:
    text = f.read()

bad_block = """                    content: SingleChildScrollView(
                      child: Text(AppStrings.str(lang, 'gemini_help_content')),
                    ),"""

good_block = """                    content: SingleChildScrollView(
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

text = text.replace(bad_block, good_block)

with open('lib/screens/settings_screen.dart', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated API instructions to be swipeable line by line.")
