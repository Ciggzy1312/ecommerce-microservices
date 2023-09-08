import { Order } from "../../models/order.model";
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
        const order = await Order.findByIdAndUpdate(message._id, { status: "CANCELLED" }, { new: true });

        log.info({ message: "Payment expired successfully", order });
    } catch (error: any) {
        log.error({ message: "Error while expire payment event", error });
    }
}