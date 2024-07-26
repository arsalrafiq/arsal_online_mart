# app/services/payment.py
from sqlmodel import Session
from app.models.payment import Payment
from app.schemas.payment import PaymentCreate
from app.services.stripe import create_payment_intent
from app.kafka.producer import produce_message

async def create_payment(db: Session, payment: PaymentCreate):
    # Create Stripe PaymentIntent
    stripe_intent = await create_payment_intent(int(payment.amount * 100))
    
    # Create payment record
    db_payment = Payment(
        order_id=payment.order_id,
        amount=payment.amount,
        payment_method=payment.payment_method,
        stripe_payment_intent_id=stripe_intent.id,
        status="pending"
    )
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)

    # Produce Kafka message
    await produce_message("payment_created", db_payment.dict())

    return db_payment