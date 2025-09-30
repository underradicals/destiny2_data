from asyncio import gather
import os
from pathlib import Path
from httpx import AsyncClient, Client, HTTPError
from time import perf_counter_ns
from clients import get_cache, get_cache_async, set_cache, set_cache_async
import aiofiles
from config import DATA


def fetch(url: str, client: Client, cache_key: str | None = None):
    if cache_key:
        cache_response = get_cache(cache_key)
        if cache_response:
            return cache_response

    try:
        start = perf_counter_ns()
        response = client.get(url)
        end = perf_counter_ns()
        response.raise_for_status()
        data = response.text
        print(
            f"Fetched {url} (took {(end - start) / 1_000_000} ms) (bytes: {len(data)})"
        )
        if cache_key:
            set_cache(cache_key, data, ex=3600)
        return data
    except HTTPError as e:
        print(f"Error fetching {url}: {e}")
        data = ""
    finally:
        pass


def download(url: str):
    with Client(
        http2=True,
        base_url="https://www.bungie.net",
        follow_redirects=True,
        headers={"x-api-key": os.getenv("D2_API_KEY") or ""},
    ) as client:
        return fetch(
            url,
            client,
            cache_key=f"manifest:{url.replace('https://', '').replace('/', '_')}",
        )


async def fetch_async(
    url: str, file_path: str | Path, client: AsyncClient, cache_key: str
):
    if cache_key:
        cache_response = await get_cache_async(cache_key)
        if cache_response:
            return cache_response

    try:
        start = perf_counter_ns()
        response = await client.get(url)
        end = perf_counter_ns()
        response.raise_for_status()
        data = response.text
        print(
            f"Cache hit for {url} (took {(end - start) / 1_000_000} ms) (bytes: {len(data)})"
        )
        if cache_key:
            await set_cache_async(cache_key, data, ex=3600)

        start_f = perf_counter_ns()
        async with aiofiles.open(file_path, "wb") as f:
            async for chunk in response.aiter_bytes():
                await f.write(chunk)
        end_f = perf_counter_ns()
        print(f"Wrote to {file_path} (took {(end_f - start_f) / 1_000_000} ms)")
    except HTTPError as e:
        print(f"Error fetching {url}: {e}")
        data = ""
    finally:
        pass


async def download_all_async(urls: list[str] | tuple[str, str]) -> None:
    async with AsyncClient(
        http2=True,
        base_url="https://www.bungie.net",
        follow_redirects=True,
        headers={"x-api-key": os.getenv("D2_API_KEY") or ""},
    ) as client:
        tasks = [
            fetch_async(
                url,
                f"{DATA}/{name}.json",
                client,
                cache_key=f"manifest:{url.replace('https://', '').replace('/', '_')}",
            )
            for name, url in urls
        ]
        await gather(*tasks)
