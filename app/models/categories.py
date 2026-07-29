from sqlalchemy import Index, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base
from app.models.products import Products


class Categories(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    slug: Mapped[str | None] = mapped_column(String, default=None)

    __table_args__ = (
        UniqueConstraint("name", "slug", name="uq_name_slug"),
        Index("name_slug_index", "name", "slug"),
    )

    products: Mapped[list[Products]] = relationship(back_populates="category")
