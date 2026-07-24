from datetime import date

from sqlalchemy import Date, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class Orders(Base):
    __talename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )
    status: Mapped[str] = mapped_column(String, nullable=False)
    total_amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    discount_code: Mapped[str] = mapped_column(String, default=None, nullable=True)
    created_at: Mapped[Date] = mapped_column(Date, default=date.today)
    updated_at: Mapped[Date] = mapped_column(Date, default=date.today)
