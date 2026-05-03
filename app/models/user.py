from pydantic import BaseModel, EmailStr, Field


class User(BaseModel):
    username: str = Field(..., min_length=3, max_length=20)
    password: str = Field(..., min_length=6)
    email: EmailStr
    role: str = "buyer"