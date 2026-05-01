from pydantic import BaseModel, Field


class Listing(BaseModel):
    title: str = Field(..., min_length=3)
    description: str = Field(..., min_length=5)
    price: float = Field(..., gt=0)
    seller_id: int