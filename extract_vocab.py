"""
extract_vocab.py

Scans english/ subfolders for PNG files that need vocabulary extraction,
calls Claude Vision API, and writes a structured .md file next to each image.

A file needs processing when:
  (a) no corresponding .md exists, OR
  (b) the .png was modified more recently than its .md

Usage:
  python extract_vocab.py                        # scan english/ relative to this script
  python extract_vocab.py path/to/folder         # scan a specific folder
  python extract_vocab.py --dry-run              # list files without processing

Requirements:
  pip install anthropic
  Set ANTHROPIC_API_KEY in environment (or .env file).
"""

import argparse
import base64
import os
import sys
from datetime import datetime
from pathlib import Path

BUCKET_MAP = {
    "7.0": "國一全", "7.1": "國一上", "7.2": "國一下",
    "8.0": "國二全", "8.1": "國二上", "8.2": "國二下",
    "9.0": "國三全", "9.1": "國三上", "9.2": "國三下",
}

EXTRACTION_PROMPT = """\
You are extracting English vocabulary from a Taiwan junior high school textbook page image.

Output ONLY the following markdown sections — no extra commentary.

## Book/Unit
One line: book title and unit number if visible (e.g. "第一冊（上）第 1 課"). Write "unclear" if not readable.

## Vocabulary

For EVERY English word or phrase on the page, produce one or more section blocks:

### Section: [section name from the page, e.g. "動詞", "形容詞", "顏色"]
| # | word | pos | meaning_zh | difficulty |
|---|---|---|---|---|
| 1 | ... | ... | ... | ... |

Rules for the `difficulty` column:
- `filtered_too_easy` — extremely basic sight words: pronouns (I/you/he/she/we/they), basic prepositions (in/on/at/to/of), conjunctions (and/but/or), colors (red/black/white/green/yellow/blue), basic nouns (boy/girl/man/woman/mother/father/school/door/bed/chair/table/wall), basic verbs (be/have/eat/drink/see/look/go/come/say/do/get/make/know/like/want), basic adjectives (big/small/good/bad/new/old/happy).
- `filtered_too_hard` — words beyond 大考中心 7000字 Level 1–4.
- `needs_verification` — word is visible but unclear; mark with [?] after the word.
- `keep` — everything else.

## Phrases
| phrase | meaning_zh |
|---|---|
| ... | ... |

List only phrases explicitly shown in the page's example notes (parenthetical or boxed).
Write "none" if there are no phrases.
"""


def needs_processing(png: Path) -> tuple[bool, str]:
    md = png.with_suffix(".md")
    if not md.exists():
        return True, "no MD found"
    if png.stat().st_mtime > md.stat().st_mtime:
        png_t = datetime.fromtimestamp(png.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")
        md_t = datetime.fromtimestamp(md.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")
        return True, f"PNG updated {png_t} > MD {md_t}"
    return False, "up to date"


def infer_bucket(name: str) -> str:
    parts = name.split(".")
    if len(parts) >= 2:
        prefix = f"{parts[0]}.{parts[1]}"
        label = BUCKET_MAP.get(prefix, "未知")
        return f"`{prefix}` ({label})"
    return "未知"


def encode_image(png: Path) -> tuple[str, str]:
    ext = png.suffix.lower()
    media = "image/jpeg" if ext in (".jpg", ".jpeg") else "image/png"
    data = base64.standard_b64encode(png.read_bytes()).decode("utf-8")
    return media, data


def call_claude(png: Path, client) -> str:
    media, data = encode_image(png)
    response = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=4096,
        messages=[{
            "role": "user",
            "content": [
                {"type": "image", "source": {"type": "base64", "media_type": media, "data": data}},
                {"type": "text", "text": EXTRACTION_PROMPT},
            ],
        }],
    )
    return response.content[0].text


def write_md(png: Path, extraction: str) -> None:
    bucket = infer_bucket(png.name)
    today = datetime.now().strftime("%Y-%m-%d")
    content = f"""# Vocab Extraction — {png.name}

- **Source file:** `{png.name}`
- **Bucket:** {bucket}
- **Extracted by:** Claude Vision (extract_vocab.py)
- **Date:** {today}

---

{extraction.strip()}
"""
    png.with_suffix(".md").write_text(content, encoding="utf-8")


def scan(root: Path) -> list[tuple[Path, str]]:
    results = []
    for png in sorted(root.rglob("*.png")):
        ok, reason = needs_processing(png)
        if ok:
            results.append((png, reason))
    return results


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract vocabulary from PNG images.")
    parser.add_argument("folder", nargs="?", default=None, help="Root folder to scan (default: english/ next to this script)")
    parser.add_argument("--dry-run", action="store_true", help="List files without calling API")
    args = parser.parse_args()

    root = Path(args.folder) if args.folder else Path(__file__).parent / "english"
    if not root.exists():
        print(f"Folder not found: {root}", file=sys.stderr)
        sys.exit(1)

    pending = scan(root)

    if not pending:
        print("All PNG files are up to date.")
        return

    print(f"{len(pending)} file(s) to process:")
    for png, reason in pending:
        print(f"  [{reason}]  {png.relative_to(root.parent)}")

    if args.dry_run:
        print("\n--dry-run: no files written.")
        return

    try:
        import anthropic
    except ImportError:
        print("\nMissing dependency: pip install anthropic", file=sys.stderr)
        sys.exit(1)

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("\nMissing ANTHROPIC_API_KEY environment variable.", file=sys.stderr)
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)

    for i, (png, reason) in enumerate(pending, 1):
        print(f"\n[{i}/{len(pending)}] {png.name}  ({reason})")
        extraction = call_claude(png, client)
        write_md(png, extraction)
        print(f"  -> written: {png.with_suffix('.md').name}")

    print(f"\nDone. {len(pending)} file(s) processed.")


if __name__ == "__main__":
    main()
