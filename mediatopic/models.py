from pydantic.main import BaseModel

class FieldSets(BaseModel):
    achievement: str = "ID" 

class OkMediatopic(BaseModel):
    ref: str
    is_product: bool
    on_moderation: bool
