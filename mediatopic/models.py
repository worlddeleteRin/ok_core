from pydantic.main import BaseModel

class FieldSets(BaseModel):
    achievement: str = "ID" 

class OkMediatopicModel(BaseModel):
    ref: str
    is_product: bool
    on_moderation: bool
