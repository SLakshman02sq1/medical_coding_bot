from fastapi import FastAPI
from appv1.chat import router as chat_router
from appv1.mysql_database import engine,Base

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(chat_router)

@app.get("/")

def display():
    return {"message":"Welcome to Medical Coding Bot"}