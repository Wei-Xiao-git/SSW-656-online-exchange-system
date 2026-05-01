from pydantic import BaseModel, Field


class Order(BaseModel):
    buyer_id: int
    listing_id: int
    quantity: int = Field(..., gt=0)
    status: str = "Pending"