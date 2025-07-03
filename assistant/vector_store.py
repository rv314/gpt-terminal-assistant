# TODO: uuid not working as an argument, might as well leave it 
#       to the library to perform the function of adding uuid
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
    
  
  def add_message(self, role: str, content: str):
    """Embed and store a message in the Chroma vector DB."""
    embeddings = self.embedder.embed_query(content)
    self.collection.add(
      documents=[content],
      embeddings=[embeddings],
      ids=[f"{role}_{hash(content)}"]
    )


  def get_top_k(self, query, k=3):
    """Retrieve top-k similar messages from vector DB based on query."""
    embeddings = self.embedder.embed_query(query)
    results = self.collection.query(
      query_embeddings=[embeddings],
      n_results=k
    )
    return results["documents"][0] if results["documents"] else []

  def add_documents(self, texts: list, role: str, uuids: str = None):
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
    self.store.update_document(document_id=uuid, document=doc)
    