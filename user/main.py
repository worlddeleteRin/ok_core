from typing import Optional
from pydantic.main import BaseModel
import requests
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from ok_core.client import OkClient
from ok_core.selenium.main import launch_default_selenium_driver

from ok_core.user.models import AuthorizeRequestFormData, AuthorizeRequestQuery, GetAccessTokenResponse
import time
from urllib.parse import urlparse
from urllib.parse import parse_qs 
from httpx import Client, Response

class OkUser(BaseModel):
    client: OkClient
    username: str = ""
    password: str = ""
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    expires_in: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True

    def check_can_authorize_web_dirty(
        self
    ) -> bool:
        request_url = "https://ok.ru/dk"
        session = requests.Session()

        headers = {
            'content-type': 'application/x-www-form-urlencoded',
        }

        form_data = AuthorizeRequestFormData(**{
            "st.email": self.username,
            "st.password": self.password
        })
        query = AuthorizeRequestQuery()

        r: requests.Response = session.post(
            url=request_url,
            headers=headers,
            params=query.dict(by_alias=True),
            data=form_data.dict(by_alias=True),
            # cookies=cookies
        )
        print('resp status', r.status_code)
        print(session.cookies.get_dict())
        if r.status_code != 200:
            return False
        auth_code = session.cookies.get_dict().get("AUTHCODE")
        if not auth_code:
            return False
        return True

    def default_selenium_login(
        self,
        wd: WebDriver,
    ):
        # target elements
        email_input: WebElement = wd.find_element_by_id("field_email")
        password_input: WebElement = wd.find_element_by_id("field_password")
        login_button: WebElement = wd.find_element_by_class_name("button-pro.__wide")
        # clear inputs
        email_input.clear()
        password_input.clear()

        email_input.send_keys(self.username)
        password_input.send_keys(self.password)

        login_button.click()

    def get_access_token_from_code(self, code: str) -> GetAccessTokenResponse | None:
        logd = self.client.logger.debug
        logw = self.client.logger.warning
        url = "https://api.ok.ru/oauth/token.do"
        params = self.client.oauth_get_access_token_params(code=code)
        http = Client()
        resp: Response = http.post(
            url=url,
            data=params
        )
        try:
            tData = GetAccessTokenResponse(**resp.json())
            return tData
        except Exception as e:
            logw(f"Exception when request access token {e}")
            logw(f"response was {resp.content}")
            return None

    def selenium_get_access_token(self, silent: bool = True):
        logd = self.client.logger.debug
        logw = self.client.logger.warning
        logd(f'start get selenium access_token')
        grant_link = self.client.oauth_get_grant_link()
        logd(f'grant link is {grant_link}')
        wd: WebDriver = launch_default_selenium_driver(
            headless=silent
        )

        wd.get(self.client.default_ok_link)
        self.default_selenium_login(wd)
        time.sleep(1)
        wd.get(grant_link)
        # target elements
        button_allow: WebElement = wd.find_element_by_class_name("form-actions_yes")
        # click on allow button
        button_allow.click()
        time.sleep(1)
        # assume that we are redirected
        parsed_red_url = urlparse(wd.current_url)
        q = parse_qs(parsed_red_url.query)
        if not 'code' in q:
            logw(f'no code in redirected url! query is {q}')
        code = q['code'][0]
        logd(f'code is {code}')
        tData = self.get_access_token_from_code(code)
        wd.close()
        return tData
        # time.sleep(1999)

        # https://fast-code.ru/?code=1Q36aASAQElrcYdqfBL95SuZ0CQAF2fNODvYUKeVlLGrP2o8ZWsNFEcj6omalAGhiE41Shjgj74kLeraPcj9Yc0hzGTD412sIHsTeGpKyeP6Crf8vMzmikzkM73wVWhiOdXgvLsbYGLSO4ce3jMcbcTJguKgnypmzAqZtwvL52WuL1&permissions_granted=PHOTO_CONTENT%3BVALUABLE_ACCESS%3BGROUP_CONTENT%3BLONG_ACCESS_TOKEN
