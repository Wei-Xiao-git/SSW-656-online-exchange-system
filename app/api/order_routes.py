from fastapi import APIRouter, HTTPException
from app.models.order import Order
from app.services.order_service import (
    create_order,
    get_all_orders,
    cancel_order
)

router = APIRouter()


@router.post("/orders")
def create_new_order(order: Order):
    return create_order(order)


@router.get("/orders")
def list_orders():
    return get_all_orders()


@router.delete("/orders/{order_id}")
def delete_order(order_id: int):
    try:
        return cancel_order(order_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))