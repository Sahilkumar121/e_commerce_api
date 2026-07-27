from typing import Annotated

from pydantic import BaseModel, Field, computed_field, model_validator
from slugify import slugify


class CreateCategory(BaseModel):
    name: Annotated[str, Field(..., min_length=1)]

    slug: Annotated[str | None, Field(default=None)]

    @model_validator(mode="after")
    def generate_slug(self) -> CreateCategory:
        if not self.slug:
            self.slug = slugify(self.name)
        else:
            self.slug = slugify(self.slug)

        return self


class CategoryFieldQuery(BaseModel):
    page: Annotated[int, Field(default=1, gt=0)]
    limit: Annotated[int, Field(default=10, gt=0)]
    name: Annotated[str | None, Field(default=None)]
    slug: Annotated[str | None, Field(default=None)]

    @computed_field
    @property
    def cal_start(self) -> int:

        start = (self.page - 1) * self.limit

        return start

    @computed_field
    @property
    def cal_end(self) -> int:

        end = self.cal_start + self.limit

        return end


class CategoryResponse(BaseModel):
    id: int
    name: str
    slug: str
