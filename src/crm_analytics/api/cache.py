import json
import redis as redis_lib

_client = redis_lib.Redis(host="localhost", port=6379, decode_responses=True)

def cached(key: str, ttl: int = 5):
    def decorator(fn):
        def wrapper(*args, **kwargs):
            cached_val = _client.get(key)
            if cached_val:
                return json.loads(cached_val)
            result = fn(*args, **kwargs)
            _client.setex(key, ttl, json.dumps(result))
            return result
        return wrapper
    return decorator
