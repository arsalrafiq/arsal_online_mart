# from fastapi import APIRouter, Depends, HTTPException, Session
# from app.db import DB_SESSION
# from app.service import (
#     handle_booking_payment, 
#     handle_ready_made_payment, 
#     handle_remaining_payment, 
#     read_payment_details
# )
# from app.models import Order, Payment, PaymentForm, RemainingPaymentModel
# from app.kafka_producer import produce_kafka_message

# router = APIRouter()

# @router.post("/payment/")
# async def process_payment(payment_details: PaymentForm, session: Session = DB_SESSION):
#     order = session.query(Order).filter(Order.order_id == payment_details.order_id).first()
#     if not order:
#         raise HTTPException(status_code=404, detail="Order not found")

#     if order.order_type.lower() == "booking":
#         handle_booking_payment(payment_details, order, session)
#     elif order.order_type.lower() == "ready_made":
#         handle_ready_made_payment(payment_details, order, session)
#     else:
#         raise HTTPException(status_code=400, detail="Invalid order type")
    
#     await produce_kafka_message("payment_topic", f"Payment processed for order {order.order_id}")
#     return {"message": "Payment processed successfully"}

# @router.post("/remaining-payment/")
# async def process_remaining_payment(remaining_amount_details: RemainingPaymentModel, session: Session = DB_SESSION):
#     payment_details = session.query(Payment).filter(Payment.payment_id == remaining_amount_details.payment_id).first()
#     if not payment_details:
#         raise HTTPException(status_code=404, detail="Payment not found")

#     payment = handle_remaining_payment(remaining_amount_details, payment_details, session)
#     await produce_kafka_message("remaining_payment_topic", f"Remaining payment processed for order {payment.order_id}")
#     return {"message": "Remaining payment processed successfully"}

# @router.get("/payment/{order_id}")
# def get_payment_details(order_id: int, session: Session = DB_SESSION):
#     payment = read_payment_details(order_id, session)
#     return payment


from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.db import get_session
from app.service import (
    handle_booking_payment, 
    handle_ready_made_payment, 
    handle_remaining_payment, 
    read_payment_details
)
from app.models import Order, Payment, PaymentForm, RemainingPaymentModel
from app.kafka_producer import produce_kafka_message

router = APIRouter()

@router.post("/payment/")
async def process_payment(payment_details: PaymentForm, session: Session = Depends(get_session)):
    statement = select(Order).where(Order.order_id == payment_details.order_id)
    order = session.exec(statement).first()
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
    statement = select(Payment).where(Payment.payment_id == remaining_amount_details.payment_id)
    payment_details = session.exec(statement).first()
    if not payment_details:
        raise HTTPException(status_code=404, detail="Payment not found")

    payment = handle_remaining_payment(remaining_amount_details, payment_details, session)
    await produce_kafka_message("remaining_payment_topic", f"Remaining payment processed for order {payment.order_id}")
    return {"message": "Remaining payment processed successfully"}

@router.get("/payment/{order_id}")
def get_payment_details(order_id: int, session: Session = Depends(get_session)):
    payment = read_payment_details(order_id, session)
    return payment
