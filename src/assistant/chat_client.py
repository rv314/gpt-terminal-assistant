# assistant/chat_client.py
from utils.token_limits import trim_messages
from typing import List, Dict
from utils.debug import debug_log, print_eval_log, print_vector_results
from utils.evaluation_logger import log_eval

from registries.vector_registry import get_vector_db
from registries.embedding_registry import get_embedder
from registries.llm_registry import get_llm
from utils.prompt_loader import load_prompt_template

from llm.openai_llm import OpenAIChatModel
from vector_backends.chroma_store import ChromaVectorStore
from embedding_models.openai_embedder import OpenAIEmbedder


class ChatEngine:
  # TODO: decouple LLM API from ChatEngine
  def __init__(self, config: dict):
    self.model = config["llm"]["model"]
    self.max_tokens = config.get("max_tokens", 3000)
    self.debug = config.get("logging", {}).get("debug", False)

    # Register LLM via registry
    self.llm = get_llm(config["llm"]["provider"], config=config["llm"])

    # Register embedder and vector store
    embedder = get_embedder(config["embedding"]["provider"])
    vector_store = get_vector_db(config["vector_store"]["provider"], embedder=embedder)
    self.vector_store = vector_store
  

  def get_context(self, query: str, k: int = 3):
    """Retrieve top-k similar Q&A from vector store to dynamically use as context in system prompt."""
    context_results = self.vector_store.get_top_k(query, k)
    context_text = "\n---\n".join([doc for doc, _ in context_results]) if context_results else ""
    return context_text, context_results
  
  
  def chat(self, messages: List[Dict[str, str]]) -> str:
    """Dynamically builds prompt using context, calls model API -> sends prompt and returns response"""
    user_input = messages[-1]["content"]

    # Step 1. Fetch relevant context
    context_text, context_results = self.get_context(user_input)

    # Step 2. Build system prompt with context if available
    template = load_prompt_template()
    prompt_content = template.replace("{{context}}", context_text if context_text else "")
    system_prompt = {"role": "system", "content": prompt_content}
    
    # Step 3. Trim and finalize message history
    full_prompt = [system_prompt] + messages[-2:] # Only last 2 user/assistant messages
    full_prompt = trim_messages(full_prompt, model=self.model, max_tokens=self.max_tokens)

    # Step 4. Debug if enabled
    if self.debug:
      import json
      print("\n📌 Prompt sent to OpenAI:")
      dumped_json = json.dumps(full_prompt, indent=2)
      print(dumped_json[:1500] + "..." if len(json.dumps(full_prompt)) > 1500 else dumped_json)
      print("\n📌 Context used:", "Yes" if context_text else "No")
      print_vector_results(context_results)
      debug_log(f"User input: {user_input}")
      debug_log(f"Context count: {len(context_results)}")
      for idx, (doc, score) in enumerate(context_results, 1):
        debug_log(f"[{idx}] (score: {score:.4f}) {doc}")

    # Step 5. Get response from model
    try:
      reply = self.llm.chat(full_prompt)
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