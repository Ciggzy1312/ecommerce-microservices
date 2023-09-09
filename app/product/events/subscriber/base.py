import aio_pika
from events.subscriber.order import orderCreatedSubscriber, orderCancelledSubscriber
from events.subscriber.payment import paymentCompletedSubscriber

async def on_message(msg: aio_pika.IncomingMessage):
    exchangeName = msg.exchange

    if exchangeName == "OrderCreated":
        message, error = await orderCreatedSubscriber(msg.body.decode("utf-8"))
        if error:
            print(error)
            return

        print(message)
        await msg.ack()

    elif exchangeName == "OrderCancelled":
        message, error = await orderCancelledSubscriber(msg.body.decode("utf-8"))
        if error:
            print(error)
            return

        print(message)
        await msg.ack()

    elif exchangeName == "PaymentCompleted":
        message, error = await paymentCompletedSubscriber(msg.body.decode("utf-8"))
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