"""
============================================================
Topic: Comparing the Natural Worlds of Five Indian Literary Texts
       (extension of Assignment 02)
============================================================
Author Name(s): Khushi Jha
Short Description: Uses the validated flora and fauna names from the
RAG pipeline of Assignment 02 to compare the five books of the corpus
(Kalidasa; the Jataka Tales; Bankim Chandra Chattopadhyay, The Poison
Tree; Sarojini Naidu, The Golden Threshold; Rabindranath Tagore, The
Gardener). The RAG step found WHICH plants and animals the books name;
this script counts HOW OFTEN each one is mentioned in the full text of
every book (not only in the retrieved passages) and asks:
  1. Is each book's natural world mostly plants or mostly animals?
  2. Which kinds (trees, flowers, birds, mammals...) dominate?
  3. Which names are shared by several books, and which belong to
     only one?
  4. Which plants and animals appear together in the same passage
     (a co-occurrence network)?
Semester: Monsoon Semester 2026
Affiliation: Department of Humanities and Social Sciences,
Indian Institute of Technology (Indian School of Mines) Dhanbad

Requirements: matplotlib, networkx
Run:  python compare_books.py
Outputs: results/mentions.json, results/summary.md, figures/*.png
============================================================
"""

import json
import re
import sys
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import networkx as nx

HERE = Path(__file__).parent
# Assignment 02's repository (dh-02-rag-flora-fauna) must be cloned next to
# this one: its corpus, pipeline and validated names are used here.
RAG = next(p for p in (HERE.parent / "dh-02-rag-flora-fauna",
                       HERE.parent / "assignment_02_rag_flora_fauna") if p.exists())
sys.path.insert(0, str(RAG))
from rag_pipeline import BOOKS, load_chunks   # same books and passages as Assignment 02

RESULTS = HERE / "results"
FIGURES = HERE / "figures"

SHORT = {
    "Kalidasa": "Kalidasa",
    "Jataka Tales": "Jataka Tales",
    "Bankim Chandra Chattopadhyay, The Poison Tree": "The Poison Tree",
    "Sarojini Naidu, The Golden Threshold": "The Golden Threshold",
    "Rabindranath Tagore, The Gardener": "The Gardener",
}
CATEGORY_LABEL = {
    "tree": "Trees", "flower": "Flowers", "herb_or_grass": "Herbs and grasses",
    "crop_or_fruit": "Crops and fruit", "creeper": "Creepers",
    "mammal": "Mammals", "bird": "Birds", "reptile": "Reptiles",
    "fish_or_aquatic": "Fish and water creatures", "insect": "Insects",
    "amphibian": "Amphibians",
}

# ---- Counting mentions --------------------------------------------------
# Names that are also common English verbs or other words ("we bear her
# along", "the sun rose", "the palm of her hand"). For these, only animal or
# plant contexts are counted: after an article, number or describing word.
_DET = r"(?:a|an|the|this|that|his|her|their|its|my|your|wild|black|white|red|great|old|young|two|three|four|five|many|of|like|and)"
AMBIGUOUS = {
    "bear": rf"\b{_DET}\s+(?:she-|he-)?bears?\b|\bshe-bears?\b",
    "rose": rf"\broses\b|\b{_DET}\s+rose\b(?!\s+(?:up|from|to|and|in|on|at|with|before))",
    "palm": r"\bpalm[- ]trees?\b|\bpalms?\b(?=\s+(?:tree|grove|leaf|leaves|wine|juice))|\bpalmyras?\b|\bfan-palms?\b",
    "fly": rf"\b{_DET}\s+fl(?:y|ies)\b(?!\s+(?:away|off|to|up))",
    "seal": rf"\b{_DET}\s+seals?\b(?!\s+of)",
    "swallow": rf"\b{_DET}\s+swallows?\b",
    "duck": rf"\b{_DET}\s+ducks?\b",
    "bat": rf"\b{_DET}\s+bats?\b",
    "date": r"\bdate[- ](?:palm|tree|fruit)s?\b",
    "spring creeper": r"\bspring[- ]creepers?\b",
    # Kunda (Kunda Nandini) is the heroine of The Poison Tree: her name is a
    # jasmine, but only the flower is counted.
    "kunda": r"\bkunda[- ](?:flowers?|blossoms?|buds?|jasmines?)\b",
    # "sandals" are footwear; count sandal-wood and sandal paste, scent, trees
    "sandalwood": r"\bsandal-?wood\b|\bsandal\b(?=[- ](?:paste|tree|trees|scent|perfume|oil|powder|-wood))",
}


