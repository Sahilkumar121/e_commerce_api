from pydantic import BaseModel, Field


class CartItemCreate(BaseModel):
    product_id: int = Field(default=..., gt=0)
    quantity: int = Field(default=...)


class CartItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int

    class Config:
        from_attribute = True


class CartItemUpdate(BaseModel):
    quantity: int = Field(
        default=..., gt=0, description="Quantity can't be 0 or negative"
    )
