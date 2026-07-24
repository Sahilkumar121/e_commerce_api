from pydantic import BaseModel, field_validator
from sqlalchemy import INTEGER, String, Index
from sqlalchemy.orm import Mapped, mapped_column


class Categories(BaseModel):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(INTEGER, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    slug: Mapped[str] = mapped_column(String)

    __table_args__ = Index("name_slug_index", "name", "slug")

    @field_validator("name", "slug")
    @classmethod
    def check_name(cls, value):
        if value.isalnum():
            raise ValueError("Only string is allowed")

        return value.lower()
