import re

with open('lib/core/recipe.dart', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Tradisional Vietnam Drip
text = re.sub(
    r'(name: "Tradisional Vietnam Drip".*?coffeeGrams: 15,)',
    r'\1\n      beanType: "Robusta",',
    text, flags=re.DOTALL
)

# 2. Ca Phe Sua Da
text = re.sub(
    r'(name: "Ca Phe Sua Da \(Kopi Susu Es\)".*?coffeeGrams: 20,)',
    r'\1\n      beanType: "Robusta",',
    text, flags=re.DOTALL
)

# 3. Vietnam Drip Gula Aren
text = re.sub(
    r'(name: "Vietnam Drip Gula Aren".*?extraIngredients: )".*?",',
    r'\1"30 ml gula aren cair, 30 ml susu evaporasi/susu segar, 100 gram es batu",',
    text, flags=re.DOTALL
)
text = re.sub(
    r'(name: "Vietnam Drip Gula Aren".*?coffeeGrams: 18,)',
    r'\1\n      beanType: "Robusta",',
    text, flags=re.DOTALL
)

# 4. Vietnam Drip Paper Filter Method
text = re.sub(
    r'(name: "Vietnam Drip Paper Filter Method".*?coffeeGrams: 15,)',
    r'\1\n      beanType: "Robusta",',
    text, flags=re.DOTALL
)

# 5. Double Tamp Vietnam Drip
text = re.sub(
    r'(name: "Double Tamp Vietnam Drip".*?coffeeGrams: 20,)',
    r'\1\n      beanType: "Robusta",',
    text, flags=re.DOTALL
)
# Fix double tamp phases
match_dt = re.search(r'(name: "Double Tamp Vietnam Drip".*?phases: \[)(.*?)(\],)', text, re.DOTALL)
if match_dt:
    new_phases = """
        RecipePhase(startTimeSeconds: 0, pourAmountMl: 20, action: PhaseAction.pourCenter),
        RecipePhase(startTimeSeconds: 30, action: PhaseAction.press),
        RecipePhase(startTimeSeconds: 35, action: PhaseAction.wait),
        RecipePhase(startTimeSeconds: 45, pourAmountMl: 80, action: PhaseAction.pourCenter),
"""
    text = text[:match_dt.start()] + match_dt.group(1) + new_phases + match_dt.group(3) + text[match_dt.end():]


# 6. Ca Phe Muoi (Salted Coffee)
text = re.sub(
    r'(name: "Ca Phe Muoi \(Salted Coffee\)".*?coffeeGrams: 20,)',
    r'\1\n      extraIngredients: "30 ml susu kental manis, 40 ml heavy cream (dikocok dengan sejumput garam hingga kental), es batu secukupnya",',
    text, flags=re.DOTALL
)

# 7. Ca Phe Trung (Egg Coffee)
text = re.sub(
    r'(name: "Ca Phe Trung \(Egg Coffee\)".*?coffeeGrams: 20,)',
    r'\1\n      extraIngredients: "2 kuning telur ayam kampung, 30 ml susu kental manis, 1/2 sdt ekstrak vanila (dikocok rata hingga mengembang berjejak)",',
    text, flags=re.DOTALL
)

# 8. Ca Phe Sua Chua (Yogurt Coffee)
text = re.sub(
    r'(name: "Ca Phe Sua Chua \(Yogurt Coffee\)".*?coffeeGrams: 15,)',
    r'\1\n      extraIngredients: "100 ml yogurt kental (plain/manis), 20 ml susu kental manis, 100 gram es batu",',
    text, flags=re.DOTALL
)

# 9. Vietnam Drip Mocha
text = re.sub(
    r'(name: "Vietnam Drip Mocha".*?coffeeGrams: 15,)',
    r'\1\n      extraIngredients: "30 ml susu kental manis, 1 sdm bubuk kakao/cokelat pekat",',
    text, flags=re.DOTALL
)


with open('lib/core/recipe.dart', 'w', encoding='utf-8') as f:
    f.write(text)

print("Fixed Vietnam Drip ingredients and bean types!")
