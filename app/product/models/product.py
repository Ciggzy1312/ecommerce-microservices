from pydantic import BaseModel

class ProductCreateSchema(BaseModel):
    name: str
    description: str
    price: str
    orderId: str = None
    createdBy: str = None

class ProductUpdateSchema(BaseModel):
    name: str = None
    description: str = None
    price: str = None