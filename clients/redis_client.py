from time import perf_counter_ns
from redis import Redis as RedisSync
from redis.asyncio import Redis as AsyncRedis


def get_redis_client() -> RedisSync:
    return RedisSync(host="172.19.80.1", port=6379, db=0)


def get_redis_client_async() -> AsyncRedis:
    return AsyncRedis(host="172.19.80.1", port=6379, db=0)


r_async = get_redis_client_async()
r_sync = get_redis_client()


async def get_cache_async(key: str) -> str | None:
    start = perf_counter_ns()
    cached_response = await r_async.get(key)
    end = perf_counter_ns()
    if cached_response:
        data: str = cached_response.decode("utf-8")
        print(
            f"Cache hit for {key} (took {(end - start) / 1_000_000} ms) bytes: {len(data)}"
        )
        return data
    else:
        return None


def get_cache(key: str) -> str | None:
    start = perf_counter_ns()
    cached_response = r_sync.get(key)
    end = perf_counter_ns()
    if cached_response:
        data: str = cached_response.decode("utf-8")  # type: ignore
        print(
            f"Cache hit for {key} (took {(end - start) / 1_000_000} ms) bytes: {len(data)}"
        )
        return data
    else:
        return None


def set_cache(key: str, value: str, ex: int | None = None) -> None:
    r_sync.set(key, value, ex=ex)


async def set_cache_async(key: str, value: str, ex: int | None = None) -> None:
    v = await r_async.set(key, value, ex=ex)
    return v
