from app.database.database import fake_orders_db


def create_order(order):
    fake_orders_db.append(order)
    return {"message": "Order created successfully"}


def get_all_orders():
    return fake_orders_db


def cancel_order(order_id: int):
    for order in fake_orders_db:
        if order.id == order_id:
            fake_orders_db.remove(order)
            return {"message": "Order cancelled successfully"}

    raise ValueError("Order not found")