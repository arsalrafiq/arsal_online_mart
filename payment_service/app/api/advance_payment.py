from fastapi import APIRouter, HTTPException
from app.models import AdvancePaymentCreate, AdvancePaymentRead
from app.db import get_session
from sqlmodel import Session, select

advance_payment_router = APIRouter()

@advance_payment_router.post("/", response_model=AdvancePaymentRead)
async def create_advance_payment(advance_payment: AdvancePaymentCreate):
    with get_session() as session:
        db_advance_payment = advance_payment.from_orm(advance_payment)
        session.add(db_advance_payment)
        session.commit()
        session.refresh(db_advance_payment)
        return db_advance_payment

@advance_payment_router.get("/{advance_payment_id}", response_model=AdvancePaymentRead)
async def get_advance_payment(advance_payment_id: int):
    with get_session() as session:
        statement = select(advance_payment).where(advance_payment.advance_payment_id == advance_payment_id)
        result = session.exec(statement)
        advance_payment = result.one_or_none()
        if not advance_payment:
            raise HTTPException(status_code=404, detail="Advance Payment not found")
        return advance_payment