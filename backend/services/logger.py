import logging
import json
import os
import datetime

logger = logging.getLogger("lens4u")
handler = logging.StreamHandler()
formatter = logging.Formatter('%(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

def log_event(event_type: str, data: dict):
    payload = {"event": event_type, "data": data}
    logger.info(json.dumps(payload))

# os.makedirs("logs", exist_ok=True)

# usage_logger = logging.getLogger("lens4u.usage")
# usage_handler = logging.FileHandler("logs/usage.json", encoding="utf-8")
# usage_handler.setFormatter(logging.Formatter("%(message)s"))
# usage_logger.addHandler(usage_handler)
# usage_logger.setLevel(logging.INFO)

# qa_logger = logging.getLogger("lens4u.qa")
# qa_handler = logging.FileHandler("logs/qa.json", encoding="utf-8")
# qa_handler.setFormatter(logging.Formatter("%(message)s"))
# qa_logger.addHandler(qa_handler)
# qa_logger.setLevel(logging.INFO)

# def log_usage(session_id: str, tokens: int, cost_usd: float):
#     payload = {
#       "event": "OPENAI_USAGE",
#       "session_id": session_id,
#       "tokens": tokens,
#       "cost_usd": cost_usd,
#       "timestamp": datetime.utcnow().isoformat()
#     }
#     usage_logger.info(json.dumps(payload))

# def log_qa(event_type: str, session_id: str, query: str, score: float | None = None):
#     payload = {
#       "event": event_type,
#       "session_id": session_id,
#       "query": query,
#       "top_score": score,
#       "timestamp": datetime.utcnow().isoformat()
#     }
#     qa_logger.info(json.dumps(payload))