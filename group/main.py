from typing import Union

from pydantic.main import BaseModel
from ok_core.client import OkClient
from httpx import Client as HttpClient

from ok_core.models import BaseOkProviderEnum
from ok_core.logging import lgd,lgw,lge
from ok_core.user.main import OkUser

class GetGroupPostIdsQuery(BaseModel):
    last_n_posts: int = 6


class OkGroup:
    id: str
    client: OkClient
    def __init__(
        self,
        id: str,
        client: OkClient
    ):
        self.id = id
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

    def http(self) -> HttpClient:
        return self.client.http.client

    def check_group_exist(self) -> bool:
        # TODO implement logic to check if group exist (by api perfectly)
        return True

    def selenium_get_group_post_ids(
        self,
        query: GetGroupPostIdsQuery,
    ) -> list[str]:
        # TODO implement
        return []

    def get_group_post_ids(
        self,
        user: OkUser, 
        query: GetGroupPostIdsQuery,
        provider: BaseOkProviderEnum = BaseOkProviderEnum.selenium
    ) -> list[str]:
        lgd(f"** Run get group post ids, provider: {provider} **")
        exist = self.check_group_exist()
        if not exist:
            msg = f"cant get {self.id} group"
            lge(msg)
            raise Exception(msg)
        if provider == BaseOkProviderEnum.selenium:
            self.selenium_get_group_post_ids(query=query)
        else:
            lge(f"Provider is not implemented: {provider}")
        return []
