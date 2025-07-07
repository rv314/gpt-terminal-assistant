# assistant/cli.py - main entry

from assistant.chat_client import ChatEngine
from utils.evaluation_logger import log_eval
import os
from dotenv import load_dotenv
from utils.debug import str_to_bool

load_dotenv()
debug = str_to_bool(os.getenv("DEBUG", "false"))

def select_model():
    models = ["gpt-3.5-turbo", "gpt-4"]
    
    print("\nAvailable Models:")
    for i, m in enumerate(models, 1):
        print(f"  {i}. {m}")
    
    while True:
        try:
            choice = int(input("\nEnter model number (default: 1): ") or 1)
            if 1 <= choice <= len(models):
                return models[choice - 1]
            else:
                print(f"Invalid choice. Please select a number between 1 and {len(models)}.")
        except ValueError:
            print("⚠️ Please enter a valid number.")

def main():

  print("GPT Terminal Assistant — Type 'exit' to quit")  

  # Let user choose a model
  selected_model = select_model()
  print(f"\n Using model: {selected_model}")
  #print(f"In CLI Debug is set to: {debug}")
  chat_engine = ChatEngine(model=selected_model, debug=debug)

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
  
