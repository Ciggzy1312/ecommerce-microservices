from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from bson import ObjectId

from models.order import OrderCreateSchema
from services.order import createOrder, getOrders, getOrder, cancelOrder
from dependency import get_current_user

router = APIRouter(prefix="/order")

# Create Order -> POST /api/order
@router.post("/")
async def createOrderHandler(payload: OrderCreateSchema, currentUser: dict = Depends(get_current_user)):
    if(payload.productId == ""):
        return JSONResponse(status_code=400, content={"message": "Please fill all the fields"})

    payload.createdBy = ObjectId(currentUser["id"])

    order, error = await createOrder(payload.dict())
    if error:
        return JSONResponse(status_code=400, content={"message": error})

    return JSONResponse(status_code=201, content={"message": "Order created successfully", "orderID": str(order.inserted_id)})


# Get Orders -> GET /api/order
@router.get("/")
async def getOrdersHandler(currentUser: dict = Depends(get_current_user)):
    orders, error = await getOrders(ObjectId(currentUser["id"]))
    if error:
        return JSONResponse(status_code=400, content={"message": error})

    return JSONResponse(status_code=200, content={"message": "Orders fetched successfully", "orders": orders})


# Get Order -> GET /api/order/{id}
@router.get("/{id}")
async def getOrderHandler(id: str, currentUser: dict = Depends(get_current_user)):
    order, error = await getOrder(id, ObjectId(currentUser["id"]))
    if error:
        return JSONResponse(status_code=400, content={"message": error})

    return JSONResponse(status_code=200, content={"message": "Order fetched successfully", "order": order})


# Cancel Order -> PUT /api/order/{id}
@router.put("/{id}")
async def cancelOrderHandler(id: str, currentUser: dict = Depends(get_current_user)):
    order, error = await cancelOrder(id, ObjectId(currentUser["id"]))
    if error:
        return JSONResponse(status_code=400, content={"message": error})

    return JSONResponse(status_code=200, content={"message": "Order cancelled successfully"})