import re
import json

with open('scratch/ui_keys.json', 'r', encoding='utf-8') as f:
    en_dict = json.load(f)

with open('lib/core/app_strings.dart', 'r', encoding='utf-8') as f:
    text = f.read()

insertion = ""
for k, v in en_dict.items():
    v = v.replace('\n', '\\n').replace("'", "\\'")
    insertion += f"      '{k}': '{v}',\n"

# The end of the file looks like:
#       'extra_key_15': '...',
#       }
#   };
# 
#   static String str(String lang, String key, [List<String>? args]) {

# So we can just split by '  static String str' and insert it before the closing of the en map.
parts = text.split('  static String str')
# parts[0] ends with something like "      }\n  };\n\n"
# We want to insert right before "      }\n  };\n\n"

# Let's find the last occurrence of "}" before parts[0] end
end_idx = parts[0].rfind('}') # This is the } before ;
end_idx2 = parts[0].rfind('}', 0, end_idx) # This is the } closing the 'en' block

new_part0 = parts[0][:end_idx2] + insertion + parts[0][end_idx2:]

new_text = new_part0 + '  static String str' + parts[1]

with open('lib/core/app_strings.dart', 'w', encoding='utf-8') as f:
    f.write(new_text)

print("Injected successfully")
