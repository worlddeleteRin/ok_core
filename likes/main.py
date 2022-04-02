from typing import Any

from pydantic.main import BaseModel
from client import OkClient
from likes.models import OkAddLikeProviderEnum


class OkAddLikeQuery(BaseModel):
    item_id: int

class OkLikes:
    client: OkClient
    def __init__(
        self,
        client: OkClient
    ) -> None:
        self.client = client

    def add(
        self,
        query: OkAddLikeQuery,
        provider: OkAddLikeProviderEnum = OkAddLikeProviderEnum.selenium
    ) -> Any:
        if provider == OkAddLikeProviderEnum.selenium:
            pass
