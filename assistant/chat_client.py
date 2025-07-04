# assistant/chat_client.py
import openai
import os
from dotenv import load_dotenv
from assistant.token_utils import trim_messages
from assistant.vector_store import VectorStore


load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
model = "gpt-3.5-turbo"
vector_store = VectorStore()

def chat(messages, model=model, max_tokens=3000):
  user_input = messages[-1]["content"]
  context_results = vector_store.get_top_k(user_input, k=3)

  # Build a single context string for system prompt
  context_text = "\n---\n".join([doc for doc, _ in context_results]) if context_results else ""


  system_prompt = [
    {"role": "system",
     "content": "You are a helpful terminal assistant. You provide short, brief and crisp responses."
     + (f"\nUse the following previous Q&A for context:\n{context_text}" if context_text else "")
     }]

  # Build full prompt
  full_prompt = system_prompt + messages[-2:]
  full_prompt = trim_messages(full_prompt, model=model, max_tokens=max_tokens)

  resp = openai.chat.completions.create(
    model=model,
    messages=full_prompt
  )

  reply = resp.choices[0].message.content

  vector_store.add_message(user_input, reply)

  return reply