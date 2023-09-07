import { baseConsumer } from "./events/subscriber/base";
import log from "./utils/logger";

const start = async () => {
    baseConsumer("OrderCreated", "Expiration_OrderCreated");

    log.info("Expiration service is running...");
};

start();