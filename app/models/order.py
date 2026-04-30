from pydantic import BaseModel


class Order(BaseModel):
    id: int
    buyer: str
    listing_title: str
    quantity: int
    status: str = "Pending"