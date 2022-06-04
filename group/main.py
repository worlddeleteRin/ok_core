from typing import Union, List
import time

from pydantic.main import BaseModel
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from ok_core.client import OkClient
from httpx import Client as HttpClient

from ok_core.models import BaseOkProviderEnum
from ok_core.logging import lgd,lgw,lge
from ok_core.selenium.main import launch_default_selenium_driver
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

    def get_group_link(self) -> str:
        default = self.client.default_ok_link
        link = f"{default}/group/{self.id}"
        return link

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
        if self.id == "":
            return False
        return True

    def selenium_get_group_post_ids(
        self,
        query: GetGroupPostIdsQuery,
        user: OkUser,
        is_testing: bool = False
    ) -> list[str]:
        post_ids: list[str] = []
        wd: WebDriver = launch_default_selenium_driver(headless=not is_testing)
        # go the the ok login page
        wd.get(self.client.default_ok_link)
        # submit login form
        user.default_selenium_login(wd=wd)
        time.sleep(1)
        # go to group page
        group_link = self.get_group_link()
        wd.get(group_link)
        post_list_el: List[WebElement] = wd.find_elements_by_class_name('feed-w')
        lgd(f'Found {len(post_list_el)} posts')
        if len(post_list_el) == 0:
            lge('Method works incorrectly, cant found posts | Or no posts in group')
        for el in post_list_el:
            like_el = el.find_element_by_class_name('controls-list_lk')
            post_id_dirty: str = like_el.get_attribute('data-like-reference-id')
            try:
                post_id = post_id_dirty.split(':')[-2]
                post_ids.append(post_id)
            except Exception:
                msg = f'cant get post id from {post_id_dirty}'
                lge(msg)
        wd.close()
        return post_ids[:query.last_n_posts]

    def get_group_post_ids(
        self,
        user: OkUser, 
        query: GetGroupPostIdsQuery,
        provider: BaseOkProviderEnum = BaseOkProviderEnum.selenium,
        is_testing: bool = False
    ) -> list[str]:
        post_ids: list[str] = []
        lgd(f"** Run get group post ids, provider: {provider} **")
        exist = self.check_group_exist()
        if not exist:
            msg = f"cant get {self.id} group. Mb wrong id"
            lge(msg)
            raise Exception(msg)
        if provider == BaseOkProviderEnum.selenium:
            post_ids = self.selenium_get_group_post_ids(
                query=query,
                user=user,
                is_testing=is_testing
            )
        else:
            lge(f"Provider is not implemented: {provider}")
        return post_ids
