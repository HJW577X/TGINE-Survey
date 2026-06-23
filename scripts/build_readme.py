#!/usr/bin/env python3
"""Build README.md from data/papers.csv.

Usage:
    python scripts/build_readme.py
"""
from pathlib import Path
import csv
from collections import Counter
ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT / "data" / "papers.csv"
README = ROOT / "README.md"

def load_papers():
    with PAPERS.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))

def md_link(label, url):
    return f"[{label}]({url})" if url else ""

def clean(v):
    return (v or "").replace("|", "/").replace("\n", " ").strip()

def task_table(rows, columns):
    out = []
    out.append("| " + " | ".join(label for label, _ in columns) + " |")
    out.append("| " + " | ".join("---" for _ in columns) + " |")
    for r in rows:
        vals = []
        for label, key in columns:
            value = clean(r.get(key, ""))
            if key == "paper":
                lab = "Paper" if ("scholar.google" not in value.lower()) else "Scholar"
                value = md_link(lab, value)
            elif key == "code":
                value = md_link("Code", value)
            elif key == "method":
                value = f"**{value}**"
            vals.append(value)
        out.append("| " + " | ".join(vals) + " |")
    return "\n".join(out)

if __name__ == "__main__":
    papers = load_papers()
    print("Loaded papers:", len(papers))
    for task, n in sorted(Counter(p["task"] for p in papers).items()):
        print(f"- {task}: {n}")
