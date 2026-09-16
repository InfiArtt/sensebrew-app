import os
import re

screens = [
    'lib/screens/brewing_screen.dart',
    'lib/screens/calibration_screen.dart',
    'lib/screens/custom_recipe_screen.dart',
    'lib/screens/home_screen.dart',
    'lib/screens/settings_screen.dart'
]

for screen in screens:
    with open(screen, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Use regex to properly move padding to SingleChildScrollView
    # Match: SingleChildScrollView(child: Column( \n [spaces] padding: ... ,
    # Replace with: SingleChildScrollView(padding: ..., child: Column( \n [spaces]
    
    content = re.sub(
        r'SingleChildScrollView\(\s*child:\s*Column\(\s*padding:\s*(.*?),\s*',
        r'SingleChildScrollView(padding: \1, child: Column(',
        content
    )
    
    content = re.sub(
        r'SingleChildScrollView\(\n\s*child:\s*Column\(\n\s*padding:\s*(.*?),\s*',
        r'SingleChildScrollView(\npadding: \1,\nchild: Column(\n',
        content
    )

    with open(screen, 'w', encoding='utf-8') as f:
        f.write(content)

print("Fixed padding syntax!")
