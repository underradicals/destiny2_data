from clients import download
from clients.http_client import download_all_async
from services import ManifestService
from orjson import loads
import asyncio

from services.localization import Localization


async def main():
    value = download("https://www.bungie.net/Platform/Destiny2/Manifest/")
    manifest = ManifestService(loads(str(value).encode("utf-8")))
    content_paths_tuples = manifest.json_world_component_content_paths_toTuple(
        Localization.en
    )
    await download_all_async(content_paths_tuples)


if __name__ == "__main__":
    main_couroutine_object = main()
    asyncio.run(main_couroutine_object)
