from pydantic import BaseModel, field_validator
from sqlalchemy import Integer, String, Date
from sqlalchemy.orm import Mapped, mapped_column

from datetime import date


class Users(BaseModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    hashed_password: Mapped[str] = mapped_column(String)
    role: Mapped[str] = mapped_column(String)
    created_at: Mapped[Date] = mapped_column(default=date.today)

    @field_validator("email")
    @classmethod
    def check_email(cls, value):
        email_domain = value.split("@")[-1]

        if email_domain not in ["gamil.com", "vitbhopal.ac.in"]:
            raise ValueError("Not A Valid Email")

        return value

    @field_validator("role")
    @classmethod
    def check_role(cls, value):

        if value not in ["admin", "customer"]:
            raise ValueError("Invalid role ['admin', 'customer']")

        return value
