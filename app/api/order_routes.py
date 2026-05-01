from fastapi import APIRouter, HTTPException
from app.models.order import Order
from app.services.order_service import (
    create_order,
    get_all_orders,
    cancel_order
)
from fastapi import HTTPException

router = APIRouter()


@router.post("/orders")
def create_new_order(order: Order):
    try:
        return create_order(order)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/orders")
def list_orders():
    return get_all_orders()


@router.delete("/orders/{order_id}")
def delete_order(order_id: int):
    try:
        return cancel_order(order_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))