from fastapi import APIRouter

from routes import order

router = APIRouter(prefix="/api")

router.include_router(order.router)