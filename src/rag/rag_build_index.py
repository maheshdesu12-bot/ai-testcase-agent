import os
import json
import numpy as np
import faiss
from pypdf import PdfReader
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

PDF_PATH = "rag/requirements.pdf"
OUT_DIR = "rag/index"
os.makedirs(OUT_DIR, exist_ok=True)

INDEX_PATH = os.path.join(OUT_DIR, "faiss.index")
META_PATH = os.path.join(OUT_DIR, "chunks.json")

EMBED_MODEL = "text-embedding-3-small"  # good default for RAG :contentReference[oaicite:0]{index=0}


def read_pdf_text(path: str) -> str:
    reader = PdfReader(path)
    pages = []
    for p in reader.pages:
        pages.append(p.extract_text() or "")
    return "\n".join(pages)


def chunk_text(text: str, chunk_size: int = 900, overlap: int = 150) -> list[str]:
    # Simple chunking by characters (good enough to start)
    chunks = []
    i = 0
    while i < len(text):
        chunks.append(text[i:i + chunk_size].strip())
        i += max(1, chunk_size - overlap)
    return [c for c in chunks if len(c) > 50]


def embed_texts(texts: list[str]) -> np.ndarray:
    # Batch embeddings
    resp = client.embeddings.create(
        model=EMBED_MODEL,
        input=texts
    )
    vectors = np.array([d.embedding for d in resp.data], dtype=np.float32)
    return vectors


def main():
    if not os.path.exists(PDF_PATH):
        raise FileNotFoundError(f"PDF not found at {PDF_PATH}")

    text = read_pdf_text(PDF_PATH)
    chunks = chunk_text(text)

    print(f"Pages text loaded. Chunks created: {len(chunks)}")
    vectors = embed_texts(chunks)

    dim = vectors.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(vectors)

    faiss.write_index(index, INDEX_PATH)
    with open(META_PATH, "w", encoding="utf-8") as f:
        json.dump({"chunks": chunks}, f, indent=2, ensure_ascii=False)

    print(f"✅ Index saved: {INDEX_PATH}")
    print(f"✅ Chunks saved: {META_PATH}")


if __name__ == "__main__":
    main()