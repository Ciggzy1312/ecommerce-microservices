import aio_pika

async def basePublisher(exchangeName: str, data):
    try:
        connection = await aio_pika.connect_robust("amqp://guest:guest@rabbitmq-srv/")
        channel = await connection.channel()
        exchange = await channel.declare_exchange(exchangeName, aio_pika.ExchangeType.FANOUT)
        await exchange.publish(aio_pika.Message(body=str(data).encode()), routing_key="")

        return f"Message sent to {exchangeName} exchange", None
    except Exception as e:
        return None, str(e)