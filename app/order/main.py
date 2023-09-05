from fastapi import FastAPI
from events.subscriber.base import baseSubscriber

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.on_event("startup")
async def startup_event():
    await baseSubscriber("ProductCreated", "Order_ProductCreated")
    await baseSubscriber("ProductUpdated", "Order_ProductUpdated")