def patterns(record):
    """Regular expressions for a name and the variants it was merged from."""
    if record["name"] in AMBIGUOUS:
        return re.compile(AMBIGUOUS[record["name"]], re.IGNORECASE)
    names = {record["name"], *record.get("variants", [])}
    words = set()
    for n in names:
        for part in re.split(r"[()]", n):           # "ketak (screw-pine)"
            part = part.strip()
            if len(part) >= 3:
                words.add(part)
    alternatives = "|".join(sorted((re.escape(w) for w in words), key=len, reverse=True))
    return re.compile(rf"\b(?:{alternatives})(?:s|es)?\b", re.IGNORECASE)


def count_mentions(records, chunks):
    """Mentions per name per book, and the names found in each passage.

    Passages overlap by 50 words, so mentions are counted only in the
    first 200 words of each passage (the part not repeated in the next).
    """
    compiled = {r["name"]: patterns(r) for r in records}
    mentions = defaultdict(Counter)
    passage_names = []
    for chunk in chunks:
        words = chunk["text"].split()
        own = " ".join(words[:200])
        present = set()
        for name, pattern in compiled.items():
            n = len(pattern.findall(own))
            if n:
                mentions[chunk["book"]][name] += n
                present.add(name)
        passage_names.append(present)
    return mentions, passage_names


# ---- Charts --------------------------------------------------------------
# Categorical palette (fixed order) from the dataviz reference instance.
SERIES = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#6250d6", "#e34948"]
FLORA, FAUNA = "#1baf7a", "#eb6834"          # plants green-aqua, animals orange
OTHER_GREY = "#c9c8c3"
INK, INK_2 = "#0b0b0b", "#52514e"
plt.rcParams.update({"font.family": "Helvetica", "text.color": INK,
                     "axes.labelcolor": INK_2, "xtick.color": INK_2,
                     "ytick.color": INK_2, "figure.facecolor": "white"})


def kingdom_pies(books, mentions, kingdom_of):
    fig, axes = plt.subplots(1, 5, figsize=(15, 4))
    for ax, book in zip(axes, books):
        flora = sum(n for name, n in mentions[book].items() if kingdom_of[name] == "flora")
        fauna = sum(n for name, n in mentions[book].items() if kingdom_of[name] == "fauna")
        total = flora + fauna or 1
        ax.pie([flora, fauna], colors=[FLORA, FAUNA], startangle=90, counterclock=False,
               wedgeprops={"width": 0.38, "edgecolor": "white", "linewidth": 2})
        ax.text(0, 0.1, f"{100 * flora / total:.0f}%", ha="center", va="center",
                fontsize=20, fontweight="bold")
        ax.text(0, -0.2, "plants", ha="center", va="center", fontsize=9, color=INK_2)
        ax.set_title(f"{SHORT[book]}\n{flora + fauna:,} mentions", fontsize=11)
    fig.legend(handles=[plt.Rectangle((0, 0), 1, 1, color=c) for c in (FLORA, FAUNA)],
               labels=["Plants (flora)", "Animals (fauna)"], loc="lower center",
               ncol=2, frameon=False, fontsize=10)
    fig.suptitle("Plants or animals? Share of flora and fauna mentions in each book",
                 fontsize=13, fontweight="bold", x=0.02, ha="left")
    fig.tight_layout(rect=(0, 0.08, 1, 0.94))
    fig.savefig(FIGURES / "flora_fauna_share.png", dpi=200)
    plt.close(fig)


