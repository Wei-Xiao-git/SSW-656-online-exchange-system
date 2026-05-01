from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database.database import Base


class ListingDB(Base):
    __tablename__ = "listings"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Float, nullable=False)

    seller_id = Column(Integer, ForeignKey("users.id"))

    seller = relationship("UserDB", back_populates="listings")
    orders = relationship("OrderDB", back_populates="listing")