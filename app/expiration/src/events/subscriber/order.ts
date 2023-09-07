import log from "../../utils/logger";


export async function orderConsumer (queueName: string, message: any) {
    try {
        const delay = new Date(message.expiresAt).getTime() - new Date().getTime();

        console.log(delay)

        
        console.log("Expiration job ", message);
        console.log(message._id);
    } catch (error: any) {
        log.error({ message: "Error while creating expiration job", error });
    }
}