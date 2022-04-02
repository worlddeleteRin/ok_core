from pydantic.main import BaseModel

class OkUser(BaseModel):
    username: str = ""
    password: str = ""

