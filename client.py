import requests
import json
import time

from httpx import Client, Response

from user.main import OkUser

from .models import *

class HttpModule():
    is_debug: bool = True
    client: Client 

    def __init__(
        self,
        client: Client
    ):
        self.client = client

    def process_response (
        self,
        response: Response
    ) -> BaseOkResponse:
        response_dict = dict(response.json())
        if response.status_code != 200:
            response_error = response_dict.get('error')
            if isinstance(response_error, dict):
                error = BaseOkErrorException(
                    response = response,
                    **response_error 
                )
            else:
                error = BaseOkErrorException.get_dummy_from_response(
                    response
                )
            raise error
        response_success = response_dict.get('response')
        if not response_success:
            raise BaseOkErrorException.get_dummy_from_response(
                response
            )
        return BaseOkResponse(
            response = response_success
        )

class OkClient():
    http: HttpModule
    access_token: str
    api_v: str
    api_url: str
    app_id: int
    user: OkUser

    def __init__(self,
            access_token: str = "",
            api_v: str = '',
            api_url: str = '',
            app_id: int = 0,
            user: OkUser = OkUser()
        ):
        self.api_v = api_v
        self.api_url = api_url
        self.access_token = access_token
        # init httpx Client
        self.http = HttpModule(
            client = Client(
                base_url = self.api_url,
                params = {
                    'access_token': self.access_token,
                    'v': self.api_v
                }
            )
        )

    """
    def request_token_url(self, app_id=7709111):
        return f'https://oauth.vk.com/authorize?client_id={app_id}&redirect_uri=https://oauth.vk.com/blank.html&display=popup&scope=notify+friends+photos+status+wall+offline+groups+stats+email+market&response_type=token&revoke=1'
    """
