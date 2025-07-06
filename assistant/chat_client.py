# assistant/chat_client.py
import openai
import os
from dotenv import load_dotenv
from utils.token_limits import trim_messages
from assistant.vector_store import VectorStore
from typing import List, Dict
from utils.debug import debug_log, print_eval_log, print_vector_results
from utils.evaluation_logger import log_eval


load_dotenv()


class ChatEngine:
  def __init__(self, model: str = "gpt-3.5-turbo", max_tokens: int = 3000, debug: bool = False):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    self.model = model
    self.max_tokens = max_tokens
    self.vector_store = VectorStore()
    self.debug = debug

    # Automaticall detect provider based on model
    if model.startswith("gpt-"):
      self.provider = "openai"
    else:
      raise ValueError(f"Unsupported model: {model}")
  
  def get_context(self, query: str, k: int = 3):
    """Retrieve top-k similar Q&A from vectore store to dynamically use as context in system prompt."""
    context_results = self.vector_store.get_top_k(query, k)
    context_text = "\n---\n".join([doc for doc, _ in context_results]) if context_results else ""
    return context_text, context_results
  
  def chat(self, messages: List[Dict[str, str]]) -> str:
    """Dynamically builds prompt using context, calls model API -> sends prompt and returns response"""
    user_input = messages[-1]["content"]

    # Step 1. Fetch relevant context
    context_text, context_results = self.get_context(user_input)

    # Step 2. Build system prompt with context if available
    system_prompt = {"role": "system",
      "content": "You are a helpful terminal assistant. You provide short, brief and crisp responses."
      + (f"\nUse the following previous Q&A for context:\n{context_text}" if context_text else "")
      }
    
    # Step 3. Trim and finalize message history
    full_prompt = [system_prompt] + messages[-2:] # Only last 2 user/assistant messages
    full_prompt = trim_messages(full_prompt, model=self.model, max_tokens=self.max_tokens)

    # Step 4. Debug if enabled
    if self.debug:
      import json
      print("\n📌 Prompt sent to OpenAI:")
      print(json.dumps(full_prompt, indent=2)[:1500] + "..." if len(json.dumps(full_prompt)) > 1500 else json.dumps(full_prompt, indent=2))
      print("\n📌 Context used:", "Yes" if context_text else "No")
      print_vector_results(context_results)
      debug_log(f"User input: {user_input}")
      debug_log(f"Context count: {len(context_results)}")
      for idx, (doc, score) in enumerate(context_results, 1):
        debug_log(f"[{idx}] (score: {score:.4f}) {doc}")

    # Step 5. Get response from model
    try:
      reply = self._call_model(full_prompt)
    except Exception as e:
      reply = "An error occured while generating response, Check logs."
      debug_log(f"Model API error: {e}")

    # Step 6. Log results
    log_eval(user_input, context_results, reply)
    if self.debug:
      print(f"In chat_client Debug is set to: {self.debug}")
      print_eval_log(user_input, context_results, reply)

    # Step 7. Add messages to vector DB
    self.vector_store.add_message(user_input, reply)

    return reply
  
  def _call_model(self, prompt: List[Dict[str, str]]) -> str:
    if self.provider == "openai":
      response = openai.chat.completions.create(
        model=self.model,
        messages=prompt
        )
      return response.choices[0].message.content

    raise NotImplementedError(f"Provider '{self.provider}' not yet implemented.")