import re

with open('lib/core/ai_service.dart', 'r', encoding='utf-8') as f:
    content = f.read()

helper = '''
  static String parseI18n(dynamic field) {
    if (field == null) return '';
    if (field is String) return field;
    if (field is Map) {
      final idStr = field['id']?.toString() ?? '';
      final enStr = field['en']?.toString() ?? '';
      if (idStr.isEmpty && enStr.isEmpty) return '';
      return 'ID: ' + idStr + ' || EN: ' + enStr;
    }
    return field.toString();
  }

  static Future<AiResponse> generateRecipe({'''

content = content.replace('  static Future<AiResponse> generateRecipe({', helper)
content = content.replace('_parseI18n', 'parseI18n')
content = re.sub(r'instructionText: AppStrings\.str\(lang, \'pour\', \[amount\.toInt\(\)\.toString\(\)\]\),', 'instructionText: parseI18n(p[\'instructionText\']),', content)

with open('lib/core/ai_service.dart', 'w', encoding='utf-8') as f:
    f.write(content)
