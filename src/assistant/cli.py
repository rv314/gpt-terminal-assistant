# assistant/cli.py - main entry

import os
from dotenv import load_dotenv
from assistant.chat_client import ChatEngine
from utils.debug import str_to_bool
from utils.config import load_config

load_dotenv()

def main():

  print("GPT Terminal Assistant — Type 'exit' to quit")

  # Load full config
  config = load_config()

  # Let user choose a model
  models = config["llm"].get("available_models", [])

  if models:
    print("Available Models:")
    for i, m in enumerate(models, 1):
      print(f"    {i}.  {m}")
    try:
      choice = int(input(f"\nSelect model [1-{len(models)}] (default: 1) ") or 1)
      selected_model = models[choice - 1]
      config["llm"]["model"] = selected_model
    except (ValueError, IndexError):
      print("Invalid choice. Using default.")

  #print(f"In CLI Debug is set to: {debug}")

  # Initialize ChatEngine with full config
  chat_engine = ChatEngine(config=config)

  messages = []

  while True:
    user_input = input("You: ")
    if user_input.lower() in ["quit", "exit"]:
      print("Goodbye!!")
      break

    # Only user input is passed, system/context is handled in chat_client
    messages.append({"role": "user", "content": user_input})
    reply = chat_engine.chat(messages)
    messages.append({"role": "assistant", "content": reply})
    print(f"GPT: {reply}")

if __name__ == '__main__':
  main()
  
