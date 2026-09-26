"""Convert the Dart `recipeDatabase` literal into a TypeScript seed array.

The brewing values (pour amounts, phase timings, grind targets) are the part of
SenseBrew that must not drift between the Flutter build and the Expo build, so
they are translated mechanically instead of by hand.

Run from the repo root:  python expo/scripts/convert_recipes.py
"""

import os
import re

BACKSLASH = chr(92)
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC = os.path.join(REPO, "lib", "core", "recipe.dart")
OUT = os.path.join(REPO, "expo", "src", "core", "recipeDatabase.ts")

HEADER = """// AUTO-GENERATED from lib/core/recipe.dart (recipeDatabase).
// Do not hand-edit: regenerate with `python expo/scripts/convert_recipes.py`
// so the Flutter and Expo builds stay identical on brewing values.
import type { RecipeSeed } from './recipe';

export const recipeSeeds: RecipeSeed[] = ["""


def convert(body: str) -> str:
    """Rewrite Dart constructor calls as object literals, string-aware.

    Recipe(...) and RecipePhase(...) become { ... }; every other paren is left
    alone. Recipe names such as "Phin Coconut (Bac Xiu)" contain parentheses
    inside string literals, so a plain regex would unbalance the output.
    """
    out = []
    stack = []  # 'obj' for a constructor call, 'paren' for anything else
    i, n = 0, len(body)
    while i < n:
        c = body[i]

        if c in ("'", '"'):  # copy string literals verbatim
            quote = c
            out.append(c)
            i += 1
            while i < n:
                if body[i] == BACKSLASH:
                    out.append(body[i:i + 2])
                    i += 2
                    continue
                out.append(body[i])
                i += 1
                if body[i - 1] == quote:
                    break
            continue

        if c == "/" and i + 1 < n and body[i + 1] == "/":  # copy line comments
            j = body.find("\n", i)
            j = n if j == -1 else j
            out.append(body[i:j])
            i = j
            continue

        m = re.match(r"(Recipe|RecipePhase)\s*\(", body[i:])
        if m:
            out.append("{")
            stack.append("obj")
            i += m.end()
            continue

        if c == "(":
            out.append("(")
            stack.append("paren")
            i += 1
            continue

        if c == ")":
            kind = stack.pop() if stack else "paren"
            out.append("}" if kind == "obj" else ")")
            i += 1
            continue

        out.append(c)
        i += 1

    text = "".join(out)
    text = re.sub(r"\bBrewMethod\.(\w+)", r"'\1'", text)
    text = re.sub(r"\bPhaseAction\.(\w+)", r"'\1'", text)
    return text


def main() -> None:
    dart = open(SRC, encoding="utf-8").read()
    marker = "List<Recipe> recipeDatabase = ["
    body = dart[dart.index(marker) + len(marker):]
    body = body[:body.index("\n];")]

    converted = convert(body)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w", encoding="utf-8").write(HEADER + converted + "\n];\n")

    print("wrote", OUT)
    print("recipes:", len(re.findall(r"\bname:", converted)))
    print("phases: ", converted.count("startTimeSeconds:"))


if __name__ == "__main__":
    main()
