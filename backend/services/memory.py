import os, json
import numpy as np
import redis.asyncio as redis

_pool: redis.Redis | None = None

async def init_pool():
    global _pool
    _pool = redis.from_url(os.getenv("REDIS_URL"), decode_responses=True)

async def get_history(sid: str) -> list:
    raw = await _pool.get(f"session:{sid}")
    return json.loads(raw) if raw else []

async def append_history(sid: str, role: str, content: str):
    hist = await get_history(sid)
    hist.append({"role": role, "content": content})
    await _pool.set(f"session:{sid}", json.dumps(hist), ex=1800)

async def cache_get_vec(text_hash: str):
    data = await _pool.get(f"emb:{text_hash}")
    return np.frombuffer(bytes.fromhex(data), dtype=np.float32) if data else None

async def cache_set_vec(text_hash: str, vec):
    await _pool.set(f"emb:{text_hash}", vec.tobytes().hex(), ex=604800)

async def get_profile(sid: str) -> dict:
    raw = await _pool.get(f"profile:{sid}")
    return json.loads(raw) if raw else {}

async def set_profile(sid: str, profile: dict):
    await _pool.set(f"profile:{sid}", json.dumps(profile), ex=3600)

