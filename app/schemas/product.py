from datetime import date
from typing import Annotated

from pydantic import BaseModel, Field, computed_field, field_validator


class CreateProducts(BaseModel):
    name: Annotated[
        str, Field(default=..., min_length=1, description="Name of product")
    ]
    category_id: int = Field(default=..., gt=0)
    description: Annotated[
        str,
        Field(
            default=...,
            min_length=1,
            max_length=20,
            description="Detail about the product",
        ),
    ]
    price: Annotated[float, Field(default=..., gt=0)]
    stock_quantity: Annotated[int, Field(default=..., gt=0)]
    image_url: Annotated[str, Field(default=..., min_length=1)]
    is_active: Annotated[bool, Field(default=True)]

    @field_validator("name")
    @classmethod
    def check_name(cls, value) -> str:
        if value.isalnum():
            raise ValueError("Invalid name")

        return value

    @field_validator("is_active")
    @classmethod
    def check_active_status(cls, value) -> bool:
        if value not in [True, False]:
            raise ValueError("Invalid active status")

        return value


class ProductFieldQuery(BaseModel):
    page: Annotated[int, Field(default=1, gt=0)]
    limit: Annotated[int, Field(default=10, gt=0)]
    name: Annotated[str | None, Field(default=None, min_length=1)]
    price: Annotated[int | None, Field(default=None, gt=0)]
    rating: Annotated[float | None, Field(default=None, ge=0, le=5)]
    stock_quantity: Annotated[int | None, Field(default=None, ge=0)]
    is_active: Annotated[bool | None, Field(default=None)]

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


class ProductResponse(BaseModel):
    id: int
    categories_id: int
    name: str
    description: str
    price: float
    stock_quantity: int
    image_url: str
    is_active: bool
    created_at: date
