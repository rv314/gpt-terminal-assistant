from assistant.vector_store import VectorStore
import sys
from uuid import uuid4
import asyncio

def test_vectorstore_basic():
  store = VectorStore()
  

  # Add message
  #store.add_message("I love programming in Python", "user")
  #store.add_message("Python is awesome", "assistant")
  #store.add_message("We are using Vlite for vector store", "user")

  # Add messages
  documents = ["I love programming in Python", "Python is awesome", "We are using Vlite for vector store"]
  uuids = [str(uuid4()) for _ in range(len(documents))]

  store.add_documents(documents, uuids, "user")
  # Search
  results = store.search_similar("Tell me about Python", k=1)

  print("Search: ", results)
  print("All: ", store.list_all())

  store.update(str(uuids[-1]), "We switched vector store to Chroma", "user")
  print("Updated: ", store.list_all())
  
def test_vectorstore_single():
  store = VectorStore()
  

  # Add message
  #store.add_message("I love programming in Python", "user")
  #store.add_message("Python is awesome", "assistant")
  temp_uuid = str(uuid4())
  store.add_message("We are using Chroma for vector store", "user")
  print("All: ", store.list_all())

if __name__ == "__main__":
  print(f"Executing from {sys.executable}")
  #test_vectorstore_basic()
  test_vectorstore_single()