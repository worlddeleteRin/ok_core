from typing import Union
from ok_core.client import OkClient


class OkGroup:
    client: OkClient
    def __init__(
        self,
        client: OkClient
    ):
        self.client = client

    @staticmethod
    def parseGroupTopicIdsFromUrl(
        url: str
    ) -> tuple[str, str] | None:
        if 'group' in url:
            # supposed url to be like
            # https://ok.ru/group/61638264422477/topic/154623547495757
            try:
                g = url.split('group/')[1].split('/')[0]
                t = url.split('topic/')[1]
            except:
                return None
            return (g,t)
        else:
            # supposed url to be like
            # https://ok.ru/kinofan.movies/topic/154853050242381
            try:
                g = url.split('ok.ru/')[1].split('/')[0]
                t = url.split('topic/')[1]
                pass
            except:
                return None
            return (g,t)
