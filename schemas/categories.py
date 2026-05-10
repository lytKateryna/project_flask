from pydantic import Field

from schemas.base import BaseSchema


class CategoryBase(BaseSchema):
    id: int
    name: str = Field(..., min_length=1, max_length=50)


class CategoryCreateRequest(BaseSchema):
    name: str = Field(..., min_length=1, max_length=50)


class CategoryUpdateRequest(BaseSchema):
    name: str | None = Field(default=None, min_length=1, max_length=50)