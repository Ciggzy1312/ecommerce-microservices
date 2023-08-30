from pydantic import BaseModel

class ProductCreateSchema(BaseModel):
    name: str
    description: str
    price: str
    createdBy: str = None

class ProductUpdateSchema(BaseModel):
    name: str = None
    description: str = None
    price: str = None