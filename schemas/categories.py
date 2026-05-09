from pydantic import (
    BaseModel,
    Field,
    model_validator,
    ConfigDict
)
from schemas.base import BaseSchema



class CategoryBase(BaseSchema):
    id: int = Field()
    name: str = Field(...,min_length=15 ,max_length=50)

