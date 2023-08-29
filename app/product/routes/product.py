from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from bson import ObjectId

from models.product import ProductCreateSchema
from services.product import createProduct, getProducts
from dependency import get_current_user

router = APIRouter(prefix="/product")

# Create Product -> POST /api/product
@router.post("/")
async def createProductHandler(payload: ProductCreateSchema, currentUser: dict = Depends(get_current_user)):
    if(payload.name == "" or payload.description == "" or payload.price == ""):
        return JSONResponse(status_code=400, content={"message": "Please fill all the fields"})

    payload.createdBy = ObjectId(currentUser["id"])

    product, error = await createProduct(payload.dict())
    if error:
        return JSONResponse(status_code=400, content={"message": error})

    return JSONResponse(status_code=201, content={"message": "User registered successfully", "productId": str(product.inserted_id)})


# Get All Products -> GET /api/product
@router.get("/")
async def getProductsHandler():
    products, error = await getProducts()
    if error:
        return JSONResponse(status_code=400, content={"message": error})

    return JSONResponse(status_code=200, content={"message": "Products fetched successfully", "products": products})