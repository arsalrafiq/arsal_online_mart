# app/api/payment.py
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.db.session import get_session
from app.schemas.payment import PaymentCreate, PaymentResponse
from app.services.payment import create_payment

router = APIRouter()

@router.post("/payments/", response_model=PaymentResponse)
async def create_payment_endpoint(payment: PaymentCreate, db: Session = Depends(get_session)):
    try:
        new_payment = await create_payment(db, payment)
        return new_payment
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    