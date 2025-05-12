import os
import hashlib
from typing import List, Dict, Tuple
import numpy as np
from openai import OpenAI
from services.memory import cache_get_vec, cache_set_vec
from services.logger import log_event
# from services.logger import log_qa
from services.faq_store import FAQ_ENTRIES, FAQ_VECS

RAG_CONFIDENCE_THRESHOLD = 0.6
MAX_FAQ_MATCHES = 1  
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
EMBED_MODEL = "text-embedding-3-small"
CHAT_MODEL = "gpt-4o-mini" 

FALLBACK_MESSAGE = (
    "I'm not certain. Please consult an eye-care professional for accurate guidance."
)
SYSTEM_PROMPT = (
    "You are OptometristBot, an AI assistant for contact lens guidance."
    "Answer only based on provided context (FAQ entries). "
    "If you are unsure, use the fallback message."
)

client = OpenAI(api_key=OPENAI_API_KEY)

def cosine(a: np.ndarray, b: np.ndarray) -> float:
    return float(a.dot(b) / (np.linalg.norm(a) * np.linalg.norm(b)))

async def get_answer(question: str, session_id, history: List[Dict],lens_type) -> Tuple[str, List[Dict], Dict]:
    print("DEBUG: FAQ_VECS contains", len(FAQ_VECS), "entries")
    q_hash = hashlib.sha256(question.encode()).hexdigest()
    vec = await cache_get_vec(q_hash)
    if vec is None:
        embed_resp = client.embeddings.create(model=EMBED_MODEL, input=question)
        vec = np.array(embed_resp.data[0].embedding, dtype=np.float32)
        await cache_set_vec(q_hash, vec)
    scores = [(fqid, cosine(vec, fvec)) for fqid, fvec in FAQ_VECS]
    scores.sort(key=lambda x: x[1], reverse=True)
    matches = []
    if scores and scores[0][1] >= RAG_CONFIDENCE_THRESHOLD:
        for fqid, score in scores[:MAX_FAQ_MATCHES]:
            faq = FAQ_ENTRIES[fqid]
            matches.append({
                "id": fqid,
                "answer": faq["answer"],
                "source": faq["source"],
                "score": score,
            })
        log_event("Question Answered", {"query": question, "session_id": session_id, "top_score": scores[0][1]})
        print("Lens type is",lens_type)
        # log_qa("Question Answered", session_id, question, score)
    else:
        log_event("RAG_FALLBACK", {"query": question, "session_id": session_id, "top_score": scores[0][1] if scores else None})
        #log_qa("RAG_FALLBACK", session_id, question, None)
        return FALLBACK_MESSAGE, [], {"tokens": 0, "usd": 0}

    messages = [
        {"role":"system", "content": SYSTEM_PROMPT},
        {"role":"system", "content": f"The user wears {lens_type} lenses."},
    ]
    for msg in history:
        messages.append({"role": msg['role'], "content": msg['content']})
    for faq in matches:
        messages.append({"role": "system", "content": faq['answer']})
    messages.append({"role": "user", "content": question})

    resp = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=messages,
        stream=False
    )
    answer = resp.choices[0].message.content

    citations = [{"id": faq['id'], "source": faq['source']} for faq in matches]

    tokens_used = resp.usage.prompt_tokens + resp.usage.completion_tokens
    cost_usd = tokens_used * 0.00000060

    return answer, citations, {"tokens": tokens_used, "usd": cost_usd}
