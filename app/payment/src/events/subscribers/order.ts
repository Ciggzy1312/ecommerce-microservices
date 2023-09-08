import { Order } from "../../models/order";
import log from "../../utils/logger";

export async function orderCreatedConsumer (message: any) {
    try {
        const order = await Order.create({
            _id: message._id,
            price: message.product.price,
            status: message.status,
            createdBy: message.createdBy,
        })

        log.info({ message: "Order for payment created successfully", order });
    } catch (error: any) {
        log.error({ message: "Error while create order event", error });
    }
}

export async function orderCancelledConsumer (message: any) {
    try {
        const order = await Order.findById(message._id);

        if (!order) {
            log.error({ message: "Order not found" });
            return;
        }

        if (order.status === "COMPLETED") {
            log.info("Order is already completed");
            return;
        }

        order.set({ status: "CANCELLED" });
        await order.save();

        log.info({ message: "Payment expired successfully", order });
    } catch (error: any) {
        log.error({ message: "Error while expire payment event", error });
    }
}