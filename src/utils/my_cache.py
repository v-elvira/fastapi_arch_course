from datetime import date, datetime
import json
from functools import wraps
from src.init import redis_manager
from src.schemas.common import CommonBaseModel

def prepare_params(value):
    try:
        if isinstance(value, (str, int, float, bool, date, datetime)) or value is None:
            return value
        elif isinstance(value, CommonBaseModel):
            return value.model_dump()
        elif isinstance(value, (list, tuple)):
            return [prepare_params(x) for x in value]
        elif isinstance(value, dict):
            return {k: prepare_params(value[k]) for k in sorted(value)}
        elif isinstance(value, (set, frozenset)):
            return [prepare_params(x) for x in sorted(value)]
        else:
            return '#'
    except Exception as ex:
        print(f'Unexpected error: {ex}')
        return '?'

def encode_additional(value):
    if isinstance(value,(date, datetime)):
        return value.isoformat()
    elif isinstance(value, CommonBaseModel):
        return value.model_dump()
    raise TypeError(f'Object of type {value.__class__.__name__} '
                    f'is not JSON serializable')


def get_json(value, for_cache_key=False):
    if for_cache_key:
        return json.dumps(prepare_params(value), default=encode_additional)
    return json.dumps(value, default=encode_additional)


def my_redis_cache(expire=10):
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
