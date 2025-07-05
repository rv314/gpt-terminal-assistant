# TODO: Check vector DB storage, reduce duplicates

from datetime import datetime
from langchain_openai import OpenAIEmbeddings
from langchain.schema import Document
import chromadb
from chromadb.config import Settings
import os
from pathlib import Path

class VectorStore:
  
  def __init__(self, collection_name="chat_memory", persist_dir="vectors/chroma"):
    # verify persistent folder exists
    persist_path = Path(persist_dir)
    persist_path.mkdir(parents=True, exist_ok=True)

    # Initialize a persistent client
    self.client = chromadb.PersistentClient(path = str(persist_path))
    self.collection = self.client.get_or_create_collection(collection_name)
    self.embedder = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
    
  
  def add_message(self, question: str, answer: str):
    """Embed and store Q&A pair into Chroma vector DB."""
    # content = f"Q: {question.strip()}\nA: {answer.strip()}"
    entry = f"Q: {question}\nA: {answer}"
    entry_id = f"user_{hash(entry)}"

    # Check for existing id to prevent duplicates
    existing = self.collection.get(["documents"])
    existing_ids = existing.get("ids", [])
    if entry_id in existing_ids:
      return
    
    embeddings = self.embedder.embed_query(entry)
    self.collection.add(
      documents=[entry],
      embeddings=[embeddings],
      ids=[entry_id]
    )
    # print(f"🧠 Added to vector store:\n{content[:100]}...\n")


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
    print(f"Docs from vector: {documents}")

    # Filter based on distances threshold (lower = more similar)
    filtered = [
      (doc, dist)
      for doc, dist in zip(documents, distances)
      if dist <= similarity_threshold
    ]

    # print("→ Query:", query)
    # print("→ Raw embedding len:", len(embeddings))
    # print("→ Collection count:", self.collection.count())
    # print("→ Query results:", results)

    return filtered

"""   def add_documents(self, texts: list, role: str, uuids: str = None):
    docs = [Document(page_content=f"{text}", metadata={"role": role}) for text in texts]
    self.store.add_documents(documents=docs, ids=uuids)
    

  
  def search_similar(self, query: str, k: int = 5):
    docs = self.store.similarity_search(query, k=k)
    return [doc.page_content for doc in docs]
  

  def list_all(self, k: int = 1000):
    docs = self.store.similarity_search("", k=k)
    return [[doc.page_content, doc.id, doc.metadata] for doc in docs]
  

  def get_uuid(self, k: int = 1000):
    docs = self.store.similarity_search("", k=k)
    return [[doc.id] for doc in docs]
  

  def update(self, uuid: str, input_text: str, role: str):
    doc = Document(page_content=f"{role}: {input_text}", 
                   metadata={"role": role,
                             "updated": str(datetime.now())})
    self.store.update_document(document_id=uuid, document=doc) """
    