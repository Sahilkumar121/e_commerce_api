from typing import Annotated

from pydantic import BaseModel, Field, field_validator, model_validator
from slugify import slugify


class CategoryCreate(BaseModel):
    name: Annotated[str, Field(..., min_length=1)]

    slug: Annotated[str | None, Field(default=None)]

    @model_validator(mode="after")
    def generate_slug(self) -> CategoryCreate:
        if not self.slug:
            self.slug = slugify(self.name)
        else:
            self.slug = slugify(self.slug)

        return self


class CategoryFieldQuery(BaseModel):
    limit: Annotated[int, Field(default=10, gt=0)]
    name: Annotated[str | None, Field(default=None)]
    slug: Annotated[str | None, Field(default=None)]

    @field_validator("name", "slug")
    @classmethod
    def check_name_slug(cls, value):
        if value is not None and not value.strip():
            raise ValueError("Value cannot be empty or just whitespaces")

        return value


class CategoryResponse(BaseModel):
    id: int
    name: str
    slug: str
