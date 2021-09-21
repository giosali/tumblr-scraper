import asyncio
import pathlib
import traceback
from typing import List

import httpx
from tqdm import tqdm

from . import utils


async def prepare_download(media: List[str], blog_name: str):
    path = pathlib.Path().cwd() / blog_name
    path.mkdir(exist_ok=True)

    limits = httpx.Limits(max_connections=5, max_keepalive_connections=4)
    transport = httpx.AsyncHTTPTransport(limits=limits, retries=5)
    async with httpx.AsyncClient(timeout=None, limits=limits, transport=transport) as c:
        tasks = [asyncio.create_task(download(c, path, uri)) for uri in media]

        with tqdm(desc="Downloading", total=len(tasks), ascii=True) as bar:
            for coro in asyncio.as_completed(tasks):
                try:
                    await coro
                except Exception:
                    print(traceback.format_exc())
                bar.update()
            bar.set_description(desc="Complete")


async def download(c: httpx.AsyncClient, path: pathlib.Path, uri: str):
    try:
        async with c.stream("GET", uri) as r:
            r.raise_for_status()
            total = r.headers.get("Content-Length")

            filename = utils.extract_filename(uri)
            with tqdm(
                desc=filename,
                total=int(total) if total else None,
                leave=False,
                ascii=True,
                unit="B",
                unit_scale=True,
                unit_divisor=1024,
            ) as bar:
                num_bytes_downloaded = r.num_bytes_downloaded
                with open(path / filename, "wb") as f:
                    async for chunk in r.aiter_bytes(chunk_size=1024):
                        f.write(chunk)
                        bar.update(r.num_bytes_downloaded - num_bytes_downloaded)
                        num_bytes_downloaded = r.num_bytes_downloaded

    except httpx.HTTPStatusError:
        pass
