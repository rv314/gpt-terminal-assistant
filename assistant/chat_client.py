# assistant/chat_client.py
import openai
import os
from dotenv import load_dotenv
from assistant.token_utils import trim_messages


load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
model = "gpt-3.5-turbo"

def chat(messages, model=model, max_tokens=3000):
  messages = trim_messages(messages, model, max_tokens=max_tokens)
  respone = openai.chat.completions.create(
    model=model,
    messages=messages
  )

  return respone.choices[0].message.content