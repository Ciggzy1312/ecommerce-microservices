import amqp from 'amqplib';
import log from '../../utils/logger';
import { orderConsumer } from './order';

const connectURL = "amqp://rabbitmq-srv:5672";

export async function baseConsumer (exchangeName: string, queueName: string) {
    try {
        const connection = await amqp.connect(connectURL);
        const channel = await connection.createChannel();

        await channel.assertExchange(exchangeName, "fanout", { durable: false });
        await channel.assertQueue(queueName, { durable: false });
        await channel.bindQueue(queueName, exchangeName, "");
        
        channel.consume(queueName, async (msg) => {
            if (msg) {
                let message = JSON.parse(msg.content.toString().replace(/'/g, '"'));

                if (exchangeName === "OrderCreated") {
                    await orderConsumer(message);
                    channel.ack(msg);
                }
            }
        });

    } catch (error: any) {
        log.error({ message: "Error while connecting to RabbitMQ", error});
    }
}