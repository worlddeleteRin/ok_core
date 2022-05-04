from typing import Optional
from pydantic.main import BaseModel
import requests
from ok_core.client import OkClient

from ok_core.user.models import AuthorizeRequestFormData, AuthorizeRequestQuery

class OkUser(BaseModel):
    client: OkClient
    username: str = ""
    password: str = ""
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    expires_in: Optional[int] = None

    class Config:
        arbitrary_types_allowed = True

    def oauth_get_grant_link(self):
        pass

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
