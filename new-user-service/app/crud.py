# app/crud.py
from sqlmodel import Session
from app.models import User

def create_user(session: Session, user: User):
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def get_user(session: Session, user_id: int):
    return session.get(User, user_id)

def get_users(session: Session):
    return session.exec(select(User)).all()

def update_user(session: Session, user: User):
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def delete_user(session: Session, user_id: int):
    user = session.get(User, user_id)
    if user:
        session.delete(user)
        session.commit()
    return user
