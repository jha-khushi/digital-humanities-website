"""
Step 1 of the RAG pipeline: pre-processing the corpus.

Removes the Project Gutenberg licence header and footer from each raw
text, collapses extra blank lines, and saves a clean copy as
corpus/<name>.txt. The raw downloads (corpus/raw_<name>.txt) are deleted
afterwards so that only the cleaned literary text is kept in the repository.

Run:  python preprocess.py
"""

import re
from pathlib import Path

CORPUS = Path(__file__).parent / "corpus"

START = re.compile(r"\*\*\* ?START OF (THE|THIS) PROJECT GUTENBERG EBOOK.*?\*\*\*")
END = re.compile(r"\*\*\* ?END OF (THE|THIS) PROJECT GUTENBERG EBOOK.*?\*\*\*")


def clean(text):
    text = text.replace("\r\n", "\n")
    start, end = START.search(text), END.search(text)
    if start and end:
        text = text[start.end():end.start()]
    text = text.replace("_", "")                 # Gutenberg italics markers
    text = re.sub(r"\[Illustration[^\]]*\]", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text)       # at most one blank line
    return text.strip() + "\n"


if __name__ == "__main__":
    for raw in sorted(CORPUS.glob("raw_*.txt")):
        cleaned = clean(raw.read_text(encoding="utf-8"))
        out = CORPUS / raw.name.removeprefix("raw_")
        out.write_text(cleaned, encoding="utf-8")
        raw.unlink()
        print(f"{out.name}: {len(cleaned.split()):,} words")
