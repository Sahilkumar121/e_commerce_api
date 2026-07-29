from enum import Enum

from pydantic import BaseModel, Field, field_validator


class OrderStatus(str, Enum):
    CREATED = "Created"
    PICKED = "Picked"
    SHIPPED = "Shipped"
    DELIVERED = "Delivered"


class CreateOrderItem(BaseModel):
    product_id: int = Field(gt=0)
    quantity: int = Field(gt=0, description="Cannnot order 0 or negative order")


class CreateOrderRequest(BaseModel):
    status: OrderStatus = Field(default=OrderStatus.CREATED)
    discount_code: str | None = Field(default=None)

    item: list[CreateOrderItem] = Field(
        min_length=1, description="Order must have atleast one item"
    )

    @field_validator("discount_code")
    @classmethod
    def check_status(cls, value):
        if value:
            return value.upper()

        return value
