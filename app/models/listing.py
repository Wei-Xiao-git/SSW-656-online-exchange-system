from pydantic import BaseModel


class Listing(BaseModel):
    title: str
    description: str
    price: float
    seller: str