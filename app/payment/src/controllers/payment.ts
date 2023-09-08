import { Request, Response } from "express";
import { createPayment } from "../services/payment";
import log from "../utils/logger";

const createPaymentHandler = async (req: Request, res: Response) => {
    try {
        const { id } = req.user;
        const { payment, error } = await createPayment(req.body, id);
        if (error) {
            log.error(error);
            return res.status(400).json({ message: error });
        }

        log.info(`Payment created successfully`);
        return res.status(201).json({ message: "Payment created successfully", payment });
    } catch (error) {
        log.error({ message: "Payment creation failed", error });
        res.status(400).json({ message: "Payment creation failed" });
    }
}

export { createPaymentHandler };