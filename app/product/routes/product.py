from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from bson import ObjectId

from models.product import ProductCreateSchema, ProductUpdateSchema
from services.product import createProduct, getProducts, getProduct, updateProduct
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


# Get Product By Id -> GET /api/product/{id}
@router.get("/{id}")
async def get_product_by_id(id: str, currentUser: dict = Depends(get_current_user)):
    product, error = await getProduct(id)
    if error:
        return JSONResponse(status_code=400, content={"message": error})

    return JSONResponse(status_code=200, content={"message": "Product fetched successfully", "product": product})


# Update Product By Id -> PUT /api/product/{id}
@router.put("/{id}")
async def update_product_by_id(id: str, product: ProductUpdateSchema, currentUser: dict = Depends(get_current_user)):
    userId = currentUser["id"]

    productUpdated, error = await updateProduct(id, userId, product.dict())
    if error:
        return JSONResponse(status_code=400, content={"message": error})

    return JSONResponse(status_code=200, content={"message": "Product updated successfully"})