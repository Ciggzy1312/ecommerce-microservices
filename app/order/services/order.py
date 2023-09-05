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


async def getOrder(id: str, userId: str):
    try:
        pipeline = [
            {
                "$match": {
                    "_id": ObjectId(id),
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

        order = await Order.aggregate(pipeline).to_list(1)
        if not order:
            return None, "Order not found"

        return order_serializer(order[0]), None
    except Exception as e:
        return None, str(e)


async def cancelOrder(id: str, userId: str):
    try:
        orderExists = await Order.find_one({"_id": ObjectId(id)})
        if not orderExists:
            return None, "Order not found"

        if ObjectId(orderExists["createdBy"]) != userId:
            return None, "Not authorized to cancel this order"

        orderCancelled = await Order.update_one({"_id": ObjectId(id)}, {"$set": {"status": "CANCELLED"}})
        if not orderCancelled:
            return None, "Error cancelling order"

        return orderCancelled, None
    except Exception as e:
        return None, str(e)