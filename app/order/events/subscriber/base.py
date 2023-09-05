import aio_pika
from events.subscriber.product import productCreatedSubscriber, productUpdatedSubscriber

async def on_message(msg: aio_pika.IncomingMessage):
    exchangeName = msg.exchange

    if exchangeName == "ProductCreated":
        message, error = await productCreatedSubscriber(msg.body.decode("utf-8"))
        if error:
            print(error)
            return

        print(message)
        await msg.ack()

    elif exchangeName == "ProductUpdated":
        message, error = await productUpdatedSubscriber(msg.body.decode("utf-8"))
        if error:
            print(error)
            return

        print(message)
        await msg.ack()

async def baseSubscriber(exchangeName, queueName):
    connection = await aio_pika.connect_robust("amqp://guest:guest@rabbitmq-srv/")
    channel = await connection.channel()
    exchange = await channel.declare_exchange(exchangeName, aio_pika.ExchangeType.FANOUT)
    queue = await channel.declare_queue(queueName)
    await queue.bind(exchangeName)
    await queue.consume(on_message)