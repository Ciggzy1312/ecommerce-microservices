from fastapi import APIRouter

from routes import product

router = APIRouter(prefix="/api")

router.include_router(product.router)