import log from "../utils/logger";
import { PaymentInput } from "../types/types";
import { Payment } from "../models/payment";
import { Order } from "../models/order";
import { paymentSuccessPublisher } from "../events/publishers/payment";

export const createPayment = async (input: PaymentInput, id: string) => {
    try {
        // check if order exists
        const order = await Order.findById(input.orderId);
        if (!order) {
            return { error: "Order not found" };
        }

        // check if order is created by the same user
        if (order.createdBy !== id) {
            return { error: "Not authorized" };
        }

        // check if order is not cancelled
        if (order.status === "CANCELLED") {
            return { error: "Cannot pay for cancelled order" };
        }

        if (order.status === "COMPLETED") {
            return { error: "Order is already completed" };
        }

        // check if amount is same as order price
        if (order.price !== input.amount) {
            return { error: "Please enter the correct amount" };
        }

        // perform payment
        const payment = await Payment.create({
            orderId: input.orderId,
            createdBy: id,
        });

        await Order.findByIdAndUpdate(input.orderId, { status: "COMPLETED" });
        // publish payment successfull event
        await paymentSuccessPublisher(payment);

        return { payment, error: null };

    } catch (error: any) {
        log.error(error.message);
        return { error: "Payment creation failed" };
    }
}