# main.py
from fastapi import FastAPI, Depends
from app.models import User
from app.db import get_session, init_db
from app.crud import create_user, get_user, get_users, update_user, delete_user
from app.lifespan import app

init_db()

@app.post("/users/", response_model=User)
def create_user_endpoint(user: User, session: Session = Depends(get_session)):
    return create_user(session, user)

@app.get("/users/{user_id}", response_model=User)
def get_user_endpoint(user_id: int, session: Session = Depends(get_session)):
    return get_user(session, user_id)

@app.get("/users/", response_model=List[User])
def get_users_endpoint(session: Session = Depends(get_session)):
    return get_users(session)

@app.put("/users/{user_id}", response_model=User)
def update_user_endpoint(user_id: int, user: User, session: Session = Depends(get_session)):
    user.id = user_id
    return update_user(session, user)

@app.delete("/users/{user_id}", response_model=User)
def delete_user_endpoint(user_id: int, session: Session = Depends(get_session)):
    return delete_user(session, user_id)
