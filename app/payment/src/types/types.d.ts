declare global {
    namespace Express {
        interface Request {
            user: any;
        }
    }
}

export interface PaymentInput {
    orderId: string;
    amount: string;
}