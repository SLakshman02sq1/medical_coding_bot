from fastapi import FastAPI
from .chat import router as chat_router
from .database import engine,Base

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(chat_router, prefix="/api")

@app.get("/")

def display():
    return {"message":"Welcome to Medical Coding Bot"}