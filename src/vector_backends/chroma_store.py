from chromadb import PersistentClient
from chromadb.config import Settings
from pathlib import Path
from registries.vector_registry import register_vector_db
from utils.config import load_config

@register_vector_db("chroma")
class ChromaVectorStore():
  def __init__(self, config: dict = None, embedder = None):
    if embedder is None:
      raise ValueError("Embedder must be provided for vector store.")
    self.embedder = embedder

    # Load config if not passed.
    config = config or load_config()
    vector_config = config.get("vector_store", {})

    # Get persistent path from config or fallback
    persist_path = vector_config.get("persist_directory", "vectors/chroma")
    persist_dir = Path(persist_path)
    persist_dir.mkdir(parents=True, exist_ok=True)

    # Initialize Chroma client
    self.client = PersistentClient(path=str(persist_dir))
    self.collection = self.client.get_or_create_collection(name="terminal-assistant")


  def add_message(self, question: str, answer: str):
    """Embed and store Q&A pair into Chroma vector DB."""
    entry = f"Q: {question.strip()}\nA: {answer.strip()}"
    entry_id = f"user_{hash(entry)}"

    # Check for duplicate
    existing = self.collection.get(include=["documents", "ids"])
    existing_ids = existing.get("ids", [])
    if entry_id in existing_ids:
        return  # Skip if already added

    embedding = self.embedder.embed_query(entry)
    self.collection.add(
        documents=[entry],
        embeddings=[embedding],
        ids=[entry_id]
    )

  def get_top_k(self, query: str, k: int = 3, similarity_threshold: float = 0.3) -> list[tuple[str, float]]:
    """Retrieve top-k similar Q&A messages from vector DB."""
    embeddings = self.embedder.embed_query(query)

    results = self.collection.query(
        query_embeddings=[embeddings],
        n_results=k,
        include=["documents", "distances"]
    )

    documents = results.get("documents", [[]])[0]
    distances = results.get("distances", [[]])[0]

    filtered = [
        (doc, dist)
        for doc, dist in zip(documents, distances)
        if dist <= similarity_threshold
    ]

    return filtered
  
