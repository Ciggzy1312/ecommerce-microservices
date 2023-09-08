import { expirationQueue } from "../../queues/expiration";
import log from "../../utils/logger";


export async function orderConsumer (message: any) {
    try {
        const delay = new Date(message.expiresAt).getTime() - new Date().getTime();

        await expirationQueue.add({
            _id: message._id,
            createdBy: message.createdBy,
        }, {
            delay
        });

        log.info({ message: "Expiration job created" });
    } catch (error: any) {
        log.error({ message: "Error while creating expiration job", error });
    }
}