def category_pies(books, mentions, category_of):
    """One pie per book: its top five categories, the rest as 'Other'."""
    order = [c for c, _ in Counter(
        {c: sum(n for b in books for name, n in mentions[b].items() if category_of[name] == c)
         for c in set(category_of.values())}).most_common()]
    shown = order[:6]                                   # fixed colour per category
    colour = {c: SERIES[i] for i, c in enumerate(shown)}
    fig, axes = plt.subplots(1, 5, figsize=(15, 4.3))
    for ax, book in zip(axes, books):
        per_cat = Counter()
        for name, n in mentions[book].items():
            per_cat[category_of[name] if category_of[name] in shown else "other"] += n
        cats = [c for c in shown if per_cat[c]] + (["other"] if per_cat["other"] else [])
        values = [per_cat[c] for c in cats]
        ax.pie(values, colors=[colour.get(c, OTHER_GREY) for c in cats], startangle=90,
               counterclock=False, wedgeprops={"edgecolor": "white", "linewidth": 2},
               autopct=lambda p: f"{p:.0f}%" if p >= 9 else "", pctdistance=0.7,
               textprops={"fontsize": 9, "color": INK})
        ax.set_title(SHORT[book], fontsize=11)
    labels = [CATEGORY_LABEL[c] for c in shown] + ["Other"]
    fig.legend(handles=[plt.Rectangle((0, 0), 1, 1, color=c)
                        for c in [colour[c] for c in shown] + [OTHER_GREY]],
               labels=labels, loc="lower center", ncol=7, frameon=False, fontsize=10)
    fig.suptitle("What kind of nature? Mentions by category in each book",
                 fontsize=13, fontweight="bold", x=0.02, ha="left")
    fig.tight_layout(rect=(0, 0.08, 1, 0.94))
    fig.savefig(FIGURES / "category_by_book.png", dpi=200)
    plt.close(fig)


def sharing_bar(books, mentions):
    """How many names appear in 1, 2, 3, 4 or all 5 books."""
    in_books = Counter()
    for name in {n for b in books for n in mentions[b]}:
        in_books[sum(1 for b in books if mentions[b][name])] += 1
    xs = list(range(1, len(books) + 1))
    ys = [in_books[x] for x in xs]
    fig, ax = plt.subplots(figsize=(7, 3.6))
    bars = ax.bar([f"{x} book" + ("s" if x > 1 else "") for x in xs], ys,
                  color=SERIES[0], width=0.6)
    for bar, y in zip(bars, ys):
        ax.text(bar.get_x() + bar.get_width() / 2, y + 0.4, str(y), ha="center",
                fontsize=11, color=INK)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color("#c9c8c3")
    ax.set_yticks([])
    ax.set_title("In how many books does each plant or animal appear?", loc="left",
                 fontsize=13, fontweight="bold")
    fig.tight_layout()
    fig.savefig(FIGURES / "shared_names.png", dpi=200)
    plt.close(fig)
    return in_books


def network(passage_names, kingdom_of, totals, top_n=40):
    keep = {name for name, _ in totals.most_common(top_n)}
    edges = Counter()
    for names in passage_names:
        for a, b in combinations(sorted(names & keep), 2):
            edges[(a, b)] += 1
    g = nx.Graph()
    for (a, b), w in edges.items():
        if w >= 2:                                      # pairs seen together at least twice
            g.add_edge(a, b, weight=w)
    pos = nx.spring_layout(g, k=0.9, iterations=200, seed=7, weight="weight")
    fig, ax = plt.subplots(figsize=(11, 8))
    widths = [0.4 + 0.5 * g[a][b]["weight"] ** 0.5 for a, b in g.edges()]
    nx.draw_networkx_edges(g, pos, ax=ax, width=widths, edge_color="#c9c8c3", alpha=0.8)
    sizes = [60 + 9 * totals[n] ** 0.85 for n in g.nodes()]
    colours = [FLORA if kingdom_of[n] == "flora" else FAUNA for n in g.nodes()]
    nx.draw_networkx_nodes(g, pos, ax=ax, node_size=sizes, node_color=colours,
                           edgecolors="white", linewidths=1.5)
    for n, (x, y) in pos.items():
        ax.text(x, y + 0.04, n, ha="center", va="bottom", fontsize=12, color=INK)
    ax.legend(handles=[plt.Line2D([], [], marker="o", ls="", color=c, markersize=10)
                       for c in (FLORA, FAUNA)],
              labels=["Plant", "Animal"], frameon=False, loc="lower left", fontsize=13)
    ax.axis("off")
    fig.tight_layout()
    fig.savefig(FIGURES / "cooccurrence_network.png", dpi=200)
    plt.close(fig)
    degree = sorted(g.degree(weight="weight"), key=lambda x: -x[1])
    return g, degree


