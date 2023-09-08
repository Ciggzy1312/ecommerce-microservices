import express from "express";
import { createPaymentHandler } from "../controllers/payment";
import validate from "../middlewares/validateResources";
import { createPaymentSchema } from "../schema/payment";
import authMiddleware from "../middlewares/authMiddleware";

const router = express.Router();

router.post("/api/payment", authMiddleware, validate(createPaymentSchema), createPaymentHandler);

export default router;