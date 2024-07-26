# from fastapi import FastAPI
# from sqlmodel import SQLModel, create_engine
# from app.router import router as user_router

# app = FastAPI()

# # Database setup
# DATABASE_URL = "postgresql://ziakhan:my_password@PostgresCont:5432/mydatabase"
# engine = create_engine(DATABASE_URL, echo=True)

# @app.on_event("startup")
# def on_startup():
#     SQLModel.metadata.create_all(engine)

# app.include_router(user_router)

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)




# main.py
from fastapi import FastAPI
from sqlmodel import SQLModel
from app.db import engine
from app.router import router as user_router

app = FastAPI()

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

app.include_router(user_router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


