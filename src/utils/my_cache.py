# not used, replaced with fastapi_cache.decorator.cache from fastapi-cache2

from datetime import date, datetime
import json
from functools import wraps
from src.init import redis_manager
from src.schemas.common import CommonBaseModel

def serialize(value, filter=False):
    if isinstance(value,(date, datetime)):
        return value.isoformat()
    elif isinstance(value, CommonBaseModel):
        return value.model_dump()
    if filter:
        return '#'
    raise TypeError(f'Object of type {value.__class__.__name__} is not JSON serializable')


def get_json(value, for_cache_key=False):
    if for_cache_key:
        return json.dumps(value, default=lambda x: serialize(x, filter=True), sort_keys=True)
    return json.dumps(value, default=serialize)


def my_redis_cache(expire=10): # replaced with fastapi_cache.decorator.cache
    def decorator(f):
        @wraps(f)
        async def wrapper(**kwargs):
            key = f'{f.__name__}|{get_json(kwargs, for_cache_key=True)}'
            from_cache = await redis_manager.get(key)
            if not from_cache:
                print(f'DB query from {f.__name__}...')
                result = await f(**kwargs)
                value = get_json(result)
                await redis_manager.set(key, value, expire=expire)
                return result
            else:
                return json.loads(from_cache)
        return wrapper
    return decorator
