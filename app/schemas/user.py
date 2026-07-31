from datetime import date

from pydantic import BaseModel, EmailStr, Field, field_validator


class UserRegisterRequest(BaseModel):
    email: EmailStr = Field(..., examples=["youremail@gmail.com"])
    password: str = Field(..., description="A unique password")
    role: str = Field(default="customer", examples=["admin", "customer", "manager"])
    created_at: date = Field(default_factory=date.today)

    @field_validator("email")
    @classmethod
    def check_email(cls, value):
        domain_name = value.split("@")[-1]

        if domain_name not in ["gmail.com", "vitbhopal.ac.in"]:
            raise ValueError("Invalid email")
        return value


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    role: str
    created_at: date


class CurrentUserResponse(BaseModel):
    id: int
    email: str
    role: str
