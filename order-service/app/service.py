# from sqlmodel import select
# from sqlmodel.ext.asyncio.session import AsyncSession
# from app.models import Order, OrderItem, ShippingAddress
# from app.schemas import OrderCreate
# from datetime import datetime
# from uuid import UUID

# class OrderService:
#     @staticmethod
#     async def create_order(session: AsyncSession, order: OrderCreate):

        
#         # Create shipping address
#         shipping_address = ShippingAddress(
#             address=order.shipping_address.address,
#             city=order.shipping_address.city,
#             country=order.shipping_address.country,
#             postal_code=order.shipping_address.postal_code
#         )
        
#         # Create new order
#         new_order = Order(
#             user_id=order.user_id,  # Now directly using the string user_id
#             total_amount=order.order_amount,
#             status="PENDING",
#             created_at=datetime.utcnow(),
#             updated_at=datetime.utcnow(),
#             shipping_address=shipping_address
#         )
#         session.add(new_order)
#         await session.flush()  # This assigns an ID to new_order without committing

#         # Create order items
#         for item in order.items:
#             new_order_item = OrderItem(
#                 order_id=new_order.id,
#                 product_id=item.product_id,  # Now directly using the string product_id
#                 name=item.name,
#                 quantity=item.quantity,
#                 price=item.price
#             )
#             session.add(new_order_item)

#         await session.commit()
#         await session.refresh(new_order)

#         return new_order

#     @staticmethod
#     async def get_order(session: AsyncSession, order_id: UUID):
#         statement = select(Order).where(Order.id == order_id)
#         result = await session.execute(statement)
#         return result.scalar_one_or_none()

#     @staticmethod
#     async def get_user_orders(session: AsyncSession, user_id: str):
#         statement = select(Order).where(Order.user_id == user_id)
#         result = await session.execute(statement)
#         return result.scalars().all()



from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.models import Order, OrderItem, ShippingAddress
from app.schemas import OrderCreate
from datetime import datetime
from uuid import UUID


class OrderService:
    @staticmethod
    async def create_order(session: AsyncSession, order: OrderCreate):
        # Create new order
        new_order = Order(
            user_id=order.user_id,
            total_amount=order.total_amount,
            status="PENDING",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        session.add(new_order)
        await session.flush()  # This assigns an ID to new_order without committing

        # Create shipping address linked to the order
        shipping_address = ShippingAddress(
            address=order.shipping_address.address,
            city=order.shipping_address.city,
            country=order.shipping_address.country,
            postal_code=order.shipping_address.postal_code,
            order_id=new_order.id  # Link shipping address to the order
        )
        session.add(shipping_address)
        await session.flush()  # This assigns an ID to shipping_address without committing

        # Create order items
        for item in order.items:
            new_order_item = OrderItem(
                order_id=new_order.id,
                product_id=item.product_id,
                name=item.name,
                quantity=item.quantity,
                price=item.price
            )
            session.add(new_order_item)

        await session.commit()
        await session.refresh(new_order)

        return new_order

    @staticmethod
    async def get_order(session: AsyncSession, order_id: str):
        statement = select(Order).where(Order.id == order_id)
        result = await session.execute(statement)
        return result.scalar_one_or_none()

    @staticmethod
    async def get_user_orders(session: AsyncSession, user_id: str):
        statement = select(Order).where(Order.user_id == user_id)
        result = await session.execute(statement)
        return result.scalars().all()
   

