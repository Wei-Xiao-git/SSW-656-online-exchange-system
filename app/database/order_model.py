from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database.database import Base


class OrderDB(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)

    buyer_id = Column(Integer, ForeignKey("users.id"))
    listing_id = Column(Integer, ForeignKey("listings.id"))

    quantity = Column(Integer, nullable=False)
    status = Column(String, default="Pending")

    buyer = relationship("UserDB", back_populates="orders")
    listing = relationship("ListingDB", back_populates="orders")