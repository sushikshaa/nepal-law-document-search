"""Measure top-k retrieval accuracy. Edit eval_questions.json with your own questions.
Each item: {"question": "...", "source": "file.pdf", "keyword": "text that must appear in the right chunk"}
Usage: python eval.py
"""
import json
from pathlib import Path
from core import build_index

CONFIGS = [(300, 50), (500, 80), (800, 120)]  # (chunk_size, overlap) to compare
questions = json.loads((Path(__file__).parent / "eval_questions.json").read_text(encoding="utf-8"))

for size, overlap in CONFIGS:
    store, n = build_index(chunk_size=size, chunk_overlap=overlap)
    hit1 = hit3 = 0
    for q in questions:
        results = store.similarity_search(q["question"], k=3)
        ok = [q["keyword"].lower() in r.page_content.lower() and r.metadata["source"] == q["source"]
              for r in results]
        hit1 += ok[0]
        hit3 += any(ok)
    print(f"chunk={size} overlap={overlap} chunks={n} | top-1: {hit1/len(questions):.0%} | top-3: {hit3/len(questions):.0%}")
