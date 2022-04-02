from typing import Any

from pydantic.main import BaseModel
from selenium.webdriver.chrome.webdriver import WebDriver
from client import OkClient
from likes.models import OkAddLikeProviderEnum
from selenium.main import default_selenium_login, launch_default_selenium_driver


class OkAddLikeQuery(BaseModel):
    item_id: int

class OkLikes:
    client: OkClient
    def __init__(
        self,
        client: OkClient
    ) -> None:
        self.client = client

    def selenium_like(
        self,
        query: OkAddLikeQuery
    ) -> Any:
        wd: WebDriver = launch_default_selenium_driver()
        default_selenium_login(wd=wd)
        print('run selenium like')

    def add(
        self,
        query: OkAddLikeQuery,
        provider: OkAddLikeProviderEnum = OkAddLikeProviderEnum.selenium
    ) -> Any:
        if provider == OkAddLikeProviderEnum.selenium:
            self.selenium_like(query=query)
