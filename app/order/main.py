from fastapi import FastAPI
from events.subscriber.base import baseSubscriber

from api import router

app = FastAPI()

app.include_router(router)

@app.on_event("startup")
async def startup_event():
    await baseSubscriber("ProductCreated", "Order_ProductCreated")
    await baseSubscriber("ProductUpdated", "Order_ProductUpdated")
    await baseSubscriber("OrderExpired", "Order_OrderExpired")
    await baseSubscriber("PaymentCompleted", "Order_PaymentCompleted")