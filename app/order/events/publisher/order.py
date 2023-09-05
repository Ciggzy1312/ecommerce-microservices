from bson import ObjectId
from events.publisher.base import basePublisher
from serializers.order import order_serializer

async def orderCreatedPublisher(exchangeName: str, order):

    data = order_serializer(order)

    message, error = await basePublisher(exchangeName, data)

    if error:
        print(error)

    print(message)

async def orderCancelledPublisher(exchangeName: str, order):

    data = order_serializer(order)

    message, error = await basePublisher(exchangeName, data)

    if error:
        print(error)

    print(message)