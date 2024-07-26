# from fastapi import HTTPException
# from sqlmodel import Session, select
# from app.models.inventory_model import InventoryItem
# from app.db_engine import Session

# # Add a New Inventory Item to the Database
# def add_new_inventory_item(inventory_item_data: InventoryItem, session: Session):
#     print("Adding Inventory Item to Database")
    
#     session.add(inventory_item_data)
#     session.commit()
#     session.refresh(inventory_item_data)
#     return inventory_item_data

# # Get All Inventory Items from the Database
# def get_all_inventory_items(session: Session):
#     all_inventory_items = session.exec(select(InventoryItem)).all()
#     return all_inventory_items

# # Get an Inventory Item by ID
# def get_inventory_item_by_id(inventory_item_id: int, session: Session):
#     inventory_item = session.exec(select(InventoryItem).where(InventoryItem.id == inventory_item_id)).one_or_none()
#     if inventory_item is None:
#         raise HTTPException(status_code=404, detail="Inventory Item not found")
#     return inventory_item

# # Delete Inventory Item by ID
# def delete_inventory_item_by_id(inventory_item_id: int, session: Session):
#     # Step 1: Get the Inventory Item by ID
#     inventory_item = session.exec(select(InventoryItem).where(InventoryItem.id == inventory_item_id)).one_or_none()
#     if inventory_item is None:
#         raise HTTPException(status_code=404, detail="Inventory Item not found")
#     # Step 2: Delete the Inventory Item
#     session.delete(inventory_item)
#     session.commit()
#     return {"message": "Inventory Item Deleted Successfully"}
# def update_inventory_item_by_id(item_id: int, to_update_item_data: InventoryItem, session: Session) -> InventoryItem:
#     """Update a single inventory item by ID"""
#     item = session.get(InventoryItem, item_id)
#     if item is None:
#         raise HTTPException(status_code=404, detail="Item not found")
#     for var, value in vars(to_update_item_data).items():
#         setattr(item, var, value)
#     session.add(item)
#     session.commit()
#     return item
# from fastapi import HTTPException
# from sqlmodel import Session, select
# from app.models.inventory_model import InventoryItem
# from app.db_engine import Session as DbSession

# # Add a New Inventory Item to the Database
# def add_new_inventory_item(inventory_item_data: InventoryItem, session: DbSession) -> InventoryItem:
#     print("Adding Inventory Item to Database")
#     session.add(inventory_item_data)
#     session.commit()
#     session.refresh(inventory_item_data)
#     return {"message": "Inventory Item Created Successfully", "data": inventory_item_data}

# # Get All Inventory Items from the Database
# def get_all_inventory_items(session: DbSession):
#     all_inventory_items = session.exec(select(InventoryItem)).all()
#     return all_inventory_items

# # Get an Inventory Item by ID
# def get_inventory_item_by_id(inventory_item_id: int, session: DbSession) -> InventoryItem:
#     inventory_item = session.exec(select(InventoryItem).where(InventoryItem.id == inventory_item_id)).one_or_none()
#     if inventory_item is None:
#         raise HTTPException(status_code=404, detail="Inventory Item not found")
#     return inventory_item

# # Delete Inventory Item by ID
# def delete_inventory_item_by_id(inventory_item_id: int, session: DbSession) -> dict:
#     # Step 1: Get the Inventory Item by ID
#     inventory_item = session.exec(select(InventoryItem).where(InventoryItem.id == inventory_item_id)).one_or_none()
#     if inventory_item is None:
#         raise HTTPException(status_code=404, detail="Inventory Item not found")
#     # Step 2: Delete the Inventory Item
#     session.delete(inventory_item)
#     session.commit()
#     return {"message": "Inventory Item Deleted Successfully"}

# # Update Inventory Item by ID
# def update_inventory_item_by_id(item_id: int, to_update_item_data: InventoryItem, session: DbSession) -> dict:
#     """Update a single inventory item by ID"""
#     item = session.get(InventoryItem, item_id)
#     if item is None:
#         raise HTTPException(status_code=404, detail="Item not found")
#     for var, value in vars(to_update_item_data).items():
#         setattr(item, var, value)
#     session.add(item)
#     session.commit()
#     return {"message": "Inventory Item Updated Successfully", "data": item}


from fastapi import HTTPException
from sqlmodel import Session, select
from app.models.inventory_model import InventoryItem

def add_new_inventory_item(inventory_item_data: InventoryItem, session: Session) -> InventoryItem:
    try:
        session.add(inventory_item_data)
        session.commit()
        session.refresh(inventory_item_data)
        return inventory_item_data
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

def get_all_inventory_items(session: Session) -> list[InventoryItem]:
    try:
        all_inventory_items = session.exec(select(InventoryItem)).all()
        return all_inventory_items
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

def get_inventory_item_by_id(inventory_item_id: int, session: Session) -> InventoryItem:
    try:
        inventory_item = session.exec(select(InventoryItem).where(InventoryItem.id == inventory_item_id)).one_or_none()
        if inventory_item is None:
            raise HTTPException(status_code=404, detail="Inventory Item not found")
        return inventory_item
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

def delete_inventory_item_by_id(inventory_item_id: int, session: Session) -> dict:
    try:
        inventory_item = session.exec(select(InventoryItem).where(InventoryItem.id == inventory_item_id)).one_or_none()
        if inventory_item is None:
            raise HTTPException(status_code=404, detail="Inventory Item not found")
        session.delete(inventory_item)
        session.commit()
        return {"message": "Inventory Item Deleted Successfully"}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    # Update Inventory Item by ID
def update_inventory_item_by_id(item_id: int, to_update_item_data: InventoryItem, session: Session) -> dict:
    """Update a single inventory item by ID"""
    item = session.get(InventoryItem, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    for var, value in vars(to_update_item_data).items():
        setattr(item, var, value)
    session.add(item)
    session.commit()
    return {"message": "Inventory Item Updated Successfully", "data": item}