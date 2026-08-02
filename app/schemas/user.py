from datetime import date

from pydantic import BaseModel, EmailStr, Field, computed_field, field_validator


class UserRegisterRequest(BaseModel):
    first_name: str = Field(..., description="Name cannot be empty")
    last_name: str | None = Field(..., examples=["kumar", "yadav"])
    username: str = Field(default=..., examples=["sahilkumar121"])
    email: EmailStr = Field(..., examples=["youremail@gmail.com"])
    password: str = Field(..., description="A unique password")
    role: str = Field(default="customer", examples=["admin", "customer", "manager"])

    @field_validator("email")
    @classmethod
    def check_email(cls, value):
        domain_name = value.split("@")[-1]

        if domain_name not in ["gmail.com", "vitbhopal.ac.in"]:
            raise ValueError("Invalid email")
        return value

    @field_validator("first_name", "last_name")
    @classmethod
    def check_first_and_lat_name(cls, value):
        if value.strip().isalnum():
            raise ValueError("Enter a valid first and last name")
        return value.strip()

    @computed_field
    @property
    def generate_full_name(self) -> str:

        if self.last_name and self.last_name.strip():
            return f"{self.first_name.strip()} {self.last_name.strip()}"

        return self.first_name


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    role: str
    created_at: date


class CurrentUserResponse(BaseModel):
    id: int
    email: str
    role: str
