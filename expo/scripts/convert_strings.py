"""Convert Dart AppStrings and grinderDatabase into TypeScript.

Dart and TypeScript agree on single-quoted string escapes, so the translation
tables copy across verbatim; only the surrounding declarations change.

Run from the repo root:  python expo/scripts/convert_strings.py
"""

import os
import re

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LIB = os.path.join(REPO, "lib", "core")
OUT_DIR = os.path.join(REPO, "expo", "src", "core")

STRINGS_HEADER = """// AUTO-GENERATED translation tables from lib/core/app_strings.dart.
// Regenerate with `python expo/scripts/convert_strings.py`.
//
// Hand-written additions belong in appStrings.ts, which merges them over this
// table — anything added here is lost on the next regeneration.
export const GENERATED_STRINGS: Record<string, Record<string, string>> = {"""

STRINGS_FOOTER = ""

GRINDER_HEADER = """// AUTO-GENERATED from lib/core/grinder_database.dart.
// Regenerate with `python expo/scripts/convert_strings.py`.
import { str } from './appStrings';

export interface GrinderModel {
  id: string;
  name: string;
  isManual: boolean;
  getSetting: (microns: number) => string;
}

export const grinderDatabase: GrinderModel[] = ["""

GRINDER_FOOTER = """
/** Human-readable grind category for a micron target, e.g. "medium-fine". */
export function getGrindCategoryName(microns: number, lang: string): string {
  if (microns <= 400) return str(lang, 'custom_grind_400');
  if (microns <= 600) return str(lang, 'custom_grind_600');
  if (microns <= 800) return str(lang, 'custom_grind_800');
  if (microns <= 1000) return str(lang, 'custom_grind_1000');
  if (microns <= 1200) return str(lang, 'custom_grind_1200');
  return str(lang, 'custom_grind_1400');
}
"""


def convert_strings() -> None:
    dart = open(os.path.join(LIB, "app_strings.dart"), encoding="utf-8").read()
    marker = "static const Map<String, Map<String, String>> _strings = {"
    body = dart[dart.index(marker) + len(marker):]
    body = body[:body.index("\n  };")]

    out = os.path.join(OUT_DIR, "generatedStrings.ts")
    open(out, "w", encoding="utf-8").write(
        STRINGS_HEADER + body + "\n};\n" + STRINGS_FOOTER
    )
    print("wrote", out)
    for lang in ("id", "en"):
        section = body.split("'%s': {" % lang, 1)[1]
        section = section.split("\n    },", 1)[0]
        print("  %s keys:" % lang, len(re.findall(r"^\s*'[^']+':", section, re.M)))


def convert_grinders() -> None:
    dart = open(os.path.join(LIB, "grinder_database.dart"), encoding="utf-8").read()
    marker = "final List<GrinderModel> grinderDatabase = ["
    body = dart[dart.index(marker) + len(marker):]
    body = body[:body.index("\n];")]

    body = body.replace("GrinderModel(", "{")
    body = body.replace("getSetting: (microns) {", "getSetting: (microns: number) => {")
    body = re.sub(r"^(\s*)\),$", r"\1},", body, flags=re.M)

    out = os.path.join(OUT_DIR, "grinderDatabase.ts")
    open(out, "w", encoding="utf-8").write(
        GRINDER_HEADER + body + "\n];\n" + GRINDER_FOOTER
    )
    print("wrote", out)
    print("  grinders:", body.count("isManual:"))


if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)
    convert_strings()
    convert_grinders()
