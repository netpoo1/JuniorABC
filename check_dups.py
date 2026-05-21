import json
from pathlib import Path

ROOT = Path(__file__).parent
for f in sorted((ROOT / "flashcard" / "data").glob("*.json")):
    data = json.loads(f.read_text(encoding="utf-8"))
    seen = {}
    dups = []
    for i, w in enumerate(data["words"]):
        key = w["word"].lower()
        if key in seen:
            dups.append((i, w["word"], seen[key]))
        else:
            seen[key] = i
    print(f"{f.name}: {len(data['words'])} words, {len(dups)} duplicates")
    for idx, word, first_idx in dups:
        print(f"  [{idx}] \"{word}\" (first at [{first_idx}])")
