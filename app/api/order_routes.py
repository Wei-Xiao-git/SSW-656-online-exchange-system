from fastapi import APIRouter, HTTPException, Depends
from app.models.order import Order
from app.security.role_dependency import require_role
from app.services.order_service import (
    create_order,
    get_all_orders,
    cancel_order
)
from fastapi import HTTPException
from app.security.auth_dependency import get_current_user

router = APIRouter()


@router.post("/orders")
def create_new_order(
    order: Order,
    current_user=Depends(require_role("buyer", "admin"))
):
    try:
        return create_order(
            order,
            buyer_id=current_user["user_id"]
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/orders")
def list_orders():
    return get_all_orders()


@router.delete("/orders/{order_id}")
def delete_order(
    order_id: int,
    current_user=Depends(get_current_user)
):
    try:
        return cancel_order(order_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))