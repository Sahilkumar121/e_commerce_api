from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base
from app.models.orders import Orders


class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # Foreign Key linking back to the order
    order_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("orders.id"), nullable=False
    )

    # Foreign Key linking to your products table
    product_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("products.id"), nullable=False
    )

    quantity: Mapped[int] = mapped_column(Integer, nullable=False)

    # Always store the price at the time of purchase!
    # If the product price goes up next year, this order's history stays accurate.
    unit_price: Mapped[float] = mapped_column(nullable=False)

    # Relationship linking back to the Order
    order: Mapped[Orders] = relationship(back_populates="items")
