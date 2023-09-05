import json
from datetime import datetime, timedelta
from bson import ObjectId
from utils.database import Product, Order

from serializers.order import order_serializer

EXPIRATION_TIME = 60

async def createOrder(payload: dict):
    try:
        # Check if product exists
        productExists = await Product.find_one({"_id": ObjectId(payload["productId"])})
        if not productExists:
            return None, "Product not found"

        # Check if product is reserved
        productReserved = await Order.find_one({"productId": ObjectId(payload["productId"]), "status": {"$ne": "CANCELLED"}})
        if productReserved:
            return None, "Product is reserved"

        # Set expiration time
        expiration = datetime.now() + timedelta(seconds=EXPIRATION_TIME)

        payload["expiresAt"] = expiration
        payload["status"] = "CREATED"
        payload["productId"] = ObjectId(payload["productId"])

        print(payload)

        order = await Order.insert_one(payload)
        return order, None
    except Exception as e:
        return None, str(e)


async def getOrders(userId: str):
    try:
        ordersList = []
        pipeline = [
            {
                "$match": {
                    "createdBy": ObjectId(userId)
                }
            },
            {
                "$lookup": {
                    "from": "product",
                    "localField": "productId",
                    "foreignField": "_id",
                    "as": "product"
                }
            }
        ]

        async for order in Order.aggregate(pipeline):
            ordersList.append(order_serializer(order))

        return ordersList, None
    except Exception as e:
        return None, str(e)