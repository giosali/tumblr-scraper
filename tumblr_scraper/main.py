import argparse
import asyncio
import logging

from . import download
from .blogs import Blog

logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Process arguments for tumblr-scraper."
    )
    parser.add_argument("blog", type=str, help="The name of the tumblr blog.")
    parser.add_argument("-v", "--verbose", help="Enable debugging", action="store_true")
    namespace = parser.parse_args()
    return namespace


def main():
    namespace = parse_args()

    logger.propagate = False
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s: %(message)s", datefmt="[%I:%M:%S %p]"
    )
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logging.basicConfig(level=logging.DEBUG if namespace.verbose else logging.INFO)

    blog = Blog(namespace.blog)
    media = []
    count = 1
    while True:
        logger.info(f"Scraping page {count}")
        page = blog.page
        images = page.get_images()
        videos = page.get_videos()
        media += images + videos
        try:
            blog.go_to_next_page()
        except IndexError:
            break
        count += 1

    asyncio.run(download.prepare_download(media, blog.get_name()))


if __name__ == "__main__":
    main()
