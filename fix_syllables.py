#!/usr/bin/env python3
"""One-time fix: restore stress/silent-letter notation in all MD syllable columns."""
from pathlib import Path
import re

# word (lowercase) → correct syl notation
SYL = {
    # ── 7.1 ──────────────────────────────────────────────
    "teacher":        "TEACH·er",
    "student":        "STU·dent",
    "police officer": "po·LICE OF·fi·cer",
    "singer":         "SING·er",
    "housewife":      "HOUSE·wife",
    "office worker":  "OF·fice WORK·er",
    "doctor":         "DOC·tor",
    "family":         "FAM·i·ly",
    "parents":        "PAR·ents",
    "daughter":       "DAU[GH]·ter",
    "grandpa":        "GRAND·pa",
    "grandma":        "GRAND·ma",
    "brother":        "BROTH·er",
    "sister":         "SIS·ter",
    "uncle":          "UN·cle",
    "cousin":         "COUS·in",
    "husband":        "HUS·band",
    "woman":          "WOM·an",
    "person":         "PER·son",
    "people":         "PEO·ple",
    "father":         "FA·ther",
    "mother":         "MOTH·er",
    "color":          "COL·or",
    "purple":         "PUR·ple",
    "orange":         "OR·ange",
    "yellow":         "YEL·low",
    "pencil case":    "PEN·cil CASE",
    "pencil box / case": "PEN·cil CASE",
    "eraser":         "e·RAS·er",
    "ruler":          "RUL·er",
    "notebook":       "NOTE·book",
    "number":         "NUM·ber",
    "classmate":      "CLASS·mate",
    "sofa":           "SO·fa",
    "table":          "TA·ble",
    "umbrella":       "um·BREL·la",
    "welcome":        "WEL·come",
    "hurry":          "HUR·ry",
    "each other":     "EACH OTH·er",
    "talk":           "TA[L]K",
    "fight":          "FI[GH]T",
    "handsome":       "HAN[D]·some",
    "careful":        "CARE·ful",
    "happy":          "HAP·py",
    "also":           "AL·so",
    "again":          "a·GAIN",
    # ── 8.2 ──────────────────────────────────────────────
    "fever":          "FE·ver",
    "headache":       "HEAD·ache",
    "stomachache":    "STOM·ach·ache",
    "runny nose":     "RUN·ny NOSE",
    "medicine":       "MED·i·cine",
    "shoulder":       "SHOUL·der",
    "finger":         "FIN·ger",
    "lemon":          "LEM·on",
    "reason":         "REA·son",
    "meeting":        "MEET·ing",
    "mistake":        "mis·TAKE",
    "angle":          "AN·gle",
    "member":         "MEM·ber",
    "topic":          "TOP·ic",
    "useful":         "USE·ful",
    "common":         "COM·mon",
    "comfortable":    "COM·fort·a·ble",
    "helpful":        "HELP·ful",
    "afraid":         "a·FRAID",
    "simple":         "SIM·ple",
    "honest":         "HON·est",
    "excellent":      "EX·cel·lent",
    "able":           "A·ble",
    "probably":       "PROB·a·bly",
    "actually":       "AC·tu·al·ly",
    "although":       "al·THOUGH",
}

ROOT = Path(__file__).parent

def fix_md(path: Path) -> int:
    text  = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    changed = 0
    new_lines = []
    for line in lines:
        if line.startswith("|"):
            cells = [c.strip() for c in line.strip("|").split("|")]
            # table data row: cells[1]=word, cells[2]=syllables
            if len(cells) >= 3:
                word_key = cells[1].lower()
                old_syl  = cells[2]
                if word_key in SYL and old_syl != SYL[word_key]:
                    # Replace first occurrence of old_syl cell
                    old_token = f"| {old_syl} |"
                    new_token = f"| {SYL[word_key]} |"
                    if old_token in line:
                        line = line.replace(old_token, new_token, 1)
                        changed += 1
                    elif old_syl in ("—", "") and SYL[word_key]:
                        # Cell is "—" or empty; need to target the right column
                        # Replace the 3rd pipe-delimited cell
                        parts = line.split("|")
                        if len(parts) > 3:
                            parts[3] = f" {SYL[word_key]} "
                            line = "|".join(parts)
                            changed += 1
        new_lines.append(line)
    if changed:
        path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
        print(f"  FIXED  {path.name}  ({changed} cells updated)")
    return changed

total = 0
for md in sorted((ROOT / "english").glob("**/*.md")):
    total += fix_md(md)
print(f"\nTotal cells fixed: {total}")
