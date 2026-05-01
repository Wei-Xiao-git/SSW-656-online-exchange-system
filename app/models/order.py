from pydantic import BaseModel, Field


class Order(BaseModel):
    id: int
    buyer: str
    listing_title: str
    quantity: int = Field(..., gt=0)
    status: str = "Pending"