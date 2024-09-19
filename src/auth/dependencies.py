import redis

def get_cache() -> redis.Redis:
    client = redis.Redis(host='redis', port=6379)
    return client