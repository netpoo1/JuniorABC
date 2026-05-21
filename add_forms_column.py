"""
One-off migration: add `forms` column to all vocab MD files.
Format:
  - Verbs: V1-V2-V3 (e.g., say-said-said)
  - Nouns (plural): pl. <plural> (e.g., pl. wives, pl. babies)
  - Default: — (em dash)
"""
import re
from pathlib import Path

ROOT = Path(__file__).parent
ENGLISH_DIR = ROOT / "english"

IRREGULAR_FORMS = {
    # Irregular verbs (V1-V2-V3)
    "wake":  "wake-woke-woken",
    "say":   "say-said-said",
    "fight": "fight-fought-fought",
    "see":   "see-saw-seen",
    "read":  "read-read-read",
    "go":    "go-went-gone",
    "have":  "have-had-had",
    "run":   "run-ran-run",
    "blow":  "blow-blew-blown",
    "meet":  "meet-met-met",
    "sleep": "sleep-slept-slept",
    "sing":  "sing-sang-sung",
    "swim":  "swim-swam-swum",
    "hurt":  "hurt-hurt-hurt",
    "put":   "put-put-put",
    "throw": "throw-threw-thrown",
    "win":   "win-won-won",
    "begin": "begin-began-begun",
    "bring": "bring-brought-brought",

    # Noun plurals (truly irregular)
    "man":       "pl. men",
    "woman":     "pl. women",
    "person":    "pl. people",
    "wife":      "pl. wives",
    "housewife": "pl. housewives",
    "mouse":     "pl. mice",
    "tooth":     "pl. teeth",
    "life":      "pl. lives",

    # Noun plurals (y -> ies)
    "baby":    "pl. babies",
    "family":  "pl. families",
    "party":   "pl. parties",
    "library": "pl. libraries",
}


def transform(text):
    lines = text.split("\n")
    out = []
    last_was_header = False

    for line in lines:
        stripped = line.strip()

        # Detect header row: starts with "| # | word |"
        if stripped.startswith("| # |") and "difficulty" in stripped:
            new_line = stripped.replace("| meaning_zh | difficulty |",
                                       "| meaning_zh | forms | difficulty |")
            out.append(new_line)
            last_was_header = True
            continue

        # Detect separator (right after header)
        if last_was_header and re.match(r"^\|[\-\s\|]+\|$", stripped):
            # Count existing segments, add one more
            out.append(stripped.rstrip("|") + "---|")
            last_was_header = False
            continue

        last_was_header = False

        # Detect data row: starts with "| <num/id> |"
        if stripped.startswith("|") and not stripped.startswith("|---"):
            cells = [c.strip() for c in stripped.strip("|").split("|")]
            # Standard data row has 6 cells: #, word, syllables, pos, meaning_zh, difficulty
            if len(cells) == 6 and re.match(r"^\d+[a-z]?$", cells[0]):
                num, word, syl, pos, zh, diff = cells
                forms = IRREGULAR_FORMS.get(word.lower(), "—")
                out.append(f"| {num} | {word} | {syl} | {pos} | {zh} | {forms} | {diff} |")
                continue

        out.append(line)

    return "\n".join(out)


updated = []
for md_path in sorted(ENGLISH_DIR.glob("**/*.md")):
    text = md_path.read_text(encoding="utf-8")
    new_text = transform(text)
    if new_text != text:
        md_path.write_text(new_text, encoding="utf-8")
        updated.append(md_path.name)
        # Count how many forms were filled
        filled = sum(1 for w in IRREGULAR_FORMS
                     if f"| {w}" in new_text.lower() or f"| {w.capitalize()}" in new_text)
        print(f"  WROTE {md_path.name}")
    else:
        print(f"  SKIP  {md_path.name}  (no change)")

print(f"\nTotal updated: {len(updated)} files")
