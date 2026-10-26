from core import load_documents
from collections import defaultdict

pages = defaultdict(list)
for d in load_documents():
    pages[d.metadata["source"]].append(d.page_content)

for name, texts in pages.items():
    print("\n=====", name, "|", len(texts), "pages with text")
    print(texts[min(5, len(texts) - 1)][:300].replace("\n", " "))