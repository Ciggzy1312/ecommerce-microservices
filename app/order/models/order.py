from pydantic import BaseModel

class OrderCreateSchema(BaseModel):
    status: str = None
    expiresAt: str = None
    createdBy: str = None
    productId: str