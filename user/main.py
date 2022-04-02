from pydantic.main import BaseModel
import requests

from ok_core.user.models import AuthorizeRequestFormData, AuthorizeRequestQuery

class OkUser(BaseModel):
    username: str = ""
    password: str = ""

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
        auth_code = session.get("AUTHCODE")
        if not auth_code:
            return False
        return True