# ---- Main ----------------------------------------------------------------
def main():
    RESULTS.mkdir(exist_ok=True)
    FIGURES.mkdir(exist_ok=True)
    data = json.loads((RAG / "results" / "validated.json").read_text(encoding="utf-8"))
    records = data["records"]
    kingdom_of = {r["name"]: r["kingdom"] for r in records}
    category_of = {r["name"]: r["category"] for r in records}

    chunks = load_chunks()
    books = list(BOOKS.values())
    mentions, passage_names = count_mentions(records, chunks)
    totals = Counter()
    for b in books:
        totals.update(mentions[b])
    words = Counter()
    for c in chunks:
        words[c["book"]] += len(c["text"].split()[:200])

    kingdom_pies(books, mentions, kingdom_of)
    category_pies(books, mentions, category_of)
    in_books = sharing_bar(books, mentions)
    g, degree = network(passage_names, kingdom_of, totals)

    summary = {}
    for b in books:
        m = mentions[b]
        total = sum(m.values())
        # distinctive = names with the largest share of their mentions in this book
        distinctive = sorted((n for n in m if m[n] >= 3),
                             key=lambda n: (-m[n] / totals[n], -m[n]))[:8]
        summary[b] = {
            "words": words[b],
            "mentions": total,
            "mentions_per_1000_words": round(1000 * total / words[b], 1),
            "distinct_names": len(m),
            "flora_mentions": sum(n for x, n in m.items() if kingdom_of[x] == "flora"),
            "fauna_mentions": sum(n for x, n in m.items() if kingdom_of[x] == "fauna"),
            "top_names": m.most_common(10),
            "distinctive_names": [(n, m[n], totals[n]) for n in distinctive],
        }
    shared_all = sorted(n for n in totals if all(mentions[b][n] for b in books))
    (RESULTS / "mentions.json").write_text(json.dumps({
        "books": summary,
        "names_in_n_books": dict(sorted(in_books.items())),
        "names_in_all_books": shared_all,
        "most_connected_in_network": degree[:10],
        "mentions": {b: dict(mentions[b].most_common()) for b in books},
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = ["# Summary: the natural world of five books", "",
             "| Book | Words | Mentions | Per 1,000 words | Distinct names | Plants | Animals |",
             "|---|---|---|---|---|---|---|"]
    for b, s in summary.items():
        lines.append(f"| {SHORT[b]} | {s['words']:,} | {s['mentions']:,} | "
                     f"{s['mentions_per_1000_words']} | {s['distinct_names']} | "
                     f"{s['flora_mentions']} | {s['fauna_mentions']} |")
    lines += ["", "## Most mentioned and most distinctive names", ""]
    for b, s in summary.items():
        lines.append(f"**{SHORT[b]}.** Most mentioned: " +
                     ", ".join(f"{n} ({c})" for n, c in s["top_names"]) +
                     ". Distinctive (share of all mentions found in this book): " +
                     ", ".join(f"{n} ({c} of {t})" for n, c, t in s["distinctive_names"]) + ".")
        lines.append("")
    lines += [f"Names found in all five books: {', '.join(shared_all) or 'none'}.", "",
              "Most connected names in the co-occurrence network: " +
              ", ".join(f"{n} ({d})" for n, d in degree[:10]) + "."]
    (RESULTS / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
