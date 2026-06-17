"""Milestone 4 — Embedding, vector store, and retrieval.

Builds a persistent ChromaDB collection from chunks.jsonl using
all-MiniLM-L6-v2 embeddings (per planning.md), and exposes retrieve()
for semantic search.

    Build the index:   python vectorstore.py
    Query it:          from vectorstore import retrieve
                       retrieve("can I get a refund?", k=5)

Distances use cosine space, so a score is 1 - cosine_similarity:
0.0 = identical meaning, lower is better. Good matches are well below 0.5.
"""

from __future__ import annotations

import json
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

BASE = Path(__file__).parent
CHUNKS_PATH = BASE / "chunks.jsonl"
CHROMA_DIR = str(BASE / "chroma_db")
COLLECTION_NAME = "parking_chunks"
MODEL_NAME = "all-MiniLM-L6-v2"

_model: SentenceTransformer | None = None


def get_model() -> SentenceTransformer:
    """Load the embedding model once and reuse it."""
    global _model
    if _model is None:
        _model = SentenceTransformer(MODEL_NAME)
    return _model


def _embed(texts: list[str]) -> list[list[float]]:
    # Normalised vectors so cosine distance is well-behaved.
    return get_model().encode(texts, normalize_embeddings=True).tolist()


def get_client() -> chromadb.ClientAPI:
    return chromadb.PersistentClient(path=CHROMA_DIR)


def get_collection():
    """Return the existing collection (cosine space)."""
    return get_client().get_or_create_collection(
        name=COLLECTION_NAME, metadata={"hnsw:space": "cosine"}
    )


def load_chunks() -> list[dict]:
    return [json.loads(line) for line in CHUNKS_PATH.open(encoding="utf-8")]


def build_index() -> None:
    """Embed every chunk and (re)build the ChromaDB collection from scratch."""
    chunks = load_chunks()
    if not chunks:
        print("No chunks in chunks.jsonl — run `python build_chunks.py` first.")
        return

    client = get_client()
    # Drop any old collection so re-running never duplicates chunks.
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME, metadata={"hnsw:space": "cosine"}
    )

    texts = [c["text"] for c in chunks]
    print(f"Embedding {len(texts)} chunks with {MODEL_NAME} ...")
    embeddings = _embed(texts)

    collection.add(
        ids=[c["chunk_id"] for c in chunks],
        embeddings=embeddings,
        documents=texts,
        metadatas=[
            {
                "source": c["source"],
                "source_type": c["source_type"],
                "url": c.get("url", ""),
                "filename": c["filename"],
                "position": int(c["chunk_id"].split("::")[1]),
            }
            for c in chunks
        ],
    )
    print(f"Stored {collection.count()} chunks in ChromaDB at {CHROMA_DIR}/ "
          f"(collection '{COLLECTION_NAME}').")


def retrieve(query: str, k: int = 5) -> list[dict]:
    """Return the top-k most similar chunks with metadata and distance."""
    result = get_collection().query(
        query_embeddings=_embed([query]),
        n_results=k,
        include=["documents", "metadatas", "distances"],
    )
    hits = []
    for doc, meta, dist in zip(
        result["documents"][0], result["metadatas"][0], result["distances"][0]
    ):
        hits.append({"text": doc, "distance": dist, **meta})
    return hits


if __name__ == "__main__":
    build_index()
