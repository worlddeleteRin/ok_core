from typing import Any, Optional
from pydantic.main import BaseModel
from ok_core.client import OkClient
from httpx import Response
import logging

from ok_core.mediatopic.models import FieldSets, OkMediatopicModel
from ok_core.models import BaseModelParseException, BaseOkResponse


logger=logging.getLogger(__name__)

class GetMediatopicByIdsQuery(BaseModel):
    # ids of mediatopic sep by ,
    # method: str = "mediatopic.getByIds"
    topic_ids: str = ""
    media_limit: int = 1
    # fields: FieldSets = FieldSets()
    fields: str = "achievement.ID"
    features: Optional[str] = None

class OkMediatopicResponse(BaseModel):
    media_topics: list[OkMediatopicModel]


class OkMediatopic:
    client: OkClient
    def __init__(
        self,
        client: OkClient
    ):
        self.client = client

    def get_by_ids(
        self,
        query: GetMediatopicByIdsQuery
    ) -> OkMediatopicResponse:
        params = query.dict(exclude_none=True)
        sig = self.client.get_sig(params=params)
        logger.warning(f'sig is {sig}')
        params['sig'] = sig

        r: Response = self.client.http.client.get(
            url="mediatopic/getByIds",
            params=params
        )
        resp: Response = self.client.http.process_response(r).response
        # logger.warning(f'req is {r.request.url}')
        # logger.warning(f'resp is {resp.json()}')
        try:
            d = OkMediatopicResponse(**resp.json())
        except Exception as e:
            raise BaseModelParseException(
                message = f'{e}'
            )
        return d

