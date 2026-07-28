from datetime import date
from typing import Annotated

from pydantic import BaseModel, Field


class CreateOrder(BaseModel):
    user_id: Annotated[int, Field(default=..., gt=0)]
    status: Annotated[bool, Field(default=True)]
    total_amount: Annotated[float, Field(default=...)]
    discount_code: Annotated[str | None, Field(default=None)]
    created_at: Annotated[date, Field(default=date.today)]
    updated_at: Annotated[date, Field(default=date.today)]
