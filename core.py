"""Core retrieval pipeline: load docs -> chunk -> embed -> FAISS index."""
from pathlib import Path
from pypdf import PdfReader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

DOCS_DIR = Path(__file__).parent / "docs"
MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"


def load_documents(docs_dir=DOCS_DIR):
    docs = []
    for path in sorted(Path(docs_dir).glob("*")):
        if path.suffix.lower() == ".pdf":
            for i, page in enumerate(PdfReader(str(path)).pages, start=1):
                text = (page.extract_text() or "").strip()
                if text:
                    docs.append(Document(page_content=text,
                                         metadata={"source": path.name, "page": i}))
        elif path.suffix.lower() == ".txt":
            docs.append(Document(page_content=path.read_text(encoding="utf-8"),
                                 metadata={"source": path.name, "page": 1}))
    return docs


def build_index(chunk_size=500, chunk_overlap=80, model_name=MODEL):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", "।", ". ", " ", ""])  # "।" = Nepali full stop
    chunks = splitter.split_documents(load_documents())
    embeddings = HuggingFaceEmbeddings(
        model_name=model_name,
        encode_kwargs={"normalize_embeddings": True})
    return FAISS.from_documents(chunks, embeddings), len(chunks)