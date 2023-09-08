import mongoose from "mongoose";
import log from "./logger";

async function connectDB() {
    try {
        await mongoose.connect("mongodb://payment-db-srv:27017/payment");
        log.info("Successfully connected to payment database");
    } catch (error) {
        log.error("Error connecting to payment database: ", error);
    }
}

export default connectDB;