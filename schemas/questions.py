from datetime import datetime

from pydantic import Field, model_validator

from schemas.base import BaseSchema
from schemas.categories import CategoryBase


class QuestionBase(BaseSchema):
    title: str = Field(..., min_length=15, max_length=150)
    description: str | None = Field(default=None, min_length=20, max_length=750)
    start_date: datetime
    end_date: datetime

    @model_validator(mode="after")
    def validate_dates(self):
        if self.start_date > self.end_date:
            raise ValueError("start_date must be before end_date")
        return self


class QuestionCreateRequest(QuestionBase):
    category_id: int


class QuestionUpdateRequest(BaseSchema):
    title: str | None = Field(default=None, min_length=15, max_length=150)
    description: str | None = Field(default=None, min_length=20, max_length=750)
    start_date: datetime | None = None
    end_date: datetime | None = None
    is_active: bool | None = None
    category_id: int | None = None

    @model_validator(mode="after")
    def validate_dates(self):
        if self.start_date is not None and self.end_date is not None:
            if self.start_date > self.end_date:
                raise ValueError("start_date must be before end_date")
        return self


class QuestionRetrieve(BaseSchema):
    id: int
    is_active: bool
    title: str
    description: str | None
    start_date: datetime
    end_date: datetime
    category: CategoryBase


class QuestionList(BaseSchema):
    id: int
    title: str
    start_date: datetime
    is_active: bool
    category: CategoryBase


class QuestionCreateResponse(QuestionRetrieve):
    ...
