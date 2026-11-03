"""
Steps 4-5 of the synthetic reading: query and targeted extraction.

Sends prompt.txt to a local LLM (qwen2.5:7b via Ollama) once for each of
the three stages of "Subha" (the same equal parts used for the partial
reading). Every extracted expression is checked against the stage text;
expressions that do not occur in the text are discarded and logged.

Output: results/llm_extraction.json  (raw + verified extractions)

Run:  python extract_themes.py      (Ollama must be running)
"""

import json
import re
import urllib.request
from pathlib import Path

from partial_reading import three_parts

HERE = Path(__file__).parent
MODEL = "qwen2.5:7b"
DIMENSIONS = ["voice_and_silence", "nature_and_nonhuman_kinship",
              "social_and_patriarchal_structure", "affect_and_being"]
STAGES = ["Stage_I", "Stage_II", "Stage_III"]

SCHEMA = {"type": "object",
          "properties": {d: {"type": "array", "items": {"type": "string"}} for d in DIMENSIONS},
          "required": DIMENSIONS}


def ask(prompt):
    req = urllib.request.Request(
        "http://localhost:11434/api/chat",
        data=json.dumps({"model": MODEL, "stream": False, "format": SCHEMA,
                         "options": {"temperature": 0, "num_ctx": 8192},
                         "messages": [{"role": "user", "content": prompt}]}).encode(),
        headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=900) as resp:
        return json.loads(json.loads(resp.read())["message"]["content"])


def in_text(phrase, text):
    words = [re.escape(w) for w in phrase.lower().split()]
    return bool(words) and re.search(r"\b" + r"\W+".join(words), text.lower()) is not None


def main():
    template = (HERE / "prompt.txt").read_text(encoding="utf-8").split("-" * 70, 1)[1]
    results = {"model": MODEL, "stages": {}}
    for stage, sentences in zip(STAGES, three_parts()):
        text = " ".join(sentences)
        raw = ask(template.replace("{STAGE_TEXT}", text).strip())
        verified, rejected = {}, []
        for dim in DIMENSIONS:
            keep = []
            for item in raw.get(dim, []):
                item = item.strip().lower()
                if not item or item in keep:
                    continue
                (keep if in_text(item, text) else rejected).append(item)
            verified[dim] = keep
        results["stages"][stage] = {"sentences": len(sentences), "raw": raw,
                                    "verified": verified, "rejected_not_in_text": rejected}
        print(stage, {d: len(v) for d, v in verified.items()}, f"rejected {len(rejected)}")

    (HERE / "results").mkdir(exist_ok=True)
    (HERE / "results" / "llm_extraction.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
