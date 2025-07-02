# tests/test_chat_client.py

from assistant.chat_client import chat

def test_chat():
  messages = [
    {"role": "system", "content": "You are helpful assistant."},
    {"role": "user", "content": "What is your purpose?"}
  ]

  reply = chat(messages)
  assert isinstance(reply, str) and len(reply) > 0
  print("✅ test_chat_with_gpt passed.")


if __name__ == '__main__':
  test_chat()