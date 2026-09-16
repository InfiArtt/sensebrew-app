import re

# Fix recipe.dart
with open('lib/core/recipe.dart', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('\n    name: "Phin Coconut', '\n  Recipe(\n    name: "Phin Coconut')
text = text.replace('\n    name: "Orea V3', '\n  Recipe(\n    name: "Orea V3')
text = text.replace('\n    name: "V60 Dark', '\n  Recipe(\n    name: "V60 Dark')
text = text.replace('\n    name: "Kasuya Devil', '\n  Recipe(\n    name: "Kasuya Devil')
text = text.replace('\n    name: "W.A.C Carolina', '\n  Recipe(\n    name: "W.A.C Carolina')
text = text.replace('\n    name: "W.A.C Paulina', '\n  Recipe(\n    name: "W.A.C Paulina')
text = text.replace('\n    name: "Tuomas Merikanto', '\n  Recipe(\n    name: "Tuomas Merikanto')
text = text.replace('\n    name: "Aeropress Flow', '\n  Recipe(\n    name: "Aeropress Flow')
text = text.replace('\n    name: "Aeropress Espresso Fake', '\n  Recipe(\n    name: "Aeropress Espresso Fake')
text = text.replace('\n    name: "Aeropress Tea', '\n  Recipe(\n    name: "Aeropress Tea')
text = text.replace('\n    name: "Aeropress Robusta', '\n  Recipe(\n    name: "Aeropress Robusta')
text = text.replace('\n    name: "Ca Phe Muoi', '\n  Recipe(\n    name: "Ca Phe Muoi')
text = text.replace('\n    name: "Ca Phe Trung', '\n  Recipe(\n    name: "Ca Phe Trung')
text = text.replace('\n    name: "Ca Phe Sua', '\n  Recipe(\n    name: "Ca Phe Sua')
text = text.replace('\n    name: "Phin Arabica', '\n  Recipe(\n    name: "Phin Arabica')
text = text.replace('\n    name: "Vietnam Drip Mocha', '\n  Recipe(\n    name: "Vietnam Drip Mocha')

with open('lib/core/recipe.dart', 'w', encoding='utf-8') as f:
    f.write(text)

# Fix brewing_screen.dart
with open('lib/screens/brewing_screen.dart', 'r', encoding='utf-8') as f:
    bt = f.read()
    
# Since my regex messed up brewing_screen.dart, I will restore it from git if possible, or just fix it.
# Let's check what the errors are in brewing_screen.dart.
