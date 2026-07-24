from pydantic import BaseModel
from sqlalchemy import Integer, String, ForeignKey, Float, Date
from sqlalchemy.orm import Mapped, mapped_column

from datetime import date


class Orders(BaseModel):
    __talename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )
    status: Mapped[str] = mapped_column(String, nullable=False)
    total_amount: Mapped[float] = mapped_column(Float, nullable=False)
    discount_code: Mapped[str] = mapped_column(String, nullable=True, default=None)
    created_at: Mapped[Date] = mapped_column(Date, default=date.today)
    updated_at: Mapped[Date] = mapped_column(Date, default=date.today)

    