import openai
import os
from langchain_chroma.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.schema import Document
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

class VectorStore:
  
  def __init__(self, collection_name="chat_vectors"):
    base_path = os.path.dirname(os.path.dirname(__file__)) # go to project root
    self.vector_dir = os.path.join(base_path, "vectors")
    os.makedirs(self.vector_dir, exist_ok=True)

    collection_path = os.path.join(self.vector_dir, collection_name)
    self.embedding_fn = OpenAIEmbeddings()

    self.store = Chroma(
      embedding_function=self.embedding_fn,
      collection_name=collection_name,
      persist_directory=self.vector_dir
    )

    #self.store.persist()
  
  
  def embed(self, text: str):
    response = openai.embeddings.create(
      input=[text],
      model="text-embedding-3-small",
      
    )
    return response.data[0].embedding
  

  def add_message(self, text: str, role: str, uuids: str):
    # embeddings = self.embed(text=text)
    doc = Document(page_content=f"{role}: {text}", metadata={"role": role})
    self.store.add_documents(documents=[doc], ids=uuids)
    #self.store.persist()


  def add_documents(self, texts: list, uuids: str, role: str):
    docs = [Document(page_content=f"{text}", metadata={"role": role}) for text in texts]
    self.store.add_documents(documents=docs, ids=uuids)
    

  
  def search_similar(self, query: str, k: int = 5):
    docs = self.store.similarity_search(query, k=k)
    return [doc.page_content for doc in docs]
  

  def list_all(self, k: int = 1000):
    docs = self.store.similarity_search("", k=k)
    return [[doc.page_content, doc.id] for doc in docs]
  

  def get_uuid(self, k: int = 1000):
    docs = self.store.similarity_search("", k=k)
    return [[doc.id] for doc in docs]
  

  def update(self, uuid: str, input_text: str, role: str):
    doc = Document(page_content=f"{role}: {input_text}", metadata={"role": role})
    self.store.update_document(document_id=uuid, document=doc)
    