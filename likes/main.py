from typing import Any

from pydantic.main import BaseModel
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from ok_core.client import OkClient
from ok_core.likes.models import OkAddLikeProviderEnum
from ok_core.selenium.main import default_selenium_login, launch_default_selenium_driver
import time


class OkAddLikeQuery(BaseModel):
    group_id: str
    item_id: str

class OkLikes:
    client: OkClient
    def __init__(
        self,
        client: OkClient
    ) -> None:
        self.client = client

    def get_group_link(
        self,
        query: OkAddLikeQuery
    ) -> str:
        default = self.client.default_ok_link
        g_id = query.group_id
        link = f"{default}/group/{g_id}"
        return link

    def selenium_like(
        self,
        query: OkAddLikeQuery
    ) -> Any:
        print('run selenium like')
        wd: WebDriver = launch_default_selenium_driver()
        # go the the ok login page
        wd.get(self.client.default_ok_link)
        # submit login form
        default_selenium_login(
            wd=wd,
            user=self.client.user
        )
        time.sleep(1)
        # go to group page
        group_link = self.get_group_link(query=query)
        wd.get(group_link)
        # find link element button
        # wd.get_screenshot_as_file('scr.png')
        like_el_attr = f"GROUP_HEADER:{query.item_id}:0"
        x_find = f"//*[@data-like-reference-id='{like_el_attr}']"
        like_el: WebElement = wd.find_element(
            by=By.XPATH,
            value=x_find
        )
        # print('like el is ', like_el)
        like_el.click()
        wd.close()

    def add(
        self,
        query: OkAddLikeQuery,
        provider: OkAddLikeProviderEnum = OkAddLikeProviderEnum.selenium
    ) -> Any:
        if provider == OkAddLikeProviderEnum.selenium:
            self.selenium_like(query=query)
