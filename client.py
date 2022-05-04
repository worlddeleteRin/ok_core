import requests
import json
import time
import hashlib

from httpx import Client, Response, Request

# from ok_core.user.main import OkUser

from ok_core.models import *
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

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
        # response_success = response_dict.get('response')
        if ( 
            'error' in response_dict or
            'error_code' in response_dict
        ):
            raise BaseOkErrorException.get_dummy_from_response(
                response
            )
        return BaseOkResponse(
            response = response 
        )

class OkClient:
    logger: logging.Logger
    http: HttpModule
    access_token: str
    session_key: str
    session_secret_key: str
    app_secret_key: str
    app_key: str
    api_v: str
    api_url: str
    app_id: int
    default_ok_link: str
    # user: OkUser

    def __init__(self,
            session_key: str = "tkn1cmoueDna4uM4gbDlpu1QpMd6l4N3KQt80CTKGlAjqCLckuzvuuusHPcGjhDDX532W9",
            session_secret_key: str = "06d5b9a9c78c73958bde41b6c4ace479",
            access_token: str = "tkn18Qs1LhTaCG0Dh5jtzKuZI9WJ6mXQs5A15NjNvWypqXveqGh9jxXjCBnywZ6ytmk39",
            app_key: str = "CIJBIKKGDIHBABABA",
            app_secret_key: str = "13C891E288B067881DFAF163",
            # access_token: str = "",
            api_v: str = '',
            api_url: str = 'https://api.ok.ru/api',
            app_id: int = 512001409175,
            default_ok_link: str = 'https://ok.ru',
            # user: OkUser = OkUser()
        ):
        global logger
        # logger.warning(f'user init is {user.dict()}')
        self.app_id = app_id
        self.api_v = api_v
        self.api_url = api_url
        self.default_ok_link = default_ok_link
        self.access_token = access_token
        self.session_key = session_key
        self.session_secret_key = session_secret_key
        self.app_key = app_key
        self.app_secret_key = app_secret_key
        self.logger = logger
        # init httpx Client
        # self.user = user
        self.http = HttpModule(
            client = Client(
                base_url = self.api_url,
                params = {
                    'access_token': self.access_token,
                    'application_key': self.app_key,
                    # 'session_secret_key': self.session_secret_key
                    # 'v': self.api_v
                }
            )
        )

    def get_session_secret_key(self) -> str:
        """
        # MD5(access_token + application_secret_key)
        at = self.access_token
        ask = self.app_secret_key
        """
        # return self.session_secret_key
        at = self.access_token
        ask = self.app_secret_key
        res = f'{at + ask}'
        logger.warning(f'session sk: {res}')
        hashed = hashlib.md5(res.encode()).hexdigest()
        return hashed.lower()

    def get_sig(self, params: dict) -> str:
        default_params = {
            'application_key': self.app_key,
        }
        params = {**params, **default_params}
        params = dict(sorted(params.items()))
        logger.warning(f'params are {params}')
        sk = self.get_session_secret_key()
        if 'session_key' in params:
            del params['session_key']
        if 'access_token' in params:
            del params['access_token']
        params_str = ""
        for (k,v) in params.items():
            params_str += f"{k}={v}"
        res = f'{params_str}{sk}'
        logger.warning(f'str to hash {res}')
        hashed = hashlib.md5(res.encode()).hexdigest()
        return hashed.lower()

    def oauth_get_grant_link(self) -> str:
        grants = [
            "VALUABLE_ACCESS", "LONG_ACCESS_TOKEN", "PHOTO_CONTENT",
            "GROUP_CONTENT", "VIDEO_CONTENT", "APP_INVITE",  "GET_EMAIL"
        ]
        params = {
            "client_id": self.app_id,
            "scope": ";".join(grants), 
            "response_type": "code",
            "redirect_uri": "https://fast-code.ru",
        }
        client = Client()
        request: Request = client.build_request(
            url="https://connect.ok.ru/oauth/authorize",
            method="get",
            params=params,
        )
        return str(request.url)
        

    """
    def request_token_url(self, app_id=7709111):
        return f'https://oauth.vk.com/authorize?client_id={app_id}&redirect_uri=https://oauth.vk.com/blank.html&display=popup&scope=notify+friends+photos+status+wall+offline+groups+stats+email+market&response_type=token&revoke=1'
    """
    """
    https://connect.ok.ru/oauth/authorize?client_id=512001409175&scope=VALUABLE_ACCESS;LONG_ACCESS_TOKEN;PHOTO_CONTENT;GROUP_CONTENT;VIDEO_CONTENT;APP_INVITE;GET_EMAIL&response_type=token&redirect_uri=socials.fast-code.ru&layout=w
    """
    """
    https://fast-code.ru/
    #access_token=tkn1kqp4QSJ3TYfYHTQ7FwgctoNQtZupUcgNUEmEjZZFuIWy0vfRCnYRzbVQj6I6G17in
    session_secret_key=edd0be174a92f156f7c160a88da57370
    permissions_granted=PHOTO_CONTENT%3BVALUABLE_ACCESS%3BGROUP_CONTENT%3BLONG_ACCESS_TOKEN
    expires_in=2592000
    """
