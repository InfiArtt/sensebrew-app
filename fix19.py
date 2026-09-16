import re

with open('lib/core/app_strings.dart', 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

# The weird character is probably \ufffd since errors='replace' will ensure it.
# Wait, if I use errors='replace', it will become \ufffd.
# But it's already written to the file. Let's just read it as is.
