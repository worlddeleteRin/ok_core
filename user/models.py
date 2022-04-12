from pydantic.fields import Field
from pydantic.main import BaseModel

class AuthorizeRequestFormData(BaseModel):
    posted: str = Field(default="set", alias="st.posted")
    fJS: str = Field(default="on", alias="st.fJS")
    email: str = Field(alias="st.email")
    password: str = Field(alias="st.password")
    iscode: bool = Field(default=False, alias="st.iscode")

    class Config:
        allow_population_by_field_name = True

class AuthorizeRequestQuery(BaseModel):
    cmd: str = Field(default="AnonymLogin", alias="cmd")
    st_cmd: str = Field(default="anonymLogin", alias="st.cmd")

    class Config:
        allow_population_by_field_name = True
