import express from "express";
import paymentRouter from "./payment";

const router = express.Router();

router.use(paymentRouter);

export default router;