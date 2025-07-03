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
  history = vector_store.get_top_k(user_input, k=3)

  full_prompt = [{"role": "system", "content": "You are a helpful terminal assistant. You provide short, brief and crisp responses."}]

  for msg in history:
    full_prompt.append({"role": "user", "content": msg})
  full_prompt.extend(messages[-2:])
  full_prompt = trim_messages(full_prompt, model=model, max_tokens=max_tokens)

  resp = openai.chat.completions.create(
    model=model,
    messages=full_prompt
  )

  reply = resp.choices[0].message.content

  vector_store.add_message("user", user_input)
  vector_store.add_message("assistant", reply)

  return reply