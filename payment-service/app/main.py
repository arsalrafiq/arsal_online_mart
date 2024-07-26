from fastapi import FastAPI
from app.router import router
from sqlmodel import SQLModel
from app.db import engine

app = FastAPI()

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

app.include_router(router)
