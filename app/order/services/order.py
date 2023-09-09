import json
from datetime import datetime, timedelta
from bson import ObjectId
from utils.database import Product, Order

from serializers.order import order_serializer
from events.publisher.order import orderCreatedPublisher, orderCancelledPublisher

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

        order = await Order.insert_one(payload)

        pipeline = [
            {
                "$match": {
                    "_id": order.inserted_id
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

        orderCreated = await Order.aggregate(pipeline).to_list(1)

        await orderCreatedPublisher("OrderCreated", orderCreated[0])

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
            return "Order not found", None

        if ObjectId(orderExists["createdBy"]) != userId:
            return "Not authorized to cancel this order", None

        if orderExists["status"] == "COMPLETED":
            return "Order is already completed", None

        if orderExists["status"] == "CANCELLED":
            return "Order is already cancelled", None

        order = await Order.update_one({"_id": ObjectId(id)}, {"$set": {"status": "CANCELLED"}})
        if not order:
            return None, "Error cancelling order"

        pipeline = [
            {
                "$match": {
                    "_id": ObjectId(id)
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

        orderCancelled = await Order.aggregate(pipeline).to_list(1)

        await orderCancelledPublisher("OrderCancelled", orderCancelled[0])

        return "Successfully expired order", None
    except Exception as e:
        return None, str(e)


async def completeOrder(id: str, userId: str):
    try:
        orderExists = await Order.find_one({"_id": ObjectId(id)})
        if not orderExists:
            return "Order not found", None

        if ObjectId(orderExists["createdBy"]) != userId:
            return "Not authorized to complete this order", None

        if orderExists["status"] == "COMPLETED":
            return "Order is already completed", None

        if orderExists["status"] == "CANCELLED":
            return "Order is already cancelled", None

        order = await Order.update_one({"_id": ObjectId(id)}, {"$set": {"status": "COMPLETED"}})
        if not order:
            return None, "Error completing order"

        return "Successfully completed order", None
    except Exception as e:
        return None, str(e)