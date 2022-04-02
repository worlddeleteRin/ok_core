from ok_core.client import OkClient


class OkGroup:
    client: OkClient
    def __init__(
        self,
        client: OkClient
    ):
        self.client = client
