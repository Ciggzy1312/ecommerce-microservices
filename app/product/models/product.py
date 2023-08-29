from pydantic import BaseModel

class ProductCreateSchema(BaseModel):
    name: str
    description: str
    price: str
    createdBy: str = None