from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    status: Mapped[str] = mapped_column(String, default="PENDING")

    items: Mapped[TransactionItems] = relationship(
        "TransactionItems", back_populates="transaction"
    )


class TransactionItems(Base):
    __tablename__ = "transactionItems"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    transaction_id: Mapped[int] = mapped_column(Integer, ForeignKey("transactions.is"))
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey("products.id"))
    quantity: Mapped[int] = mapped_column(Integer)

    transaction: Mapped[Transaction] = relationship(
        "Transaction",
        back_populates="items",
    )
