from pydantic import BaseModel, field_validator
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, ForeignKey, Float, Boolean, Date
from datetime import date


class Products(BaseModel):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    categories_id: Mapped[int] = mapped_column(Integer, ForeignKey("categories.id"))
    name: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    price: Mapped[float] = mapped_column(Float)
    stock_quantity: Mapped[int] = mapped_column(Integer)
    image_url: Mapped[str] = mapped_column(String)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[Date] = mapped_column(Date, default=date.today)

    @field_validator("name", "description")
    @classmethod
    def check_name_description(cls, value):
        if value.isalnum():
            raise ValueError("Not a Valid string")

        return value.lower()

    @field_validator("price", "stock_quantity")
    @classmethod
    def check_price_stock_quantity(cls, value) -> int:
        if value < 0:
            raise ValueError("Not a valid value")

        return value

    @field_validator("is_active")
    @classmethod
    def check_active_status(cls, value):
        if value not in [False, True]:
            raise ValueError("Not a valid input")

        return value
