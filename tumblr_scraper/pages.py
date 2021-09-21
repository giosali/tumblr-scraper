import mimetypes
from typing import List
from urllib.parse import urlparse

import httpx
from bs4 import BeautifulSoup, element

from . import constants
from .http import HttpMixin


class Page(HttpMixin):
    def __init__(self, page: element.Tag, blog_name: str):
        self.page: element.Tag = page
        self.blog_name: str = blog_name

    def get_images(self) -> List[str]:
        """
        Returns a list of URIs of images/gifs from the tumblr page.
        """

        images = []
        soup = BeautifulSoup(self.page, "html.parser")
        articles = soup.find_all("article", "not-page")
        for article in articles:
            figures = article.find_all("figure")
            for figure in figures:
                iframe = figure.find("iframe")
                if iframe:
                    src = iframe.get("src")
                    images += self.__get_images_from_iframe(src)
                else:
                    a_tags = figure.find_all("a")
                    if a_tags:
                        for a_tag in a_tags:
                            img = a_tag.find("img")
                            if img and not self.__is_from_reblog(img):
                                data_big_photo = a_tag.get("data-big-photo")
                                href = a_tag.get("href")
                                src = img.get("src")
                                if href != constants.COMMUNITY_POLICY:
                                    images.append(
                                        data_big_photo
                                        or (
                                            href
                                            if (mimetypes.guess_type(href)[0])
                                            else None
                                        )
                                        or src
                                    )
                    else:
                        imgs = figure.find_all("img")
                        for img in imgs:
                            if not self.__is_from_reblog(img):
                                images.append(img.get("src"))
        return images

    def get_videos(self) -> List[str]:
        """
        Returns a list of URIs of videos from the tumblr page.
        """

        videos = []
        soup = BeautifulSoup(self.page, "html.parser")
        articles = soup.find_all("article", "not-page")
        for article in articles:
            figures = article.find_all("figure")
            for figure in figures:
                iframe = figure.find("iframe")
                if iframe:
                    src = iframe.get("src")
                    src = self.__get_videos_from_iframe(src)
                    if src:
                        videos.append(src)
                else:
                    sources = figure.find_all("source")
                    for source in sources:
                        videos.append(source.get("src"))
        return videos

    def has_posts(self) -> bool:
        soup = BeautifulSoup(self.page, "html.parser")
        page = soup.find(id="page")
        div = page.find("div", constants.NO_POSTS_CLASS)
        if div:
            return False
        return True

    def __get_images_from_iframe(self, src: str) -> List[str]:
        try:
            o = urlparse(src)
            if not o.scheme:
                src = constants.BLOG_URI_FORMAT.format(blog=self.blog_name) + src

            headers = self.get_headers(self.blog_name)
            with httpx.Client(http2=True, headers=headers) as c:
                r = c.get(src)
                r.raise_for_status()

                images = []
                soup = BeautifulSoup(r.text, "html.parser")
                a_tags = soup.find_all("a")
                for a_tag in a_tags:
                    img = a_tag.find("img")
                    if img:
                        href = a_tag.get("href")
                        src = img.get("src")
                        images.append(href or src)
                return images

        except httpx.HTTPStatusError:
            return []

    def __get_videos_from_iframe(self, src: str) -> str:
        try:
            o = urlparse(src)
            if not o.scheme:
                src = constants.BLOG_URI_FORMAT.format(blog=self.blog_name) + src

            headers = self.get_headers(self.blog_name)
            with httpx.Client(http2=True, headers=headers) as c:
                r = c.get(src)
                r.raise_for_status()

                soup = BeautifulSoup(r.text, "html.parser")
                source = soup.find("source")
                return source.get("src") if source else None

        except httpx.HTTPStatusError:
            pass

    def __is_from_reblog(self, tag: element.Tag) -> bool:
        result = tag.find_parent("div", constants.REBLOG_LIST_CLASS)
        return result is not None
