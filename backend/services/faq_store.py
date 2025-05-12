import os, json
import pickle
import numpy as np
from openai import OpenAI

current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
EMBED_CACHE_FILE = os.path.join(parent_dir,"data", "faqs_embeddings.pkl")
EMBED_MODEL = "text-embedding-3-small"
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

FAQ_ENTRIES: dict[str, dict] = {}
FAQ_VECS: list[tuple[str, np.ndarray]] = []

def initialize_faq_store():
    global FAQ_ENTRIES, FAQ_VECS
    if os.path.exists(EMBED_CACHE_FILE):
        with open(EMBED_CACHE_FILE, "rb") as f:
            cached_entries, cached_vecs = pickle.load(f)
        FAQ_ENTRIES.clear()
        FAQ_ENTRIES.update(cached_entries)
    else:
        cached_vecs = {}

    with open("data/faqs.jsonl", "r") as f:
        for line in f:
            obj = json.loads(line)
            fid = obj["id"]
            FAQ_ENTRIES[fid] = obj

    new_vecs = {}

    for fid, entry in FAQ_ENTRIES.items():
        if fid in cached_vecs:
            vec = cached_vecs[fid]
        else:
            resp = client.embeddings.create(
                model=EMBED_MODEL,
                input=entry["question"]
            )
            vec = np.array(resp.data[0].embedding, dtype=np.float32)
            new_vecs[fid] = vec
        FAQ_VECS.append((fid, vec))

    all_vecs = {**cached_vecs, **new_vecs}
    with open(EMBED_CACHE_FILE, "wb") as f:
        pickle.dump((FAQ_ENTRIES, all_vecs), f)