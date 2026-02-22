import os
import json
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI
import numpy as np
import faiss

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()


class FeatureRequest(BaseModel):
    feature: str


def generate_test_cases(feature_description: str) -> dict:
    system_msg = "You are a senior QA engineer. Output ONLY valid JSON."

    user_msg = f"""
Generate test cases for this feature:

{feature_description}

Return JSON with:
positive_test_cases, negative_test_cases, edge_cases
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.2,
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_msg}
        ],
        response_format={"type": "json_object"},
    )

    return json.loads(response.choices[0].message.content)

RAG_INDEX_PATH = "rag/index/faiss.index"
RAG_META_PATH = "rag/index/chunks.json"
EMBED_MODEL = "text-embedding-3-small"

def load_rag():
    if not os.path.exists(RAG_INDEX_PATH) or not os.path.exists(RAG_META_PATH):
        raise FileNotFoundError("RAG index not found. Run: python rag/rag_build_index.py")
    index = faiss.read_index(RAG_INDEX_PATH)
    with open(RAG_META_PATH, "r", encoding="utf-8") as f:
        meta = json.load(f)
    return index, meta["chunks"]

def embed_query(text: str) -> np.ndarray:
    resp = client.embeddings.create(model=EMBED_MODEL, input=[text])
    return np.array([resp.data[0].embedding], dtype=np.float32)

def retrieve_context(query: str, k: int = 4) -> str:
    index, chunks = load_rag()
    qv = embed_query(query)
    distances, ids = index.search(qv, k)
    picked = [chunks[i] for i in ids[0] if i >= 0]
    return "\n\n---\n\n".join(picked)
@app.post("/generate-testcases-rag")
def generate_rag(request: FeatureRequest):
    context = retrieve_context(request.feature, k=4)

    system_msg = "You are a senior QA engineer. Output ONLY valid JSON."
    user_msg = f"""
You MUST use the provided context from the requirements/spec document.

CONTEXT (from PDF):
{context}

TASK:
Generate test cases for:
{request.feature}

Return JSON with: positive_test_cases, negative_test_cases, edge_cases.
Output must be valid JSON only.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.2,
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_msg}
        ],
        response_format={"type": "json_object"},  # keeps output as JSON :contentReference[oaicite:2]{index=2}
    )

    return json.loads(response.choices[0].message.content)
@app.post("/generate-testcases")
def generate(request: FeatureRequest):
    result = generate_test_cases(request.feature)
    return result