from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from app.models import User, UserCreate, UserUpdate
from app.db import get_session
from app.crud import get_all_users, get_user, create_user, update_user, delete_user
from app.dependencies import oauth2_scheme
from app.schemas import TokenData
# router = APIRouter()
router = APIRouter(
    prefix="/Service",
    tags=["User Service"],
    responses={404: {"description": "Not found"}},
)

user_router = APIRouter(
    prefix="/service",
    tags=["service"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(oauth2_scheme)]
)

@router.post("/users/", response_model=User)
def create_new_user(user: UserCreate, session: Session = Depends(get_session)):
    return create_user(session=session, user_create=user)

@router.get("/users/{user_id}", response_model=User)
def read_user(user_id: int, session: Session = Depends(get_session)):
    db_user = get_user(session, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put("/users/{user_id}", response_model=User)
def update_existing_user(*, session: Session = Depends(get_session), user_id: int, user: UserUpdate):
    db_user = get_user(session, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return update_user(session, db_user, user)

@router.delete("/users/{user_id}", response_model=User)
def delete_existing_user(user_id: int, session: Session = Depends(get_session)):
    db_user = get_user(session, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return delete_user(session, user_id)

@router.patch("/users/{user_id}", response_model=User)
async def update_user_route(user_id: int, user: UserUpdate, session: Session = Depends(get_session)):
    db_user = session.get(User, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    updated_user = update_user(session, db_user, user)
    return updated_user

@router.get("/users/", response_model=List[User])
def read_all_users(skip: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    users = get_all_users(session, skip=skip, limit=limit)
    return users



# # app/router.py
# from typing import List
# from fastapi import APIRouter, Depends, HTTPException, status
# from fastapi.security import OAuth2PasswordRequestForm
# from sqlmodel import Session
# from app.models import User, UserCreate, UserUpdate
# from app.db import get_session
# from app.crud import get_all_users, get_user, create_user, update_user, delete_user, authenticate_user
# from app.auth import create_access_token
# from app.dependencies import get_current_user, get_current_admin_user
# from app.schemas import Token

# router = APIRouter()

# @router.post("/token", response_model=Token)
# async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
#     user = authenticate_user(session, form_data.username, form_data.password)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token = create_access_token(data={"sub": user.email})
#     return {"access_token": access_token, "token_type": "bearer"}

# @router.post("/users/", response_model=User)
# def create_new_user(user: UserCreate, session: Session = Depends(get_session)):
#     return create_user(session=session, user_create=user)

# @router.get("/users/me", response_model=User)
# async def read_users_me(current_user: User = Depends(get_current_user)):
#     return current_user

# @router.get("/users/{user_id}", response_model=User)
# def read_user(user_id: int, session: Session = Depends(get_session), current_user: User = Depends(get_current_admin_user)):
#     db_user = get_user(session, user_id)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user

# @router.put("/users/{user_id}", response_model=User)
# def update_existing_user(user_id: int, user: UserUpdate, session: Session = Depends(get_session), current_user: User = Depends(get_current_admin_user)):
#     db_user = get_user(session, user_id)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return update_user(session, db_user, user)

# @router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_existing_user(user_id: int, session: Session = Depends(get_session), current_user: User = Depends(get_current_admin_user)):
#     delete_user(session, user_id)
#     return {"ok": True}

# @router.get("/users/", response_model=List[User])
# def read_all_users(skip: int = 0, limit: int = 100, session: Session = Depends(get_session), current_user: User = Depends(get_current_admin_user)):
#     users = get_all_users(session, skip=skip, limit=limit)
#     return users
