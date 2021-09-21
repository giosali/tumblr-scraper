import httpx

from . import constants
from .http import HttpMixin
from .pages import Page


class Blog(HttpMixin):
    def __init__(self, blog_name: str):
        self.blog_name: str = blog_name

        self.blog_uri: str = constants.BLOG_URI_FORMAT.format(blog=blog_name)
        self.current_page_number = 1

        self._page: Page = Page(self.__get_page(), blog_name)

    @property
    def page(self) -> Page:
        return self._page

    @page.setter
    def page(self, page_number: int):
        self.current_page_number = page_number
        self._page = Page(self.__get_page(page_number), self.blog_name)

    def go_to_next_page(self):
        current_page = self._page

        self.current_page_number += 1
        self._page = Page(self.__get_page(self.current_page_number), self.blog_name)
        if not self._page.has_posts():
            self._page = current_page
            raise IndexError("Max number of pages exceeded")

    def go_to_previous_page(self):
        if self.current_page_number - 1 < 1:
            raise IndexError("Page number cannot fall below 1")

        self.current_page_number -= 1
        self._page = Page(self.__get_page(self.current_page_number), self.blog_name)

    def get_name(self) -> str:
        return self.blog_name

    def __get_page(self, page_number: int = 1) -> bytes:
        try:
            blog_page = constants.BLOG_PAGE_FORMAT.format(page_number=page_number)
            page_uri = self.blog_uri + blog_page

            headers = self.get_headers(self.blog_name)
            with httpx.Client(http2=True, headers=headers) as c:
                r = c.get(page_uri)
                r.raise_for_status()
                return r.content

        except httpx.HTTPStatusError:
            return bytes("", encoding="utf-8")
