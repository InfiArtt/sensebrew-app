import os

screens = [
    'lib/screens/brewing_screen.dart',
    'lib/screens/calibration_screen.dart',
    'lib/screens/custom_recipe_screen.dart',
    'lib/screens/home_screen.dart',
    'lib/screens/settings_screen.dart'
]

def find_matching_paren(s, start_idx):
    count = 1
    idx = start_idx
    while idx < len(s):
        if s[idx] == '(':
            count += 1
        elif s[idx] == ')':
            count -= 1
            if count == 0:
                return idx
        idx += 1
    return -1

for screen in screens:
    with open(screen, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Revert first
    content = content.replace('SingleChildScrollView(\nchild: Column(\n', 'ListView(\n')
    content = content.replace('SingleChildScrollView(child: Column(', 'ListView(')
    
    # Now replace properly
    while 'ListView(' in content:
        start_idx = content.find('ListView(') + len('ListView(')
        end_idx = find_matching_paren(content, start_idx)
        
        if end_idx != -1:
            content = content[:start_idx-len('ListView(')] + 'SingleChildScrollView(child: Column(' + content[start_idx:end_idx] + '))' + content[end_idx+1:]
        else:
            break

    with open(screen, 'w', encoding='utf-8') as f:
        f.write(content)

print("Properly replaced ListView with SingleChildScrollView!")
