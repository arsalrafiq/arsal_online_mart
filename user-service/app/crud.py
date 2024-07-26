from sqlmodel import Session, select
from app.models import User, UserCreate, UserUpdate
from fastapi import HTTPException, status
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt
from typing import Optional, Union, List

SECRET_KEY = "fhwM72RXWmBm4SerqVWygdIkbcb-NBKn7ftOCisUcyG2vWO-2J74egaHo7LZreNq"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_user_by_email(session: Session, email: str) -> Optional[User]:
    return session.exec(select(User).where(User.email == email)).first()

def get_user(session: Session, user_id: Union[int, str]) -> Optional[User]:
    if isinstance(user_id, int):
        return session.get(User, user_id)
    elif isinstance(user_id, str):
        return get_user_by_email(session, user_id)
    else:
        raise ValueError("user_id must be either an integer ID or an email string")

def create_user(session: Session, user_create: UserCreate) -> User:
    existing_user = get_user_by_email(session, user_create.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    db_user = User(
        name=user_create.name,
        email=user_create.email,
        hashed_password=get_password_hash(user_create.password),
        is_admin=user_create.is_admin  # Handle is_admin
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

def update_user(session: Session, db_user: User, user: UserUpdate) -> User:
    if user.name:
        db_user.name = user.name
    if user.email:
        db_user.email = user.email
    if user.password:
        db_user.hashed_password = get_password_hash(user.password)
    if user.is_admin is not None:
        db_user.is_admin = user.is_admin  # Update is_admin if provided
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

def delete_user(session: Session, user_id: int) -> None:
    db_user = session.get(User, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(db_user)
    session.commit()

def authenticate_user(session: Session, email: str, password: str) -> Optional[User]:
    user = get_user_by_email(session, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

def login_user(session: Session, email: str, password: str) -> str:
    user = authenticate_user(session, email, password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    return access_token

def get_all_users(session: Session, skip: int = 0, limit: int = 100) -> List[User]:
    statement = select(User).offset(skip).limit(limit)
    users = session.exec(statement).all()
    return users



# # app/crud.py
# from fastapi import HTTPException, status
# from sqlmodel import Session, select
# from app.models import User, UserCreate, UserUpdate
# from app.auth import get_password_hash, verify_password
# from typing import List, Optional

# def get_user_by_email(session: Session, email: str) -> Optional[User]:
#     return session.exec(select(User).where(User.email == email)).first()

# def get_user(session: Session, user_id: int) -> Optional[User]:
#     return session.get(User, user_id)

# def create_user(session: Session, user_create: UserCreate) -> User:
#     existing_user = get_user_by_email(session, user_create.email)
#     if existing_user:
#         raise HTTPException(status_code=400, detail="Email already registered")
    
#     db_user = User(
#         name=user_create.name,
#         email=user_create.email,
#         hashed_password=get_password_hash(user_create.password),
#         is_admin=user_create.is_admin
#     )
#     session.add(db_user)
#     session.commit()
#     session.refresh(db_user)
#     return db_user

# def update_user(session: Session, db_user: User, user: UserUpdate) -> User:
#     if user.name:
#         db_user.name = user.name
#     if user.email:
#         db_user.email = user.email
#     if user.password:
#         db_user.hashed_password = get_password_hash(user.password)
#     if user.is_admin is not None:
#         db_user.is_admin = user.is_admin
#     session.add(db_user)
#     session.commit()
#     session.refresh(db_user)
#     return db_user

# def delete_user(session: Session, user_id: int) -> None:
#     db_user = session.get(User, user_id)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     session.delete(db_user)
#     session.commit()

# def get_all_users(session: Session, skip: int = 0, limit: int = 100) -> List[User]:
#     statement = select(User).offset(skip).limit(limit)
#     users = session.exec(statement).all()
#     return users

# def authenticate_user(session: Session, email: str, password: str) -> Optional[User]:
#     user = get_user_by_email(session, email)
#     if not user or not verify_password(password, user.hashed_password):
#         return None
#     return user
