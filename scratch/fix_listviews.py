import os

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
    
    # We must ensure we don't blindly replace `ListView.builder`.
    # First, let's just replace `ListView(`
    content = content.replace('ListView(', 'SingleChildScrollView(child: Column(')
    
    with open(screen, 'w', encoding='utf-8') as f:
        f.write(content)

print("Replaced ListView with SingleChildScrollView + Column in top-level scrolling!")
