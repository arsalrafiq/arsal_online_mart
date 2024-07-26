# import stripe
# from fastapi import HTTPException
# from sqlmodel import Session
# from app.models import Order, Payment, AdvancePayment, PaymentForm, RemainingPaymentModel
# from app.settings import settings

# stripe.api_key = settings.STRIPE_SECRET_KEY

# def handle_booking_payment(payment_details: PaymentForm, order: Order, session: Session):
#     advance_payment_details = payment_details.advance_payment
#     if not advance_payment_details or advance_payment_details.advance_payment_method_id.lower() == "cash on delivery":
#         raise HTTPException(status_code=400, detail="Cash on delivery is not allowed for booking orders.")

#     if order.advance_price != advance_payment_details.advance_price:
#         raise HTTPException(status_code=400, detail="Advance payment amount does not match the order's advance price.")

#     try:
#         payment_intent = stripe.PaymentIntent.create(
#             amount=int(advance_payment_details.advance_price * 100),
#             currency="usd",
#             payment_method=advance_payment_details.advance_payment_method_id,
#             confirmation_method="manual",
#             confirm=True
#         )

#         if payment_intent.status == "succeeded":
#             create_advance_payment(payment_intent, order, session)
#         elif payment_intent.status in ["processing", "canceled"]:
#             raise HTTPException(status_code=400, detail="Payment is processing or canceled.")
#         else:
#             raise HTTPException(status_code=400, detail="Payment failed.")
#     except stripe.StripeError as se:
#         raise HTTPException(status_code=500, detail=str(se))

# def handle_ready_made_payment(payment_details: PaymentForm, order: Order, session: Session):
#     if payment_details.advance_payment:
#         raise HTTPException(status_code=400, detail="Advance payment is not applicable for ready-made orders.")

#     if payment_details.payment_method and payment_details.payment_method.lower() == "cash on delivery":
#         create_cod_payment(payment_details, order, session)
#     else:
#         if not payment_details.payment_method_id or payment_details.total_price != order.total_price:
#             raise HTTPException(status_code=400, detail="Invalid payment method ID or total price mismatch.")
#         try:
#             payment_intent = stripe.PaymentIntent.create(
#                 amount=int(payment_details.total_price * 100),
#                 currency="usd",
#                 payment_method=payment_details.payment_method_id,
#                 confirmation_method="manual",
#                 confirm=True
#             )

#             if payment_intent.status == "succeeded":
#                 create_payment(payment_intent, order, session)
#             elif payment_intent.status in ["processing", "canceled"]:
#                 raise HTTPException(status_code=400, detail="Payment is processing or canceled.")
#             else:
#                 raise HTTPException(status_code=400, detail="Payment failed.")
#         except stripe.StripeError as se:
#             raise HTTPException(status_code=500, detail=str(se))

# def handle_remaining_payment(remaining_amount_details: RemainingPaymentModel, payment_details: Payment, session: Session):
#     if remaining_amount_details.payment_method_id.lower() == "cash on delivery":
#         payment_details.payment_method = remaining_amount_details.payment_method_id
#     else:
#         if not remaining_amount_details.payment_method_id or remaining_amount_details.remaining_balance != payment_details.remaining_balance:
#             raise HTTPException(status_code=400, detail="Invalid payment method ID or remaining balance mismatch.")
#         try:
#             payment_intent = stripe.PaymentIntent.create(
#                 amount=int(remaining_amount_details.remaining_balance * 100),
#                 payment_method=remaining_amount_details.payment_method_id,
#                 currency="usd",
#                 confirm=True,
#                 confirmation_method="manual"
#             )

#             if payment_intent.status == "succeeded":
#                 payment_details.payment_intent_id = payment_intent.id
#                 payment_details.payment_method = payment_intent.payment_method_types[0]
#                 payment_details.is_completed = True
#                 payment_details.remaining_balance -= payment_intent.amount
#             elif payment_intent.status in ["processing", "canceled"]:
#                 raise HTTPException(status_code=400, detail="Payment is processing or canceled.")
#             else:
#                 raise HTTPException(status_code=400, detail="Payment failed.")
#         except stripe.StripeError as se:
#             raise HTTPException(status_code=500, detail=str(se))

#     session.add(payment_details)
#     session.commit()
#     session.refresh(payment_details)
#     return payment_details

# def create_advance_payment(payment_intent, order, session: Session):
#     outstanding_balance = order.total_price - order.advance_price
#     advance_payment = AdvancePayment(
#         advance_payment_intent_id=payment_intent.id,
#         advance_payment_method=payment_intent.payment_method_types[0],
#         advance_price=order.advance_price,
#         advance_payment_status=payment_intent.status
#     )
#     session.add(advance_payment)
#     session.commit()
#     session.refresh(advance_payment)

#     payment = Payment(
#         is_completed=False,
#         order_id=order.order_id,
#         total_price=order.total_price,
#         remaining_balance=outstanding_balance,
#         payment_status="pending",
#         advance_payment_id=advance_payment.advance_payment_id
#     )
#     session.add(payment)
#     session.commit()
#     session.refresh(payment)

# def create_cod_payment(payment_details: PaymentForm, order: Order, session: Session):
#     payment = Payment(
#         is_completed=False,
#         order_id=order.order_id,
#         total_price=order.total_price,
#         payment_status="pending",
#         payment_method=payment_details.payment_method
#     )
#     session.add(payment)
#     session.commit()
#     session.refresh(payment)

# def create_payment(payment_intent, order, session: Session):
#     payment = Payment(
#         payment_intent_id=payment_intent.id,
#         is_completed=True,
#         order_id=order.order_id,
#         total_price=order.total_price,
#         payment_status=payment_intent.status,
#         payment_method=payment_intent.payment_method_types[0]
#     )
#     session.add(payment)
#     session.commit()
#     session.refresh(payment)

# def read_payment_details(order_id: int, session: Session) -> Payment:
#     payment = session.query(Payment).filter(Payment.order_id == order_id).first()
#     if not payment:
#         raise HTTPException(status_code=404, detail="Payment not found")
#     return payment

from app.models import Order, Payment, PaymentForm, RemainingPaymentModel
from sqlmodel import Session

def handle_booking_payment(payment_details: PaymentForm, order: Order, session: Session):
    payment = Payment(order_id=payment_details.order_id, amount=payment_details.amount)
    session.add(payment)
    session.commit()

def handle_ready_made_payment(payment_details: PaymentForm, order: Order, session: Session):
    payment = Payment(order_id=payment_details.order_id, amount=payment_details.amount)
    session.add(payment)
    session.commit()

def handle_remaining_payment(remaining_amount_details: RemainingPaymentModel, payment_details: Payment, session: Session):
    payment_details.amount += remaining_amount_details.remaining_amount
    session.add(payment_details)
    session.commit()

def read_payment_details(order_id: int, session: Session):
    payment = session.query(Payment).filter(Payment.order_id == order_id).first()
    return payment
