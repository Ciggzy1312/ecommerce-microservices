from bson import ObjectId
from events.publisher.base import basePublisher
from serializers.product import product_serializer

async def productCreatedPublisher(exchangeName: str, product):

    data = {
        "_id": str(ObjectId(product["_id"])),
        "name": product["name"],
        "price": product["price"]
    }

    message, error = await basePublisher(exchangeName, data)

    if error:
        print(error)

    print(message)

async def productUpdatedPublisher(exchangeName: str, product):

    data = {
        "_id": str(ObjectId(product["_id"])),
        "name": product["name"],
        "price": product["price"]
    }

    message, error = await basePublisher(exchangeName, data)

    if error:
        print(error)

    print(message)