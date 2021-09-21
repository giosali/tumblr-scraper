from typing import Dict

from . import constants


class HttpMixin:
    def get_headers(self, blog_name: str) -> Dict:
        headers = {
            "accept": constants.ACCEPT,
            "user-agent": constants.USER_AGENT,
            "referer": constants.REFERER_FORMAT.format(blog=blog_name),
        }
        return headers
