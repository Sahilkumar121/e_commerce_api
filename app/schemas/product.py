from typing import Annotated

from pydantic import BaseModel, Field, computed_field


class ProductFieldQuery(BaseModel):
    page: Annotated[int, Field(default=1, gt=0)]
    limit: Annotated[int, Field(default=10, gt=0)]
    name: Annotated[str | None, Field(default=None, min_length=1)]
    price: Annotated[int | None, Field(default=None, gt=0)]
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
