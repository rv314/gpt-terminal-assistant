# assistant/cli.py - main entry

import sys
from assistant.chat_client import chat

def main():
  print("🧠 GPT Terminal Assistant — Type 'exit' to quit")

  messages = [
  {"role": "system", "content": "You are a helpful terminal assistant. You provide short, brief and crisp responses."}
  ]

  while True:
    user_input = input("👤 You: ")
    if user_input.lower() in ["quit", "exit"]:
      break


    messages.append({"role": "user", "content": user_input})
    reply = chat(messages)
    print(f"🤖 GPT: {reply}")
    messages.append({"role": "assitant", "content": reply})


if __name__ == '__main__':
  main()
  
