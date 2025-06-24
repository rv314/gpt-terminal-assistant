import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

response = openai.chat.completions.create(
  model = "gpt-3.5-turbo",
  messages=[
    {"role":"system", "content": "You are a helpful assistant"},
    {"role":"user", "content": "Hello, what can you do?"}
  ]
)

print(response.choices[0].message.content)