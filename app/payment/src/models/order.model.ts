import mongoose from "mongoose";

const orderSchema = new mongoose.Schema({
    _id: {
        type: String,
        required: true,
    },
    status: {
        type: String,
        required: true,
        default: "CREATED",
    },
    price: {
        type: String,
        required: true,
    },
    createdBy: {
        type: String,
        required: true,
    },
},{ _id : false });

export const Order = mongoose.model("Order", orderSchema);