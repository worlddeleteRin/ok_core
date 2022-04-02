from typing import Union
from ok_core.client import OkClient


class OkGroup:
    client: OkClient
    def __init__(
        self,
        client: OkClient
    ):
        self.client = client

    def parseGroupTopicIdsFromUrl(
        self,
        url: str
    ) -> tuple[str, str] | None:
        # https://ok.ru/group/61638264422477/topic/154623547495757
        try:
            g = url.split('group/')[1].split('/')[0]
            t = url.split('topic/')[1]
        except:
            return None
        return (g,t)
