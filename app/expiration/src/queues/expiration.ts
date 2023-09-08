import Queue from "bull";
import { orderExpiredPublisher } from "../events/publisher/expiration";

const expirationQueue = new Queue("expiration", 'redis://localhost:6379');

expirationQueue.process(async function(job) {
    await orderExpiredPublisher(job.data);
});

export { expirationQueue };