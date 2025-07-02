import os
import openai
from dotenv import load_dotenv
from assistant.vector_store import VectorStore
from uuid import uuid4
from assistant.token_utils import trim_messages

load_dotenv()
store = VectorStore()
openai.api_key = os.getenv("OPENAI_API_KEY")

""" response = openai.chat.completions.create(
  model = "gpt-3.5-turbo",
  messages=[
    {"role":"system", "content": "You are a helpful assistant"},
    {"role":"user", "content": "Hello, what can you do?"}
  ]
)

print(response.choices[0].message.content) """


messages = [
  {"role": "system", "content": "You are a helpful terminal assistant. You provide short, brief and crisp responses."}
]

print("🧠 GPT Terminal Assistant (type 'exit' to quit)\n")

while True:
  user_input = input("You: ")

  if user_input.lower() in {"exit", "quit"}:
    print("Goodbye!")
    break
  
  messages.append({"role": "user", "content": user_input})
  store.add_message(user_input, "user") # store embedding
  model = "gpt-3.5-turbo"
  # Trim messages to fit within 3000 token budget
  messages = trim_messages(messages, model, max_tokens=3000)

  try:
    response = openai.chat.completions.create(
      model=model,
      messages=messages
    )

    reply = response.choices[0].message.content
    print(f'Assistant: {reply}\n')
    messages.append({"role": "assistant", "content": reply})
    store.add_message(reply, "assistant") # store embedding
    
  except Exception as e:
    print(f"[Error] {e}")