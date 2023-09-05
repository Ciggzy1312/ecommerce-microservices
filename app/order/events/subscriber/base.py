import aio_pika
from events.subscriber.product import productCreatedSubscriber, productUpdatedSubscriber

async def on_message(message: aio_pika.IncomingMessage):
    exchangeName = message.exchange

    if exchangeName == "ProductCreated":
        product, error = await productCreatedSubscriber(message.body.decode("utf-8"))
        if error:
            print(error)
            return

        await message.ack()
    elif exchangeName == "ProductUpdated":
        product, error = await productUpdatedSubscriber(message.body.decode("utf-8"))
        if error:
            print(error)
            return

        await message.ack()

async def baseSubscriber(exchangeName, queueName):
    connection = await aio_pika.connect_robust("amqp://guest:guest@rabbitmq-srv/")
    channel = await connection.channel()
    queue = await channel.declare_queue(queueName)
    await queue.bind(exchangeName)
    await queue.consume(on_message)