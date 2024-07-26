# # app/router.py
# from uuid import UUID
# from fastapi import APIRouter, Depends
# from sqlmodel.ext.asyncio.session import AsyncSession
# from app.db import get_session
# from app.service import OrderService
# from app.schemas import OrderCreate, OrderResponse
# from typing import List

# router = APIRouter(prefix="/orders", tags=["Orders"])

# @router.post("/", response_model=OrderResponse)
# async def create_order(order: OrderCreate, db: AsyncSession = Depends(get_session)):
#     return await OrderService.create_order(db, order)

# @router.get("/{order_id}", response_model=OrderResponse)
# async def get_order(order_id: UUID, db: AsyncSession = Depends(get_session)):
#     return await OrderService.get_order(db, order_id)

# @router.get("/user/{user_id}", response_model=List[OrderResponse])
# async def get_user_orders(user_id: str, db: AsyncSession = Depends(get_session)):
#     return await OrderService.get_user_orders(db, user_id)



from uuid import UUID
from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from app.db import get_session
from app.service import OrderService
from app.schemas import OrderCreate, OrderResponse
from typing import List

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/", response_model=OrderResponse)
async def create_order(order: OrderCreate, db: AsyncSession = Depends(get_session)):
    return await OrderService.create_order(db, order)

@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(order_id: UUID, db: AsyncSession = Depends(get_session)):
    return await OrderService.get_order(db, order_id)

@router.get("/user/{user_id}", response_model=List[OrderResponse])
async def get_user_orders(user_id: str, db: AsyncSession = Depends(get_session)):
    return await OrderService.get_user_orders(db, user_id)


