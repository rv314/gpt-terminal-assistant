# assistant/cli.py - main entry

import sys
from assistant.chat_client import chat
from assistant.vector_store import VectorStore

vector_store = VectorStore()

def main(debug: bool):

  print("🧠 GPT Terminal Assistant — Type 'exit' to quit")  

  while True:
    user_input = input("👤 You: ")
    if user_input.lower() in ["quit", "exit"]:
      break

    vector_store.add_message("user", user_input)
    context_docs = vector_store.get_top_k(user_input, k=3)
    context_text = "\n".join(context_docs)

    # Build context aware system messages
    system_prompt = (
      f"You are a helpful terminal assistant. You provide short, brief and crisp responses. Use the following previous messages for context:\n\n{context_text}"
    )

    messages = [
      {"role": "system", "content": system_prompt},
      {"role": "user", "content": user_input}
    ]

    if debug:
      # verify message added to vector db by querying it back
      print("\n Verifying message added to vector store")
      results = vector_store.get_top_k(user_input, k=1)
      print(f"Retrieved: {results}")
      print(f"Collection count: {vector_store.collection.count()}")
      if context_docs:
        print(f"\n Retrieved {len(context_docs)} context messages:")
        for idx, doc in enumerate(context_docs, 1):
          print(f"   [{idx}] {doc}")

    #messages.append({"role": "user", "content": user_input})

    reply = chat(messages)
    print(f"🤖 GPT: {reply}")
    messages.append({"role": "assistant", "content": reply})

if __name__ == '__main__':
  main(debug=True)
  
