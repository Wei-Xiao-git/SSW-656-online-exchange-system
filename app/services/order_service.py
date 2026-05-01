from app.database.database import SessionLocal
from app.database.order_model import OrderDB
from app.database.user_model import UserDB
from app.database.listing_model import ListingDB


def create_order(order, buyer_id: int):
    db = SessionLocal()

    buyer = db.query(UserDB).filter(
        UserDB.id == buyer_id
    ).first()

    if not buyer:
        db.close()
        raise ValueError("Buyer not found")

    listing = db.query(ListingDB).filter(
        ListingDB.id == order.listing_id
    ).first()

    if not listing:
        db.close()
        raise ValueError("Listing not found")

    new_order = OrderDB(
        buyer_id=buyer_id,
        listing_id=order.listing_id,
        quantity=order.quantity,
        status=order.status
    )

    db.add(new_order)
    db.commit()
    db.close()

    return {"message": "Order created successfully"}


def get_all_orders():
    db = SessionLocal()
    orders = db.query(OrderDB).all()
    db.close()
    return orders


def cancel_order(order_id: int):
    db = SessionLocal()

    order = db.query(OrderDB).filter(
        OrderDB.id == order_id
    ).first()

    if not order:
        db.close()
        raise ValueError("Order not found")

    db.delete(order)
    db.commit()
    db.close()

    return {"message": "Order cancelled successfully"}