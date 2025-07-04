# assistant/cli.py - main entry

from assistant.chat_client import chat
from assistant.vector_store import VectorStore
from assistant.evaluation_logger import log_eval

vector_store = VectorStore()

def main(debug: bool):

  print("🧠 GPT Terminal Assistant — Type 'exit' to quit")  

  while True:
    user_input = input("👤 You: ")
    if user_input.lower() in ["quit", "exit"]:
      break

    context_results = vector_store.get_top_k(user_input, k=3)
    context_docs = [doc for doc, score in context_results]

    # Only user input is passed, system/context is handled in chat_client
    messages = [
      {"role": "user", "content": user_input}
    ]

    if debug:
      print(f"\n🛠️ Retrieved {len(context_docs)} context message(s):")
      for idx, (doc, score) in enumerate(context_results, 1):
        print(f"  [{idx}] (score: {score:.4f}) {doc}")
        print(f"Total vector store count: {vector_store.collection.count()}")

    reply = chat(messages)
    print(f"🤖 GPT: {reply}")

    # Log for RAG evaluation
    log_eval(query=user_input, context_results=context_results, response=reply)

if __name__ == '__main__':
  main(debug=False)
  
