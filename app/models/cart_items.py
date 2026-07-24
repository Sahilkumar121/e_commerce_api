from pydantic import BaseModel
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, ForeignKey


class CartItems(BaseModel):
    __tablename__ = "cartItems"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey("products.id"))
    quantity: Mapped[int] = mapped_column(Integer)
