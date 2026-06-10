#!/usr/bin/env python3
"""
build_vocab.py — Parse vocabulary MD files and generate per-bucket JSON.

Usage:
  python build_vocab.py           # generate JSON for all new buckets
  python build_vocab.py --force   # overwrite existing JSON files
"""
import re, json, sys
from pathlib import Path
from collections import defaultdict

ROOT        = Path(__file__).parent
ENGLISH_DIR = ROOT / "english"
DATA_DIR    = ROOT / "flashcard" / "data"

BUCKET_LABELS = {
    "7.0":"國一 (全冊)","7.1":"國一 (上冊)","7.2":"國一 (下冊)",
    "8.0":"國二 (全冊)","8.1":"國二 (上冊)","8.2":"國二 (下冊)",
    "9.0":"國三 (全冊)","9.1":"國三 (上冊)","9.2":"國三 (下冊)",
}
DIFF_MAP = {"keep":"keep","filtered_too_easy":"easy"}

def extract_vocab_rows(text):
    rows, header = [], None
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if all(re.match(r"^[-:]+$", c) for c in cells if c):
            continue
        if any(c.lower() == "word" for c in cells):
            header = [c.lower().replace(" ","_") for c in cells]
            continue
        if header and len(cells) >= len(header):
            rows.append(dict(zip(header, cells)))
    return rows

def get_year_and_bucket(filename):
    """Parse '114.7.1.006.md' → ('114', '7.1')."""
    m = re.match(r"^(\d+)\.(\d+\.\d+)\.", filename)
    return (m.group(1), m.group(2)) if m else (None, None)

def main():
    force = "--force" in sys.argv
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    bucket_words  = defaultdict(list)
    bucket_seen   = defaultdict(set)

    for md_path in sorted(ENGLISH_DIR.glob("**/*.md")):
        # Skip VIP-only subdirectories (purely numeric folder names like "1010609").
        if any(part.isdigit() for part in md_path.relative_to(ENGLISH_DIR).parts[:-1]):
            continue
        year, bucket = get_year_and_bucket(md_path.name)
        if not bucket:
            continue
        key = (year, bucket)
        text = md_path.read_text(encoding="utf-8")
        for row in extract_vocab_rows(text):
            word = row.get("word","").strip()
            if not word or word in ("—","?","word"):
                continue
            diff = DIFF_MAP.get(row.get("difficulty","").strip())
            if diff is None:
                continue
            syl_raw = row.get("syllables","").strip()
            syl = "" if syl_raw in ("—","","?") else syl_raw
            forms_raw = row.get("forms","").strip()
            forms = "" if forms_raw in ("—","","?") else forms_raw
            wkey = word.lower()
            if wkey not in bucket_seen[key]:
                bucket_seen[key].add(wkey)
                bucket_words[key].append({
                    "word":  word,
                    "pos":   row.get("pos","").strip(),
                    "zh":    row.get("meaning_zh","").strip(),
                    "syl":   syl,
                    "forms": forms,
                    "diff":  diff,
                })

    for (year, bucket), words in bucket_words.items():
        out = DATA_DIR / f"{year}.{bucket}.json"
        if out.exists() and not force:
            print(f"  SKIP  {out.name}  (exists — use --force to overwrite)")
            continue
        out.write_text(
            json.dumps({"year":year,"bucket":bucket,"label":BUCKET_LABELS.get(bucket,bucket),"words":words},
                       ensure_ascii=False, indent=2),
            encoding="utf-8"
        )
        print(f"  WROTE {out.name}  ({len(words)} words)")

if __name__ == "__main__":
    main()
