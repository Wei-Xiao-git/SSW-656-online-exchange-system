from pydantic import BaseModel, Field


class Order(BaseModel):
    listing_id: int
    quantity: int = Field(..., gt=0)
    status: str = "Pending"