# from fastapi import APIRouter, Depends, HTTPException
# from sqlmodel import Session, select
# from app.db import get_session
# from app.service import (
#     handle_booking_payment, 
#     handle_ready_made_payment, 
#     handle_remaining_payment, 
#     read_payment_details
# )
# from app.models import Order, Payment, PaymentForm, RemainingPaymentModel

# router = APIRouter()

# @router.post("/payments")
# def create_payment(payment_details: PaymentForm, session: Session = Depends(get_session)):
#     order = session.query(Order).filter(Order.order_id == payment_details.order_id).first()
#     if not order:
#         raise HTTPException(status_code=404, detail="Order not found")

#     if order.order_type == "booking":
#         return handle_booking_payment(payment_details, order, session)
#     elif order.order_type == "ready_made":
#         return handle_ready_made_payment(payment_details, order, session)
#     else:
#         raise HTTPException(status_code=400, detail="Unknown order type")

# @router.post("/payments/remaining")
# def pay_remaining_balance(remaining_payment: RemainingPaymentModel, session: Session = Depends(get_session)):
#     payment = session.query(Payment).filter(Payment.order_id == remaining_payment.order_id).first()
#     if not payment:
#         raise HTTPException(status_code=404, detail="Payment not found")

#     return handle_remaining_payment(remaining_payment, payment, session)

# @router.get("/payments/{order_id}")
# def get_payment_details(order_id: int, session: Session = Depends(get_session)):
#     return read_payment_details(order_id, session)


from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.db import get_session
from app.service import (
    handle_booking_payment, 
    handle_ready_made_payment, 
    handle_remaining_payment, 
    read_payment_details
)
from app.models import Order, Payment, PaymentForm, RemainingPaymentModel
from app.kafka_producer import produce_kafka_message, produce_order_created_event

router = APIRouter()

@router.post("/payment/")
async def process_payment(payment_details: PaymentForm, session: Session = Depends(get_session)):
    order = session.query(Order).filter(Order.order_id == payment_details.order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if order.order_type.lower() == "booking":
        handle_booking_payment(payment_details, order, session)
    elif order.order_type.lower() == "ready_made":
        handle_ready_made_payment(payment_details, order, session)
    else:
        raise HTTPException(status_code=400, detail="Invalid order type")
    
    await produce_kafka_message("payment_topic", f"Payment processed for order {order.order_id}")
    return {"message": "Payment processed successfully"}

@router.post("/remaining-payment/")
async def process_remaining_payment(remaining_amount_details: RemainingPaymentModel, session: Session = Depends(get_session)):
    payment_details = session.query(Payment).filter(Payment.payment_id == remaining_amount_details.payment_id).first()
    if not payment_details:
        raise HTTPException(status_code=404, detail="Payment not found")

    payment = handle_remaining_payment(remaining_amount_details, payment_details, session)
    await produce_kafka_message("remaining_payment_topic", f"Remaining payment processed for order {payment.order_id}")
    return {"message": "Remaining payment processed successfully"}

@router.get("/payment/{order_id}")
def get_payment_details(order_id: int, session: Session = Depends(get_session)):
    payment = read_payment_details(order_id, session)
    return payment
@router.post("/order_created")
async def order_created(order_id: str):
    await produce_order_created_event(order_id)
    return {"message": "Order created event produced"}
