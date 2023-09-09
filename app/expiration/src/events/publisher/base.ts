import amqp from 'amqplib';

const connectURL = "amqp://rabbitmq-srv:5672";

export async function basePublisher (exchangeName: string, data: any) {
    try {
        const connection = await amqp.connect(connectURL);
        const channel = await connection.createChannel();

        await channel.assertExchange(exchangeName, 'fanout', { durable: false });
        await channel.publish(exchangeName, '', Buffer.from(JSON.stringify(data)));

        return { message: `Message published to ${exchangeName}`, error: null};
    } catch (error: any) {
        return { error: `Error publishing message to ${exchangeName}` };
    }
}