# app/main.py
from fastapi import FastAPI
from app.router import router
from app.db import engine
from sqlmodel import SQLModel
from app.auth_routher import auth_router

app = FastAPI(title="Order Service API with DB", version="0.0.1")

@app.on_event("startup")
async def on_startup():
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

app.include_router(auth_router)
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    