from fastapi import FastAPI
from events.subscriber.base import baseSubscriber

from api import router

app = FastAPI()

app.include_router(router)

@app.on_event("startup")
async def startup_event():
    await baseSubscriber("OrderCreated", "Product_OrderCreated")
    await baseSubscriber("OrderCancelled", "Product_OrderCancelled")
    await baseSubscriber("PaymentCompleted", "Product_PaymentCompleted")