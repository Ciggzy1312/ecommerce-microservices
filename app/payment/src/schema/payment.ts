import { z } from "zod";

export const createPaymentSchema = z.object({
    orderId: z.string({
        required_error: "OrderId is required",
        invalid_type_error: "OrderId must be a string",
    }),
    amount: z.string({
        required_error: "Amount is required",
        invalid_type_error: "Amount must be a string",
    }),
});