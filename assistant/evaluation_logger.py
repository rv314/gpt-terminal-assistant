import json
import os
from datetime import datetime


EVAL_LOG_FILE = "logs/eval_log.jsonl"

# Confirm directory exists
os.makedirs("logs", exist_ok=True)


def log_eval(query, context_results, response):
  log_entry = {
    "timestamp": datetime.now().isoformat(),
    "query": query,
    "top_k_context": [
      {"text": doc, "score": score} for doc, score in context_results
    ],
    "response": response,
    "context_used": bool(context_results)
  }

  with open(EVAL_LOG_FILE, "a", encoding="utf-8") as f:
    f.write(json.dumps(log_entry) + "\n")